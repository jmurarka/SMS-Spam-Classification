# SMS Spam Classification - Comprehensive Experiments Guide

## Overview

This project now includes a comprehensive experimentation framework that systematically compares different combinations of:

- **Models**: Multinomial NB, Bernoulli NB, Complement NB
- **Vectorizers**: CountVectorizer, TF-IDF Vectorizer
- **Preprocessing**: With/without stopword removal, with/without stemming
- **Hyperparameters**: max_features, ngram_range, alpha smoothing

## New Components

### 1. Enhanced `model.py`

Added the following functions for systematic experimentation:

#### `preprocess_text(text, remove_stopwords, apply_stemming)`

Flexible text preprocessing with optional stopword removal and stemming.

#### `run_experiment(...)`

Runs a single experiment with specified configuration and returns metrics:

- Accuracy, Precision, Recall, F1-Score
- Confusion Matrix
- Model and predictions

#### `run_all_experiments(df)`

Orchestrates all experiments:

- **3 Main Experiments** (predefined configurations)
- **Additional Tweaks** (hyperparameter variations):
  - Vectorizer max_features: 500, 3000, 5000
  - NGram range: (1,1) vs (1,2)
  - Alpha smoothing: 0.1, 0.5, 1.0
  - Stopword removal: on/off
  - Stemming: on/off

#### `create_comparison_table(all_results)`

Generates a comparison DataFrame with all metrics for easy viewing.

#### `generate_report(all_results, df)`

Creates a formatted report with the structure:

1. Introduction
2. Dataset Overview
3. Preprocessing Steps
4. Experiment 1 - Multinomial NB + CountVectorizer
5. Experiment 2 - Bernoulli NB + Binary BoW
6. Experiment 3 - Complement NB + TF-IDF
7. Comparison Table
8. Tweaks Analysis
9. Key Findings & Recommendations

### 2. New `experiments.py`

Standalone script to run all experiments offline and generate detailed reports.

**Usage:**

```bash
python experiments.py
```

**Output:**

- `results/EXPERIMENT_REPORT.txt` - Full formatted report
- `results/COMPARISON_TABLE.csv` - Results as CSV
- `results/METRICS.json` - All metrics in JSON format

### 3. Updated `frontend.py`

Added `render_tab_experiments()` function with:

- Experiment descriptions and configurations
- Run experiments button
- Interactive results visualization
- Downloadable reports and CSV data
- Detailed analysis of main experiments
- Hyperparameter tweaks comparison

### 4. Updated `app.py`

Added new "Experiments" tab (5th tab) to the Streamlit interface.

## Main Experiments

### Experiment 1: Multinomial NB + CountVectorizer + Basic

- **Model**: Multinomial Naive Bayes
- **Vectorizer**: CountVectorizer
- **Parameters**: max_features=3000, ngram_range=(1,1)
- **Preprocessing**: No stopword removal, no stemming
- **Use Case**: Baseline with basic text features

### Experiment 2: Bernoulli NB + Binary BoW + Stopword Removal

- **Model**: Bernoulli Naive Bayes
- **Vectorizer**: Binary CountVectorizer (binary=True)
- **Parameters**: max_features=3000, ngram_range=(1,1)
- **Preprocessing**: With stopword removal
- **Use Case**: Binary presence/absence features, cleaner vocabulary

### Experiment 3: Complement NB + TF-IDF + Stemming

- **Model**: Complement Naive Bayes (better for imbalanced data)
- **Vectorizer**: TF-IDF Vectorizer
- **Parameters**: max_features=3000, ngram_range=(1,1), sublinear_tf=True
- **Preprocessing**: With stemming
- **Use Case**: Optimized for imbalanced dataset with normalized term frequencies

## Hyperparameter Tweaks

### Vectorizer Tweaks

**Max Features Variation:**

- Tests vocabulary sizes: 500, 3000, 5000
- Measures impact of feature space dimensionality
- Trade-off: More features = better representation but slower training

**NGram Range Variation:**

- Unigrams: `ngram_range=(1,1)` - Single words
- Bigrams: `ngram_range=(1,2)` - Single words + word pairs
- Captures context: "too good to be true" vs individual words

### Model Tweaks

**Alpha (Smoothing) Variation:**

