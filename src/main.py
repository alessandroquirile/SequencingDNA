import os

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

CLASS_MAPPING = {
    0: 'Recettori accoppiati a proteine G',
    1: 'Tirosin-chinasi',
    2: 'Tirosina fosfatasi',
    3: 'Sintetasi',
    4: 'Sintasi',
    5: 'Canale ionico',
    6: 'Fattore di trascrizione'
}


def get_kmers(sequence: str, k: int = 6) -> str:
    """Extract overlapping k-mers of length k from a sequence and join them with spaces."""
    return ' '.join([sequence[i:i + k] for i in range(len(sequence) - k + 1)])


def run_pipeline(data_path: str, k: int = 6, test_size: float = 0.2, random_state: int = 42):
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at {data_path}")

    # Loading data set
    df = pd.read_table(data_path)
    print(f"Loaded {len(df)} DNA sequences from {data_path}")

    # Map numerical class to description
    df['class_description'] = df['class'].map(CLASS_MAPPING)

    # Generate 6-mers
    df['k-mers'] = df['sequence'].apply(lambda seq: get_kmers(seq, k))

    # Stratified Train-Test split FIRST (before vectorizer fit to avoid data leakage)
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
    classifier = LogisticRegression(max_iter=1000)
    classifier.fit(x_train, y_train)

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


if __name__ == '__main__':
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    human_data_path = os.path.join(project_root, 'data', 'raw', 'human.txt')
    run_pipeline(human_data_path)
