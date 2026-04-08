"""
ML Model Training and Comprehensive Experimentation Framework
"""
import pandas as pd
import numpy as np
import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB, ComplementNB
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import warnings
warnings.filterwarnings('ignore')

# Download NLTK resources quietly
for resource in ['stopwords', 'punkt', 'punkt_tab']:
    try:
        nltk.download(resource, quiet=True)
    except:
        pass


@st.cache_data(show_spinner=False)
def load_data():
    """Load SMS Spam Collection dataset from data folder."""
    import os
    
    data_file = os.path.join("data", "SMSSpamCollection")
    
    if not os.path.exists(data_file):
        st.error(f"❌ Unsuccessful to get the data")
        st.error(f"Dataset file not found at: {data_file}")
        st.error("Please ensure SMSSpamCollection file exists in the data folder.")
        raise FileNotFoundError(f"Dataset not found at {data_file}")
    
    try:
        df = pd.read_csv(data_file, sep='\t', header=None, names=['label', 'message'],
                         encoding='latin-1')
        st.info(f"✅ Loaded {len(df):,} messages from data/SMSSpamCollection")
        return df
    except Exception as e:
        st.error(f"❌ Error loading dataset: {str(e)}")
        raise


def preprocess_text(text, remove_stopwords=True, apply_stemming=True):
    """
    Clean and preprocess text with flexible options.
    
    Args:
        text: Input text
        remove_stopwords: Whether to remove stopwords
        apply_stemming: Whether to apply stemming
    """
    stemmer = PorterStemmer()
    try:
        stop_words = set(stopwords.words('english')) if remove_stopwords else set()
    except:
        stop_words = set()
    
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', ' url ', text)
    text = re.sub(r'\d+', ' num ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    
    tokens = text.split()
    if apply_stemming:
        tokens = [stemmer.stem(w) for w in tokens if w not in stop_words and len(w) > 1]
    else:
        tokens = [w for w in tokens if w not in stop_words and len(w) > 1]
    
    return ' '.join(tokens)


@st.cache_data(show_spinner=False)
def preprocess_data(df, remove_stopwords=True, apply_stemming=True):
    """Preprocess SMS data with feature engineering and flexible text cleaning."""
    df = df.copy()
    df['label_enc'] = (df['label'] == 'spam').astype(int)

    # Feature engineering
    df['num_chars']    = df['message'].str.len()
    df['num_words']    = df['message'].str.split().str.len()
    df['num_sentences']= df['message'].str.count(r'[.!?]+') + 1
    df['num_digits']   = df['message'].str.count(r'\d')
    df['num_upper']    = df['message'].str.count(r'[A-Z]')
    df['has_url']      = df['message'].str.contains(r'http|www|\.com', case=False, regex=True).astype(int)
    df['has_phone']    = df['message'].str.contains(r'\d{5,}', regex=True).astype(int)
    df['has_currency'] = df['message'].str.contains(r'£|\$|€|free|win|prize|claim', case=False, regex=True).astype(int)
    df['exclamations'] = df['message'].str.count(r'!')
    df['capitals_ratio'] = df['num_upper'] / (df['num_chars'] + 1)

    df['cleaned'] = df['message'].apply(
        lambda x: preprocess_text(x, remove_stopwords=remove_stopwords, apply_stemming=apply_stemming)
    )
    return df


@st.cache_resource(show_spinner=False)
def train_models(df):
    """Train multiple classification models."""
    X = df['cleaned']
    y = df['label_enc']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Helper function to convert sparse to dense
    def sparse_to_dense(X):
        return X.toarray()
    
    models = {
        "Multinomial NB": Pipeline([
            ('tfidf', TfidfVectorizer(max_features=8000, ngram_range=(1,2), sublinear_tf=True, min_df=2)),
            ('clf', MultinomialNB(alpha=0.1))
        ]),
        "Gaussian NB": Pipeline([
            ('tfidf', TfidfVectorizer(max_features=8000, ngram_range=(1,2), sublinear_tf=True, min_df=2)),
            ('converter', FunctionTransformer(sparse_to_dense)),
            ('clf', GaussianNB())
        ]),
        "Bernoulli NB": Pipeline([
            ('tfidf', TfidfVectorizer(max_features=8000, ngram_range=(1,2), sublinear_tf=True, min_df=2)),
            ('clf', BernoulliNB(alpha=0.1))
        ]),
    }

    results = {}
    trained = {}
    for name, pipe in models.items():
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        y_prob = pipe.predict_proba(X_test)[:,1] if hasattr(pipe.named_steps['clf'], 'predict_proba') else None

        results[name] = {
            'accuracy':  accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall':    recall_score(y_test, y_pred, zero_division=0),
            'f1':        f1_score(y_test, y_pred, zero_division=0),
            'cm':        confusion_matrix(y_test, y_pred),
            'y_pred':    y_pred,
            'y_prob':    y_prob,
            'y_test':    y_test.values,
            'report':    classification_report(y_test, y_pred, target_names=['Ham','Spam'])
        }
        trained[name] = pipe

    return trained, results, X_test, y_test


# ============================================================================
# COMPREHENSIVE EXPERIMENTATION FRAMEWORK
# ============================================================================

def run_experiment(df, model_class, vectorizer_class, vectorizer_params, model_params, 
                   remove_stopwords, apply_stemming, experiment_name):
    """
    Run a single experiment with specified configuration.
    
    Returns:
        dict: Results including metrics and confusion matrix
    """
    # Preprocess data with specific options
    processed_df = preprocess_data(df, remove_stopwords=remove_stopwords, apply_stemming=apply_stemming)
    
    X = processed_df['cleaned']
    y = processed_df['label_enc']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Build pipeline
    def sparse_to_dense(X):
        return X.toarray() if hasattr(X, 'toarray') else X
    
    pipeline = Pipeline([
        ('vectorizer', vectorizer_class(**vectorizer_params)),
        ('clf', model_class(**model_params))
    ])
    
    # Check if we need to convert to dense (for GaussianNB)
    if model_class == GaussianNB:
        pipeline = Pipeline([
            ('vectorizer', vectorizer_class(**vectorizer_params)),
            ('converter', FunctionTransformer(sparse_to_dense)),
            ('clf', model_class(**model_params))
        ])
    
    # Train
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)
    
    return {
        'experiment_name': experiment_name,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'confusion_matrix': cm,
        'model': pipeline,
        'X_test': X_test,
        'y_test': y_test,
        'y_pred': y_pred
    }


