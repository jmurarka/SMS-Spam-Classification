# 🛡️ SpamGuard — SMS Spam Classifier

A production-grade Streamlit web app for SMS spam classification using Naive Bayes models with TF-IDF text preprocessing.

---

## 📦 Dataset

**UCI SMS Spam Collection Dataset**  
Source: [UCI ML Repository](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)

The dataset is included in the project structure at `data/SMSSpamCollection`

---

## 🚀 Setup & Run

```bash
# 1. Clone / copy project folder
cd spam_classifier

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

App will open at: **http://localhost:8501**

---

## 📋 Features

| Tab            | Contents                                                                                      |
| -------------- | --------------------------------------------------------------------------------------------- |
| 🔍 EDA         | Class distribution, char length histograms, box plots, word clouds, top-word bar charts       |
| 🎯 Predict     | Single-message classifier, confidence gauge, message stats, batch CSV upload                  |
| 📊 Metrics     | Model comparison table, bar charts, confusion matrix, ROC curve, classification report        |
| 🧪 Experiments | Comprehensive ML experimentation framework with 3 main experiments + 14 hyperparameter tweaks |

---

## 🧪 NEW: Comprehensive Experiments Framework

The app now includes a complete experimentation framework for systematic model comparison:

### Main Experiments (3)

1. **Multinomial NB + TF-IDF + Basic** - Baseline with word frequency weighting
2. **Gaussian NB + TF-IDF + Dense Conversion** - Dense matrix transformation for Gaussian
3. **Bernoulli NB + TF-IDF + Alpha Smoothing** - Binary feature support with smoothing

### Hyperparameter Tweaks (14)

- **Vectorizer**: max_features (500, 3000, 5000) + ngram_range (1,1 vs 1,2)
- **Model**: alpha smoothing (0.1, 0.5, 1.0)
- **Preprocessing**: with/without stopwords + with/without stemming

### Deliverables

- Accuracy, Precision, Recall, F1-Score for each experiment
- Confusion matrices for all configurations
- Comparison table with all metrics
- Downloadable reports (TXT, CSV, JSON)

👉 **See [EXPERIMENTS.md](EXPERIMENTS.md) for detailed guide**

---

## 🤖 Models

| Model          | Notes                                    |
| -------------- | ---------------------------------------- |
| Multinomial NB | Fast baseline, optimized for word counts |
| Gaussian NB    | Converts sparse TF-IDF to dense features |
| Bernoulli NB   | Binary feature support, alpha-smoothing  |

---

## 📁 Project Structure

```
SMS-Spam-Classification/
├── app.py                      ← Main Streamlit application (entry point)
├── model.py                    ← ML models & training logic
├── backend.py                  ← Backend utilities & analytics
├── experiments.py              ← Experimentation framework
├── requirements.txt            ← Python dependencies
├── README.md                   ← This file
├── EXPERIMENTS.md              ← Detailed experiments guide
│
├── data/
│   └── SMSSpamCollection       ← UCI SMS Spam Collection dataset
│
└── frontend/                   ← UI components package
    ├── __init__.py             ← Module exports
    ├── styles.py               ← Page config & global CSS
    ├── common.py               ← Sidebar & hero banner
    ├── eda.py                  ← Exploratory Data Analysis tab
    ├── predict.py              ← Prediction tab
    ├── metrics.py              ← Model metrics tab
    ├── experiments.py          ← Experiments framework tab
    └── README.md               ← Frontend documentation
```

---

## 📚 Report Checklist (Submission)

- [x] **EDA Findings**: Class imbalance (87% ham / 13% spam), spam messages are ~3× longer, use more digits, capitals, and promotional language
- [x] **Model Choice Justification**: Three Naive Bayes variants for robust text classification - Multinomial NB for word frequencies, Gaussian NB for dense features, Bernoulli NB for binary presence/absence
- [x] **Preprocessing Pipeline**: Lowercase → URL normalization → digit removal → stopword removal → Porter stemming → TF-IDF (unigrams + bigrams)
- [x] **Metrics Summary**: All 3 models achieve >95% accuracy; F1 scores reported per class; confusion matrix and ROC curve available per model

---

## 📌 Rules Compliance

| Rule                    | Status                      |
| ----------------------- | --------------------------- |
| No GitHub clones        | ✅ Built from scratch       |
| No AutoML tools         | ✅ Manual sklearn pipeline  |
| No pre-trained weights  | ✅ Trained on dataset only  |
| Dataset from Kaggle/UCI | ✅ UCI SMS Spam Collection  |
| sklearn.pipeline used   | ✅ `Pipeline([tfidf, clf])` |
| Explainable code        | ✅ Every line documented    |
