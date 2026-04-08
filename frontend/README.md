# Frontend Module - Modular Structure Guide

## Overview

The frontend code has been refactored into a modular, organized structure with separate files for each component. This makes the codebase more maintainable, debuggable, and scalable.

## Directory Structure

```
frontend/
├── __init__.py          ← Centralized exports
├── styles.py            ← Page config & CSS styling
├── common.py            ← Sidebar & hero banner
├── eda.py               ← Tab 1: Exploratory Data Analysis
├── pipeline.py          ← Tab 2: Preprocessing Pipeline
├── predict.py           ← Tab 3: Real-time Prediction
├── metrics.py           ← Tab 4: Model Metrics Analysis
├── experiments.py       ← Tab 5: Experiments Framework
└── README.md            ← This file
```

## Module Details

### 1. **styles.py** - Page Configuration & Styling

**Exports:**

- `set_page_config()` - Configures Streamlit page settings
- `apply_custom_css()` - Applies dark theme CSS

**Purpose:** Centralizes all appearance and configuration settings

**Key Classes/Variables:**

- CSS variables (colors, fonts, spacing)
- Responsive design classes
- Dark theme color palette

---

### 2. **common.py** - Sidebar & Hero Banner

**Exports:**

- `render_sidebar(df, models_list)` - Renders the sidebar with dataset info and models list
- `render_hero()` - Renders the main hero banner

**Purpose:** Common, reusable UI components used across tabs

**Components:**

- Logo and branding
- Dataset statistics display
- Model list
- Project rules/guidelines

---

### 3. **eda.py** - Exploratory Data Analysis Tab

**Exports:**

- `render_tab_eda(df)` - Renders the complete EDA tab

**Purpose:** Displays comprehensive data exploration and analysis

**Visualizations:**

- Class distribution pie chart
- Character length histogram
- Feature box plots (Characters, Words, Digits, Ratio)
- Word clouds (Ham vs Spam)
- Top 15 words bar charts
- Sample message tables

**Dependencies:** `plotly`, `backend.create_wordcloud`, `backend.get_top_words`

---

### 4. **pipeline.py** - Preprocessing Pipeline Tab

**Exports:**

- `render_tab_pipeline(df)` - Renders pipeline documentation and feature engineering info

**Purpose:** Explains the text preprocessing and feature engineering process

**Sections:**

- Text cleaning steps (ASCII art pipeline)
- Feature engineering table (10 features with descriptions)
- TF-IDF parameters explanation
- Train/test split ratios

**Note:** Educational/informational tab - no calculations here

---

### 5. **predict.py** - Real-time SMS Prediction Tab

**Exports:**

- `render_tab_predict(trained_models)` - Renders prediction interface

**Purpose:** Allows users to classify messages in real-time

**Features:**

- Text input area for manual message entry
- Example message selector
- Model selection dropdown
- Classification button
- Confidence gauge (Plotly indicator)
- Message statistics display (characters, words, uppercase, exclamations)
- Batch CSV upload for bulk predictions

**Dependencies:** `backend.predict_message`, `backend.batch_predict`

---

### 6. **metrics.py** - Model Performance Analysis Tab

**Exports:**

- `render_tab_metrics(results)` - Renders model comparison and detailed analysis

**Purpose:** Displays comprehensive model performance metrics

**Visualizations:**

- Metrics summary table (Accuracy, Precision, Recall, F1)
- Grouped bar chart comparison
- Confusion matrix heatmap
- ROC/AUC curve
- Classification report
- Per-model metric cards

**Dependencies:** `sklearn.metrics.roc_curve`, `sklearn.metrics.roc_auc_score`

---

### 7. **experiments.py** - Comprehensive Experiments Tab

**Exports:**

- `render_tab_experiments(df)` - Renders experiments framework

**Purpose:** Runs systematic ML experiments with various configurations

**Main Components:**

- Experiment descriptions (3 main experiments)
- Hyperparameter tweaks explanation
- "Run All Experiments" button
- Results display with:
  - Comparison table
  - Main experiment details (3 tabs)
  - Hyperparameter tweak analysis (5 tabs)
  - Full report download

**Helper Functions:**

- `_display_experiment_results()` - Orchestrates results display
- `_display_main_experiment_details()` - Shows main experiment metrics
- `_display_tweaks_analysis()` - Shows hyperparameter tweak comparisons

**Dependencies:** `model.run_all_experiments`, `model.create_comparison_table`, `model.generate_report`

---

### 8. ****init**.py** - Module Exports

**Purpose:** Centralizes all imports so app.py can import everything cleanly

**Pattern:**

```python
from frontend import (
    set_page_config,
    apply_custom_css,
    render_sidebar,
    render_hero,
    render_tab_eda,
    render_tab_pipeline,
    render_tab_predict,
    render_tab_metrics,
    render_tab_experiments
)
```

---

## Usage in app.py

The main application imports and uses the modular components:

