"""
Backend Logic for Prediction and Text Processing
"""
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# Initialize stemmer
stemmer = PorterStemmer()
try:
    stop_words = set(stopwords.words('english'))
except:
    stop_words = set()


def clean_text(text):
    """Clean and preprocess a text string."""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', ' url ', text)
    text = re.sub(r'\d+', ' num ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    tokens = text.split()
    tokens = [stemmer.stem(w) for w in tokens if w not in stop_words and len(w) > 1]
    return ' '.join(tokens)


def get_message_stats(message):
    """Extract statistics from a message."""
    return {
        'num_chars': len(message),
        'num_words': len(message.split()),
        'num_uppercase': sum(c.isupper() for c in message),
        'num_exclamations': message.count('!'),
    }


def predict_message(text, model):
    """Predict if a message is spam using a trained model."""
    cleaned_text = clean_text(text)
    pred = model.predict([cleaned_text])[0]
    
    clf = model.named_steps['clf']
    if hasattr(clf, 'predict_proba'):
        prob = model.predict_proba([cleaned_text])[0]
        spam_prob = prob[1]
        ham_prob = prob[0]
    else:
        spam_prob = float(pred)
        ham_prob = 1 - spam_prob
    
    return {
        'prediction': pred,
        'spam_prob': spam_prob,
        'ham_prob': ham_prob,
        'cleaned_text': cleaned_text,
        'label': 'spam' if pred == 1 else 'ham'
    }


def batch_predict(csv_df, model):
    """Process batch predictions from a DataFrame."""
    batch_df = csv_df.copy()
    
    if 'message' not in batch_df.columns:
        return None, "CSV must contain a 'message' column."
    
    batch_df['cleaned'] = batch_df['message'].apply(clean_text)
    batch_df['prediction'] = model.predict(batch_df['cleaned'])
    batch_df['label'] = batch_df['prediction'].map({0: 'Ham', 1: 'Spam'})
    
    if hasattr(model.named_steps['clf'], 'predict_proba'):
        batch_df['spam_prob'] = model.predict_proba(batch_df['cleaned'])[:, 1]
    
    return batch_df, None


def create_wordcloud(texts, colormap='viridis'):
    """Create a wordcloud figure from a list of texts."""
    text = ' '.join(texts)
    wc = WordCloud(
        width=700, height=300, background_color='#111827',
        colormap=colormap, max_words=100,
        collocations=False, prefer_horizontal=0.9
    ).generate(text)
    
    fig, ax = plt.subplots(figsize=(7, 3))
    fig.patch.set_facecolor('#111827')
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout(pad=0)
    return fig


def get_top_words(texts, n=15):
    """Extract top n most common words from texts."""
    all_words = ' '.join(texts).split()
    return Counter(all_words).most_common(n)