def run_all_experiments(df):
    """
    Run all experiments: 3 main experiments + tweaks.
    
    Returns:
        dict: Results organized by experiment
    """
    all_results = {
        'main_experiments': {},
        'tweaks': {}
    }
    
    # ========================================================================
    # MAIN EXPERIMENTS (3)
    # ========================================================================
    
    # Experiment 1: Multinomial NB + CountVectorizer + Basic Preprocessing
    print("Running Experiment 1: Multinomial NB + CountVectorizer + Basic Preprocessing...")
    all_results['main_experiments']['Exp1_MultinomialNB_CountVect_Basic'] = run_experiment(
        df,
        model_class=MultinomialNB,
        vectorizer_class=CountVectorizer,
        vectorizer_params={'max_features': 3000, 'ngram_range': (1, 1)},
        model_params={'alpha': 1.0},
        remove_stopwords=False,
        apply_stemming=False,
        experiment_name='Multinomial NB + CountVectorizer + Basic'
    )
    
    # Experiment 2: Bernoulli NB + Binary BoW + Stopword Removal
    print("Running Experiment 2: Bernoulli NB + Binary BoW + Stopword Removal...")
    all_results['main_experiments']['Exp2_BernoulliNB_BinaryBoW_Stopword'] = run_experiment(
        df,
        model_class=BernoulliNB,
        vectorizer_class=CountVectorizer,
        vectorizer_params={'max_features': 3000, 'ngram_range': (1, 1), 'binary': True},
        model_params={'alpha': 1.0},
        remove_stopwords=True,
        apply_stemming=False,
        experiment_name='Bernoulli NB + Binary BoW + Stopword Removal'
    )
    
    # Experiment 3: Complement NB + TF-IDF + Stemming
    print("Running Experiment 3: Complement NB + TF-IDF + Stemming...")
    all_results['main_experiments']['Exp3_ComplementNB_TFIDF_Stemming'] = run_experiment(
        df,
        model_class=ComplementNB,
        vectorizer_class=TfidfVectorizer,
        vectorizer_params={'max_features': 3000, 'ngram_range': (1, 1), 'sublinear_tf': True},
        model_params={'alpha': 1.0},
        remove_stopwords=False,
        apply_stemming=True,
        experiment_name='Complement NB + TF-IDF + Stemming'
    )
    
    # ========================================================================
    # TWEAKS - VECTORIZER: max_features variations
    # ========================================================================
    for max_feat in [500, 3000, 5000]:
        print(f"Running tweak: Multinomial NB with max_features={max_feat}...")
        key = f'Tweak_MaxFeatures_{max_feat}'
        all_results['tweaks'][key] = run_experiment(
            df,
            model_class=MultinomialNB,
            vectorizer_class=TfidfVectorizer,
            vectorizer_params={'max_features': max_feat, 'ngram_range': (1, 1)},
            model_params={'alpha': 1.0},
            remove_stopwords=False,
            apply_stemming=False,
            experiment_name=f'Multinomial NB + TF-IDF (max_features={max_feat})'
        )
    
    # ========================================================================
    # TWEAKS - VECTORIZER: ngram_range variations
    # ========================================================================
    for ngram in [(1, 1), (1, 2)]:
        print(f"Running tweak: Multinomial NB with ngram_range={ngram}...")
        key = f'Tweak_Ngram_{ngram[0]}_{ngram[1]}'
        all_results['tweaks'][key] = run_experiment(
            df,
            model_class=MultinomialNB,
            vectorizer_class=TfidfVectorizer,
            vectorizer_params={'max_features': 3000, 'ngram_range': ngram},
            model_params={'alpha': 1.0},
            remove_stopwords=False,
            apply_stemming=False,
            experiment_name=f'Multinomial NB + TF-IDF (ngram_range={ngram})'
        )
    
    # ========================================================================
    # TWEAKS - MODEL: alpha (smoothing) variations
    # ========================================================================
    for alpha in [0.1, 0.5, 1.0]:
        print(f"Running tweak: Multinomial NB with alpha={alpha}...")
        key = f'Tweak_Alpha_{str(alpha).replace(".", "_")}'
        all_results['tweaks'][key] = run_experiment(
            df,
            model_class=MultinomialNB,
            vectorizer_class=TfidfVectorizer,
            vectorizer_params={'max_features': 3000, 'ngram_range': (1, 1)},
            model_params={'alpha': alpha},
            remove_stopwords=False,
            apply_stemming=False,
            experiment_name=f'Multinomial NB + TF-IDF (alpha={alpha})'
        )
    
    # ========================================================================
    # TWEAKS - PREPROCESSING: Stopwords variation
    # ========================================================================
    for use_stopwords in [False, True]:
        label = "WithStopwords" if use_stopwords else "WithoutStopwords"
        print(f"Running tweak: Multinomial NB {label}...")
        key = f'Tweak_Stopwords_{label}'
        all_results['tweaks'][key] = run_experiment(
            df,
            model_class=MultinomialNB,
            vectorizer_class=TfidfVectorizer,
            vectorizer_params={'max_features': 3000, 'ngram_range': (1, 1)},
            model_params={'alpha': 1.0},
            remove_stopwords=use_stopwords,
            apply_stemming=False,
            experiment_name=f'Multinomial NB + TF-IDF ({label})'
        )
    
    # ========================================================================
    # TWEAKS - PREPROCESSING: Stemming variation
    # ========================================================================
    for use_stemming in [False, True]:
        label = "WithStemming" if use_stemming else "WithoutStemming"
        print(f"Running tweak: Multinomial NB {label}...")
        key = f'Tweak_Stemming_{label}'
        all_results['tweaks'][key] = run_experiment(
            df,
            model_class=MultinomialNB,
            vectorizer_class=TfidfVectorizer,
            vectorizer_params={'max_features': 3000, 'ngram_range': (1, 1)},
            model_params={'alpha': 1.0},
            remove_stopwords=False,
            apply_stemming=use_stemming,
            experiment_name=f'Multinomial NB + TF-IDF ({label})'
        )
    
    return all_results