- Values: 0.1, 0.5, 1.0
- Controls Laplace smoothing strength
- Lower alpha = more aggressive smoothing
- Prevents zero probabilities for unseen features

### Preprocessing Tweaks

**Stopword Removal:**

- Common English words: "the", "a", "is", "and", ...
- Reduces noise and vocabulary size
- May lose important context ("good" for HAM, "claim" for SPAM)

**Stemming:**

- Porter Stemmer: "running" → "run", "classification" → "classif"
- Reduces vocabulary but groups related forms
- May lose semantic differences

## Usage

### Option 1: Web UI (Streamlit)

```bash
streamlit run app.py
```

Click the "🧪 Experiments" tab and hit "Run All Experiments" button.

### Option 2: Command Line (Standalone)

```bash
python experiments.py
```

Results saved to `results/` directory.

### Option 3: Python Script

```python
from model import load_data, run_all_experiments, create_comparison_table, generate_report

# Load data
df = load_data()

# Run experiments
all_results = run_all_experiments(df)

# View results
print(create_comparison_table(all_results))

# Get full report
report = generate_report(all_results, df)
print(report)
```

## Results Structure

### Metrics Returned for Each Experiment:

- **Accuracy**: (TP + TN) / Total
- **Precision**: TP / (TP + FP) - False alarm rate
- **Recall**: TP / (TP + FN) - Completeness for spam detection
- **F1-Score**: Harmonic mean of Precision & Recall
- **Confusion Matrix**: [[TN, FP], [FN, TP]]

### Interpretation:

- **High Accuracy** = Model performs well overall
- **High Precision** = Few false positives (legitimate emails not flagged)
- **High Recall** = Few false negatives (spam caught)
- **Balanced F1** = Good compromise between precision and recall

## Dataset

- **Source**: UCI SMS Spam Collection
- **Total Messages**: 5,574
- **Ham (Legitimate)**: 4,825 (86.6%)
- **Spam**: 749 (13.4%)
- **Class Imbalance**: 6.4:1 ratio (more challenging)

## Key Findings

The experiments help answer:

1. Which model works best for SMS spam?
2. Is TF-IDF better than simple word counts?
3. How does preprocessing affect performance?
4. What's the optimal vocabulary size?
5. Do bigrams help or hurt performance?
6. Which smoothing parameter is best?
7. Is stemming beneficial for this task?

## Report Deliverables

Experiments generate three output formats:

### 1. Text Report (`EXPERIMENT_REPORT.txt`)

Full formatted report with all 7 sections, detailed metrics, confusion matrices, and analysis.

### 2. CSV Table (`COMPARISON_TABLE.csv`)

Spreadsheet-ready format for Excel/Google Sheets with all experiments and metrics.

### 3. JSON Metrics (`METRICS.json`)

Machine-readable format with all results for programmatic access.

## Extensibility

To add new experiments:

1. **Add to `run_all_experiments()`**:

```python
all_results['tweaks']['new_experiment'] = run_experiment(
    df,
    model_class=MultinomialNB,
    vectorizer_class=TfidfVectorizer,
    vectorizer_params={...},
    model_params={...},
    remove_stopwords=True,
    apply_stemming=False,
    experiment_name='Your Experiment Name'
)
```

2. **Run and check results**:

```python
comparison_table = create_comparison_table(all_results)
print(comparison_table)
```

## Performance Expectations

On a modern machine:

- **Single Experiment**: 2-5 seconds
- **All Experiments (17 total)**: 1-2 minutes
- **Full Web UI Experiment Run**: 2-3 minutes

## Troubleshooting

**Issue**: Experiments take too long

- Reduce dataset size by filtering in preprocessing
- Use fewer max_features variations
- Skip some tweaks by commenting them out

**Issue**: Memory errors

- Reduce max_features to 1000 or less
- Process data in batches
- Use smaller test set

**Issue**: Different results each time

- Set random_state=42 everywhere (already done)
- Check for caching with Streamlit (`@st.cache_data`)
- Clear cache between runs if needed

## References

- **Naive Bayes**: scikit-learn's MultinomialNB, BernoulliNB, ComplementNB
- **Vectorization**: TF-IDF and CountVectorizer from sklearn
- **Metrics**: Standard classification metrics (Accuracy, Precision, Recall, F1)
- **Dataset**: UCI SMS Spam Collection (Almeida et al., 2011)
