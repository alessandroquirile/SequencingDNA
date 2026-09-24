# DNA Sequence Classification with Machine Learning

This repository contains a Jupyter Notebook designed to introduce high school students to Machine Learning concepts
through a practical example: **DNA sequence classification**.

## 🧬 What is DNA Sequence Classification?

DNA sequence classification is the process of predicting the biological function or gene family of a known DNA sequence
(such as identifying ion channels, transcription factors, or G-protein coupled receptors). Scientists use machine
learning models to automatically annotate and categorize genetic sequences.

## 🤖 How Can Machine Learning Help?

Machine Learning (ML) allows us to recognize sequence patterns (such as k-mer frequencies) in DNA, helping in tasks like
classifying gene families or predicting gene function. In this notebook, we break down the problem into simple steps
that anyone can follow, even without prior programming experience!

## 📚 What You Will Learn

In this notebook, we explore:

1. **Data Analysis**: Understanding DNA sequences and preparing them for machine learning.
2. **K-mer Counting**: Splitting DNA sequences into smaller overlapping pieces (k-mers) for feature extraction.
3. **Bag-of-Words (BoW) Representation**: Converting DNA sequences into a numerical format that a machine learning model
   can understand.
4. **Model Training & Validation**: Using the **Hold-Out Method** to test our model's performance.

## 🚀 How to Use the Notebook

1. Clone this repository:
   ```bash
   git clone https://github.com/alessandroquirile/SequencingDNA.git
   ```
2. Install the required python dependencies:
    ```bash
   pip install -r requirements.txt
   ```
3. Open the Jupyter Notebook:
    ```bash
   jupyter notebook notebooks/dna-classification.ipynb
   ```

## 🎯 Who Is This For?

- **High school students** curious about science and technology.
- **Beginners in programming** who want a hands-on introduction to machine learning.
- **Anyone interested in bioinformatics** and its real-world applications.
- _The explanations are written in a **simplified and accessible language** to ensure that students with no prior
  knowledge of programming or machine learning can follow along easily._

## 💡 Why This Project?

This notebook was created as an educational tool to **make Machine Learning accessible** to students with no prior
programming knowledge. The explanations use simple, intuitive language to guide learners through the process step by
step.