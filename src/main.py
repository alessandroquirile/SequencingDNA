import os
import warnings

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score

CLASS_MAPPING = {
    0: 'Recettori accoppiati a proteine G',
    1: 'Tirosin-chinasi',
    2: 'Tirosina fosfatasi',
    3: 'Sintetasi',
    4: 'Sintasi',
    5: 'Canale ionico',
    6: 'Fattore di trascrizione'
}


def clean_sequence(sequence: str) -> str:
    """Clean DNA sequence: uppercase, keep only ATCG."""
    return ''.join(c for c in sequence.upper() if c in 'ATCG')


def validate_sequences(df: pd.DataFrame, col: str = 'sequence') -> pd.DataFrame:
    """Validate and clean sequences, report invalid chars."""
    original_len = len(df)
    df = df.copy()
    df[col] = df[col].apply(clean_sequence)
    # Remove empty sequences after cleaning
    df = df[df[col].str.len() > 0].reset_index(drop=True)
    removed = original_len - len(df)
    if removed:
        warnings.warn(f"Removed {removed} sequences with invalid/empty nucleotides")
    return df


def get_kmers(sequence: str, k: int = 6) -> str:
    """Extract overlapping k-mers of length k from a sequence and join them with spaces."""
    return ' '.join([sequence[i:i + k] for i in range(len(sequence) - k + 1)])


def run_pipeline(data_path: str, k: int = 6, test_size: float = 0.2, random_state: int = 42, cv_folds: int = 5):
    # Loading data set
    df = pd.read_table(data_path)
    print(f"Loaded {len(df)} DNA sequences from {data_path}")

    # Validate and clean sequences (fix #5)
    # df = validate_sequences(df)
    # print(f"After cleaning: {len(df)} valid DNA sequences")

    # Map numerical class to description
    df['class_description'] = df['class'].map(CLASS_MAPPING)

    # Generate k-mers
    df['k-mers'] = df['sequence'].apply(lambda seq: get_kmers(seq, k))

    # Stratified Train-Test split first (before vectorizer fit to avoid data leakage)
    x_raw = df['k-mers'].values
    y = df['class'].values
    x_train_raw, x_test_raw, y_train, y_test = train_test_split(
        x_raw, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # Feature extraction via Bag of Words (fit on train only)
    vectorizer = CountVectorizer()
    x_train = vectorizer.fit_transform(x_train_raw)
    x_test = vectorizer.transform(x_test_raw)

    print(f"Bag-of-Words feature matrix shape: {x_train.shape} ({x_train.shape[1]} unique {k}-mers)")

    # Train Logistic Regression Classifier
    classifier = LogisticRegression(max_iter=5000, random_state=random_state)
    classifier.fit(x_train, y_train)

    # Cross-validation
    print(f"\n--- {cv_folds}-Fold Cross-Validation ---")
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
    cv_scores = cross_val_score(classifier, x_train, y_train, cv=cv, scoring='accuracy')
    print(f"CV Accuracy: {cv_scores.mean() * 100:.2f}% ± {cv_scores.std() * 100:.2f}%")

    # Predictions and Evaluation
    y_pred = classifier.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    print("\n--- Model Performance Evaluation (Logistic Regression) ---")
    print(f"Accuracy:  {accuracy * 100:.2f}%")
    print(f"Precision: {precision * 100:.2f}%")
    print(f"Recall:    {recall * 100:.2f}%")
    print(f"F1-Score:  {f1 * 100:.2f}%")

    # Per-class metrics
    print("\n--- Per-Class Classification Report ---")
    target_names = [CLASS_MAPPING[i] for i in sorted(CLASS_MAPPING.keys())]
    print(classification_report(y_test, y_pred, target_names=target_names, digits=4))


if __name__ == '__main__':
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    human_data_path = os.path.join(project_root, 'data', 'raw', 'human.txt')
    run_pipeline(human_data_path)
