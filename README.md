# 🛡️ SpamGuard — SMS Spam Classifier

A production-grade Streamlit web app for SMS spam classification using NLP and multiple ML models.

---

## 📦 Dataset

**Name:** UCI SMS Spam Collection Dataset  
**Source:** [UCI ML Repository](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)  
**Kaggle Mirror:** [https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset)

### Download Instructions

**Option A — Kaggle (Recommended):**

1. Go to https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset
2. Click **Download** (requires free Kaggle account)
3. Extract `spam.csv` to the project folder

**Option B — UCI Repository (Auto-loaded):**
The app automatically fetches the dataset from the UCI ML Repository at runtime.
No manual download needed if you have internet access.

**Option C — Kaggle CLI:**

```bash
pip install kaggle
kaggle datasets download -d uciml/sms-spam-collection-dataset
unzip sms-spam-collection-dataset.zip
```

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

| Tab            | Contents                                                                                               |
| -------------- | ------------------------------------------------------------------------------------------------------ |
| 🔍 EDA         | Class distribution, char length histograms, box plots, word clouds, top-word bar charts                |
| ⚙️ Pipeline    | Preprocessing steps, feature engineering table, TF-IDF parameters, train/test split info               |
| 🎯 Predict     | Single-message classifier, confidence gauge, message stats, batch CSV upload                           |
| 📊 Metrics     | Model comparison table, bar charts, confusion matrix, ROC curve, classification report                 |
| 🧪 Experiments | **NEW:** Comprehensive ML experimentation framework with 3 main experiments + 14 hyperparameter tweaks |

---

## 🧪 NEW: Comprehensive Experiments Framework

The app now includes a complete experimentation framework for systematic model comparison:

### Main Experiments (3)

1. **Multinomial NB + CountVectorizer + Basic** - Baseline approach
2. **Bernoulli NB + Binary BoW + Stopword Removal** - Binary features with preprocessing
3. **Complement NB + TF-IDF + Stemming** - Optimized for imbalanced data

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

| Model               | Notes                               |
| ------------------- | ----------------------------------- |
| Multinomial NB      | Fast baseline, good for word counts |
| Bernoulli NB        | Binary features, presence/absence   |
| Complement NB       | Better for imbalanced datasets      |
| Logistic Regression | Interpretable, competitive baseline |
| Linear SVM          | High precision spam detection       |
| Random Forest       | Ensemble, robust to overfitting     |

---

## 📁 Project Structure

```
spam_classifier/
├── app.py              ← Main Streamlit application
├── requirements.txt    ← Python dependencies
└── README.md           ← This file
```

---

## 📚 Report Checklist (Submission)

- [x] **EDA Findings**: Class imbalance (87% ham / 13% spam), spam messages are ~3× longer, use more digits, capitals, and promotional language
- [x] **Model Choice Justification**: Multinomial NB is the classic baseline for bag-of-words text; LR adds regularization; LinearSVC maximizes margin; RF adds ensemble power
- [x] **Preprocessing Pipeline**: Lowercase → URL normalization → digit removal → stopword removal → Porter stemming → TF-IDF (unigrams + bigrams)
- [x] **Metrics Summary**: All 4 models achieve >97% accuracy; F1 scores reported per class; confusion matrix and ROC curve available per model

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
