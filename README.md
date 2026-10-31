# DNA Sequence Classification with Machine Learning

This repository contains Python scripts for DNA sequence classification using k-mer features and logistic regression.

## 🧬 What is DNA Sequence Classification?

DNA sequence classification predicts the biological function or gene family of a known DNA sequence (e.g., ion channels, transcription factors, G-protein coupled receptors).

## 🤖 Approach

- **K-mer counting**: Split DNA sequences into overlapping k-mers (default k=6)
- **Bag-of-Words**: Convert k-mer counts to numerical feature vectors
- **Logistic Regression**: Multi-class classifier with cross-validation

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the model
```bash
python src/train.py
```

Trains on `data/raw/human.txt`, saves model to `models/dna_classifier.joblib`.

### 3. Run inference
```bash
python src/inference.py
```

Loads trained model, runs predictions on random test samples, shows per-class metrics and model parameters.

## 📁 Project Structure

```
SequencingDNA/
├── data/
│   └── raw/
│       └── human.txt          # Training data (TSV: sequence, class)
├── models/                     # Saved models (created after training)
├── src/
│   ├── train.py               # Training pipeline
│   ├── inference.py           # Inference & evaluation
│   └── utils.py               # K-mer extraction utilities
├── dna_pipeline.py            # Alternative pipeline script
└── requirements.txt
```

## 📊 Data Format

`human.txt` - tab-separated:
```
sequence    class
ATCGATCG...  0
GCTAGCTA...  1
...
```

Classes (0-6):
- 0: G-protein coupled receptors
- 1: Tyrosine kinase
- 2: Tyrosine phosphatase
- 3: Synthetase
- 4: Synthase
- 5: Ion channel
- 6: Transcription factor

## ⚙️ Configuration

Key parameters in `train.py`:
- `k=6` - k-mer length
- `test_size=0.2` - train/test split
- `cv_folds=5` - cross-validation folds
- `random_state=42` - reproducibility

## 📈 Output

Training prints:
- Cross-validation F1 score
- Test set accuracy, precision, recall, F1
- Per-class classification report
- Model saved to `models/dna_classifier.joblib`

Inference prints:
- Model parameters (weights, bias, vocabulary size)
- Random test sample predictions with confidence