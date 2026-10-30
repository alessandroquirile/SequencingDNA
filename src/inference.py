import os
import sys

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import get_kmers


def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(project_root, 'models', 'dna_classifier.joblib')
    data_path = os.path.join(project_root, 'data', 'raw', 'human.txt')

    # 1. Caricamento del modello salvato
    print("=== 1. CARICAMENTO MODELLO ===")
    saved_data = joblib.load(model_path)
    clf = saved_data['classifier']
    vec = saved_data['vectorizer']
    class_mapping = saved_data['class_mapping']
    k = saved_data.get('k', 6)
    print(f"Modello caricato con successo da: {model_path}\n")

    # 2. Parametri ottenuti dal training
    print("=== 2. PARAMETRI APPRESI DAL MODELLO ===")
    print(f"• Matrice dei Pesi W (coef_):       {clf.coef_.shape}  (7 classi x {clf.coef_.shape[1]} n_features)")
    print(f"• Vettore di Bias b (intercept_):   {clf.intercept_.shape}  (7 classi)")
    print(f"• Dimensione vocabolario 6-meri:   {len(vec.vocabulary_)}")
    print(f"• Iterazioni alla convergenza:     {clf.n_iter_[0]}")

    print("\nValori del vettore di Bias b:")
    for c_id, b_val in enumerate(clf.intercept_):
        print(f"  Classe {c_id} ({class_mapping[c_id]}): {b_val:+.4f}")

    """print("\nTop 3 esameri con peso maggiore per ciascuna classe:")
    feature_names = np.array(vec.get_feature_names_out())
    for c_id in range(len(clf.classes_)):
        top_idx = np.argsort(clf.coef_[c_id])[-3:][::-1]
        top_features = ", ".join([f"{feature_names[i]} ({clf.coef_[c_id][i]:+.3f})" for i in top_idx])
        print(f"  [{c_id}] {class_mapping[c_id]}: {top_features}")"""
    print()

    # 3. Inferenza su campioni casuali estratti dal Test Set
    print("=== 3. INFERENZA SU CAMPIONI CASUALI DEL TEST SET ===")
    df = pd.read_table(data_path)
    _, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['class'])

    # Campionamento casuale dal test set (es. 5 sequenze)
    sample_test = test_df.sample(n=5)

    for i, (_, row) in enumerate(sample_test.iterrows(), start=1):
        seq = row['sequence']
        true_class = int(row['class'])

        # Preprocessing: estrazione 6-meri e vettorizzazione
        kmers = get_kmers(seq, k)
        X = vec.transform([kmers])

        # Predizione e confidenza
        pred_class = int(clf.predict(X)[0])
        probabilities = clf.predict_proba(X)[0]
        confidence = probabilities[pred_class] * 100
        is_correct = (true_class == pred_class)

        print(f"Campione casuale #{i}:")
        print(f"  Sequenza ({len(seq)}):  {seq[:35]}...{seq[-15:]}")
        print(f"  Classe Reale:       [{true_class}] {class_mapping[true_class]}")
        print(f"  Classe Predetta:    [{pred_class}] {class_mapping[pred_class]}")
        print(f"  Confidenza:         {confidence:.2f}%")
        print(f"  Esito:              {'✓ CORRETTO' if is_correct else '✗ ERRATO'}")
        print()


if __name__ == '__main__':
    main()
