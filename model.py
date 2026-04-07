"""
ML Model Training and Utilities
"""
import pandas as pd
import numpy as np
import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)

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
@st.cache_data(show_spinner=False)
def preprocess_data(df):
    """Preprocess SMS data with feature engineering."""
    stemmer = PorterStemmer()
    try:
        stop_words = set(stopwords.words('english'))
    except:
        stop_words = set()

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

    def clean_text(text):
        text = text.lower()
        text = re.sub(r'http\S+|www\S+', ' url ', text)
        text = re.sub(r'\d+', ' num ', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        tokens = text.split()
        tokens = [stemmer.stem(w) for w in tokens if w not in stop_words and len(w) > 1]
        return ' '.join(tokens)

    df['cleaned'] = df['message'].apply(clean_text)
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
