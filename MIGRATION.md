# Frontend Refactoring - Migration Guide

## What Changed?

The monolithic `frontend.py` file (1000+ lines) has been reorganized into a clean, modular structure.

### Old Structure

```
frontend.py (1000+ lines)
├── set_page_config()
├── apply_custom_css()
├── render_sidebar()
├── render_hero()
├── render_tab_eda()
├── render_tab_pipeline()
├── render_tab_predict()
├── render_tab_metrics()
└── render_tab_experiments()
```

### New Structure

```
frontend/
├── __init__.py                 ← Centralized exports
├── styles.py                   ← Page config & CSS (200 lines)
├── common.py                   ← Sidebar & hero (60 lines)
├── eda.py                      ← EDA tab (140 lines)
├── pipeline.py                 ← Pipeline tab (90 lines)
├── predict.py                  ← Predict tab (120 lines)
├── metrics.py                  ← Metrics tab (120 lines)
├── experiments.py              ← Experiments tab (250 lines)
└── README.md                   ← Module documentation
```

## Benefits

✅ **Easier Debugging**: Find issues faster in smaller, single-purpose files
✅ **Better Maintainability**: Changes to one tab don't affect others
✅ **Scalability**: Easy to add new tabs or components
✅ **Code Organization**: Clear separation of concerns
✅ **Team Collaboration**: Multiple developers can work on different tabs
✅ **Testing**: Each module can be tested independently
✅ **Re-usability**: Components can be imported separately

## What Stayed the Same

- **app.py** imports are identical (uses `frontend/__init__.py`)
- **All functionality** is preserved
- **UI/UX** is unchanged
- **Dependencies** are the same
- **Performance** is the same

## How to Update Imports

### Before

```python
from frontend import (
    set_page_config, apply_custom_css, render_sidebar, ...
)
```

### After

```python
from frontend import (
    set_page_config, apply_custom_css, render_sidebar, ...
)
```

**No changes needed!** The `frontend/__init__.py` handles all imports automatically.

## File Locations

| Function                   | Old File    | New File                |
| -------------------------- | ----------- | ----------------------- |
| `set_page_config()`        | frontend.py | frontend/styles.py      |
| `apply_custom_css()`       | frontend.py | frontend/styles.py      |
| `render_sidebar()`         | frontend.py | frontend/common.py      |
| `render_hero()`            | frontend.py | frontend/common.py      |
| `render_tab_eda()`         | frontend.py | frontend/eda.py         |
| `render_tab_pipeline()`    | frontend.py | frontend/pipeline.py    |
| `render_tab_predict()`     | frontend.py | frontend/predict.py     |
| `render_tab_metrics()`     | frontend.py | frontend/metrics.py     |
| `render_tab_experiments()` | frontend.py | frontend/experiments.py |

## Quick Debugging

Need to fix something?

1. **Colors/styling issues** → `frontend/styles.py`
2. **Sidebar not showing** → `frontend/common.py`
3. **EDA visualizations broken** → `frontend/eda.py`
4. **Pipeline info wrong** → `frontend/pipeline.py`
5. **Prediction not working** → `frontend/predict.py`
6. **Metrics display error** → `frontend/metrics.py`
7. **Experiments failing** → `frontend/experiments.py`

## Testing Individual Tabs

You can now test individual tabs in isolation:

```python
# Test only EDA
from frontend.eda import render_tab_eda
import streamlit as st
df = load_data()
render_tab_eda(df)

# Test only Metrics
from frontend.metrics import render_tab_metrics
render_tab_metrics(results)
```

## Removing Old File

**Optional:** You can delete the old `frontend.py` file (it's no longer used):

```bash
rm frontend.py
```

All code has been migrated and `frontend/__init__.py` provides the same interface.

## Project Structure After Refactoring

```
SMS-Spam-Classification/
├── app.py                  ← Main application (unchanged)
├── model.py                ← ML models and experiments
├── backend.py              ← Prediction and utilities
├── experiments.py          ← Standalone experiments runner
│
├── frontend/               ← ⭐ NEW: Modular frontend
│   ├── __init__.py
│   ├── styles.py
│   ├── common.py
│   ├── eda.py
│   ├── pipeline.py
│   ├── predict.py
│   ├── metrics.py
│   ├── experiments.py
│   └── README.md
│
├── data/
│   └── SMSSpamCollection
│
├── results/                ← Experiment outputs (optional)
├── requirements.txt        ← Dependencies
├── README.md               ← Main project README
├── EXPERIMENTS.md          ← Experiments guide
└── (old frontend.py → can be deleted)
```

## Running the App

No changes to how you run the app:

```bash
streamlit run app.py
```

The application works exactly as before!

## Common Issues & Solutions

### Issue: ModuleNotFoundError: No module named 'frontend.eda'

**Solution:** Make sure you're running from the project root directory:

```bash
cd SMS-Spam-Classification
streamlit run app.py
```

### Issue: Import errors in app.py

**Solution:** Check that `frontend/__init__.py` exists and has all exports:

```bash
ls -la frontend/
# Should show: __init__.py, styles.py, common.py, eda.py, ...
```

### Issue: Styles not applying

**Solution:** Make sure `frontend/styles.py` has the CSS. Check that app.py calls `apply_custom_css()`.

## Rollback (If Needed)

If you need to go back to the monolithic frontend:

1. Keep the old `frontend.py` as `frontend_backup.py`
2. Update `app.py` imports:

```python
from frontend_backup import (
    set_page_config, apply_custom_css, ...
)
```

3. Comment out the new `frontend/` imports

## Next Steps

- ✅ Code is organized and debuggable
- [ ] Add unit tests for each module
- [ ] Add type hints throughout
- [ ] Create shared component library
- [ ] Add logging for debugging
- [ ] Profile performance per tab

---

**Timeline:**

- Refactoring completed: April 8, 2026
- Old `frontend.py`: Preserved as reference (can be deleted)
- All functionality: Working as before
- Code quality: Significantly improved

**Questions?** Check `frontend/README.md` for detailed module information.