def create_comparison_table(all_results):
    """
    Create a comparison table of all experiments.
    
    Returns:
        pd.DataFrame: Comparison table with all metrics
    """
    rows = []
    
    # Main experiments
    for key, result in all_results['main_experiments'].items():
        rows.append({
            'Experiment': result['experiment_name'],
            'Type': 'Main Experiment',
            'Accuracy': f"{result['accuracy']:.4f}",
            'Precision': f"{result['precision']:.4f}",
            'Recall': f"{result['recall']:.4f}",
            'F1-Score': f"{result['f1']:.4f}"
        })
    
    # Tweaks
    for key, result in all_results['tweaks'].items():
        rows.append({
            'Experiment': result['experiment_name'],
            'Type': 'Tweak',
            'Accuracy': f"{result['accuracy']:.4f}",
            'Precision': f"{result['precision']:.4f}",
            'Recall': f"{result['recall']:.4f}",
            'F1-Score': f"{result['f1']:.4f}"
        })
    
    return pd.DataFrame(rows)


def generate_report(all_results, df):
    """
    Generate comprehensive report with the required structure.
    
    Returns:
        str: Formatted report
    """
    report = []
    report.append("="*80)
    report.append("SMS SPAM CLASSIFICATION - COMPREHENSIVE EXPERIMENTATION REPORT")
    report.append("="*80)
    report.append("")
    
    # 1. INTRODUCTION
    report.append("1. INTRODUCTION")
    report.append("-" * 80)
    report.append("""
This report presents a comprehensive experimental analysis of machine learning models
for SMS spam classification. We evaluate three different Naive Bayes variants with
various vectorization techniques and preprocessing strategies. Additionally, we conduct
systematic tweaks on key hyperparameters to identify the optimal configuration.

Objective: Determine the best combination of model, vectorizer, and preprocessing 
technique for accurate spam classification.
    """)
    report.append("")
    
    # 2. DATASET OVERVIEW
    report.append("2. DATASET OVERVIEW")
    report.append("-" * 80)
    spam_count = (df['label'] == 'spam').sum()
    ham_count = (df['label'] == 'ham').sum()
    total = len(df)
    
    report.append(f"Total Messages: {total:,}")
    report.append(f"Ham Messages: {ham_count:,} ({ham_count/total*100:.1f}%)")
    report.append(f"Spam Messages: {spam_count:,} ({spam_count/total*100:.1f}%)")
    report.append(f"Class Imbalance Ratio (Ham:Spam): {ham_count/spam_count:.2f}:1")
    report.append("")
    
    # 3. PREPROCESSING STEPS
    report.append("3. PREPROCESSING STEPS")
    report.append("-" * 80)
    report.append("""
The preprocessing pipeline includes:

1. Text Normalization:
   - Convert to lowercase
   - Remove special characters
   - Replace URLs with placeholder 'url'
   - Replace numbers with placeholder 'num'

2. Tokenization:
   - Split text into words
   - Remove tokens shorter than 2 characters

3. Optional Processing:
   - Stopword Removal: Remove common English words
   - Stemming: Apply Porter Stemmer for word normalization

Feature Engineering:
   - Number of characters, words, sentences
   - Count of digits, uppercase letters
   - Presence of URLs, phone numbers, currency keywords
   - Ratio of uppercase to total characters
    """)
    report.append("")
    
    # 4, 5, 6. MAIN EXPERIMENTS
    exp_names = {
        'Exp1_MultinomialNB_CountVect_Basic': '4. EXPERIMENT 1 — Multinomial NB + CountVectorizer',
        'Exp2_BernoulliNB_BinaryBoW_Stopword': '5. EXPERIMENT 2 — Bernoulli NB + Binary BoW',
        'Exp3_ComplementNB_TFIDF_Stemming': '6. EXPERIMENT 3 — Complement NB + TF-IDF'
    }
    
    for exp_key, exp_title in exp_names.items():
        result = all_results['main_experiments'][exp_key]
        report.append(exp_title)
        report.append("-" * 80)
        report.append(f"Configuration: {result['experiment_name']}")
        report.append("")
        
        # Metrics
        report.append("Performance Metrics:")
        report.append(f"  Accuracy:  {result['accuracy']:.4f}")
        report.append(f"  Precision: {result['precision']:.4f}")
        report.append(f"  Recall:    {result['recall']:.4f}")
        report.append(f"  F1-Score:  {result['f1']:.4f}")
        report.append("")
        
        # Confusion Matrix
        cm = result['confusion_matrix']
        report.append("Confusion Matrix:")
        report.append(f"  True Negatives:  {cm[0, 0]:5d} | False Positives: {cm[0, 1]:5d}")
        report.append(f"  False Negatives: {cm[1, 0]:5d} | True Positives:  {cm[1, 1]:5d}")
        report.append("")
    
    # 7. COMPARISON TABLE
    report.append("7. COMPARISON TABLE")
    report.append("-" * 80)
    comparison_df = create_comparison_table(all_results)
    report.append(comparison_df.to_string(index=False))
    report.append("")
    
    # TWEAKS SUMMARY
    report.append("="*80)
    report.append("TWEAKS - DETAILED ANALYSIS")
    report.append("="*80)
    report.append("")
    
    # Max Features Tweaks
    report.append("Max Features Comparison (500 vs 3000 vs 5000):")
    report.append("-" * 80)
    for max_feat in [500, 3000, 5000]:
        key = f'Tweak_MaxFeatures_{max_feat}'
        result = all_results['tweaks'][key]
        report.append(f"max_features={max_feat}: Accuracy={result['accuracy']:.4f}, F1={result['f1']:.4f}")
    report.append("")
    
    # NGram Tweaks
    report.append("NGram Range Comparison (Unigrams vs Bigrams):")
    report.append("-" * 80)
    ngram_keys = [k for k in all_results['tweaks'].keys() if 'Ngram' in k]
    for key in sorted(ngram_keys):
        result = all_results['tweaks'][key]
        report.append(f"{result['experiment_name']}: Accuracy={result['accuracy']:.4f}, F1={result['f1']:.4f}")
    report.append("")
    
    # Alpha Tweaks
    report.append("Alpha (Smoothing) Comparison (0.1 vs 0.5 vs 1.0):")
    report.append("-" * 80)
    for alpha in [0.1, 0.5, 1.0]:
        key = f'Tweak_Alpha_{str(alpha).replace(".", "_")}'
        result = all_results['tweaks'][key]
        report.append(f"alpha={alpha}: Accuracy={result['accuracy']:.4f}, F1={result['f1']:.4f}")
    report.append("")
    
    # Stopwords Tweaks
    report.append("Stopword Removal Comparison:")
    report.append("-" * 80)
    for label in ['WithoutStopwords', 'WithStopwords']:
        key = f'Tweak_Stopwords_{label}'
        result = all_results['tweaks'][key]
        report.append(f"{label}: Accuracy={result['accuracy']:.4f}, F1={result['f1']:.4f}")
    report.append("")
    
    # Stemming Tweaks
    report.append("Stemming Comparison:")
    report.append("-" * 80)
    for label in ['WithoutStemming', 'WithStemming']:
        key = f'Tweak_Stemming_{label}'
        result = all_results['tweaks'][key]
        report.append(f"{label}: Accuracy={result['accuracy']:.4f}, F1={result['f1']:.4f}")
    report.append("")
    
    # KEY FINDINGS
    report.append("="*80)
    report.append("KEY FINDINGS & RECOMMENDATIONS")
    report.append("="*80)
    
    # Find best experiment
    all_scores = {}
    for exp_key, result in all_results['main_experiments'].items():
        all_scores[result['experiment_name']] = result['f1']
    for exp_key, result in all_results['tweaks'].items():
        all_scores[result['experiment_name']] = result['f1']
    
    best_exp = max(all_scores.items(), key=lambda x: x[1])
    report.append(f"Best Performing Configuration: {best_exp[0]}")
    report.append(f"Best F1-Score: {best_exp[1]:.4f}")
    report.append("")
    
    report.append("="*80)
    
    return "\n".join(report)