```python
from frontend import (
    set_page_config,
    apply_custom_css,
    render_sidebar,
    render_hero,
    render_tab_eda,
    render_tab_pipeline,
    render_tab_predict,
    render_tab_metrics,
    render_tab_experiments
)

# Configure page
set_page_config()
apply_custom_css()

# Load data and train models
df = preprocess_data(load_data())
trained_models, results, ... = train_models(df)

# Render UI
render_sidebar(df, list(trained_models.keys()))
render_hero()

# Render tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([...])
with tab1: render_tab_eda(df)
with tab2: render_tab_pipeline(df)
with tab3: render_tab_predict(trained_models)
with tab4: render_tab_metrics(results)
with tab5: render_tab_experiments(df)
```

---

## Debugging Guide

### How to Debug Individual Tabs

1. **EDA issues?** → Check `frontend/eda.py`
   - Visualizations: plotly figures
   - Data processing: wordcloud generation
   - Check `backend.py` for helper functions

2. **Pipeline info incorrect?** → Check `frontend/pipeline.py`
   - Feature engineering table
   - TF-IDF parameter explanations
   - No dependencies needed

3. **Prediction not working?** → Check `frontend/predict.py`
   - User input handling
   - Model selection logic
   - Check `backend.predict_message()` function

4. **Metrics display errors?** → Check `frontend/metrics.py`
   - ROC curve generation
   - Confusion matrix heatmap
   - Classification report parsing

5. **Experiments failing?** → Check `frontend/experiments.py`
   - Check `model.run_all_experiments()`
   - Check data preprocessing in `model.py`
   - Log output from `_display_experiment_results()`

### Adding New Features

To add a new tab:

1. **Create** `frontend/newtab.py`:

   ```python
   def render_tab_newtab(data):
       st.markdown("...")
       # Your code here
   ```

2. **Export** from `frontend/__init__.py`:

   ```python
   from frontend.newtab import render_tab_newtab
   __all__ = [..., 'render_tab_newtab']
   ```

3. **Use** in `app.py`:
   ```python
   from frontend import render_tab_newtab
   tab6 = st.tabs([..., "New Tab"])
   with tab6: render_tab_newtab(data)
   ```

---

## Styling Constants

**Color Palette** (defined in `styles.py`):

- `--bg`: `#0a0e1a` (Dark background)
- `--surface`: `#111827` (Card background)
- `--accent`: `#00f5a0` (Green accent)
- `--accent2`: `#00d9f5` (Cyan accent)
- `--danger`: `#ff4d6d` (Red for spam)
- `--warn`: `#ffd166` (Yellow for warning)
- `--text`: `#e2e8f0` (Light text)
- `--muted`: `#64748b` (Gray for secondary text)
- `--border`: `#1e293b` (Border color)

**CSS Classes** Available:

- `.metric-card` - Card component with gradient top border
- `.section-header` - Section title with trailing line
- `.hero-banner` - Main hero banner with gradient
- `.pred-spam` / `.pred-ham` - Prediction result boxes
- `.info-pill` - Small badge/pill component

---

## Dependencies Per Module

| Module         | Dependencies                       |
| -------------- | ---------------------------------- |
| styles.py      | streamlit                          |
| common.py      | streamlit                          |
| eda.py         | streamlit, pandas, plotly, backend |
| pipeline.py    | streamlit, pandas                  |
| predict.py     | streamlit, pandas, plotly, backend |
| metrics.py     | streamlit, pandas, plotly, sklearn |
| experiments.py | streamlit, pandas, plotly, model   |

---

## Migration Notes

**Old Structure:**

- Single `frontend.py` with 1000+ lines
- All tabs mixed together

**New Structure:**

- One file per logical component
- Clear separation of concerns
- Easier to test and debug
- Better code organization

**No Breaking Changes:**

- `app.py` imports remain the same
- All functionality preserved
- Same UI/UX experience

---

## Performance Tips

1. **Use Streamlit caching** for expensive operations
2. **Cache data** in app.py (already done)
3. **Lazy load** visualizations if they're heavy
4. **Avoid redundant imports** - use `__init__.py`
5. **Profile slow tabs** individually

---

## Future Enhancements

- [ ] Add unit tests for each tab
- [ ] Create tab-specific test files
- [ ] Add type hints throughout
- [ ] Create component library (reusable parts)
- [ ] Add logging for debugging
- [ ] Create separate `utils.py` for shared functions
- [ ] Add docstring tests

---

## Quick Reference

| Need                 | File           | Function                 |
| -------------------- | -------------- | ------------------------ |
| Change colors        | styles.py      | apply_custom_css()       |
| Fix sidebar          | common.py      | render_sidebar()         |
| EDA bugs             | eda.py         | render_tab_eda()         |
| Pipeline info        | pipeline.py    | render_tab_pipeline()    |
| Prediction issues    | predict.py     | render_tab_predict()     |
| Metrics display      | metrics.py     | render_tab_metrics()     |
| Experiments problems | experiments.py | render_tab_experiments() |

---

## Support

For issues or questions about specific modules:

1. Check the module's docstring
2. Look at the dependencies section
3. Review the related `backend.py` or `model.py` code
4. Check Streamlit/Plotly documentation for rendering issues
