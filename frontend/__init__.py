"""
Frontend Module - Centralized Imports and Exports

This module organizes all UI components into separate, debuggable modules:
- styles.py: Page configuration and CSS
- common.py: Sidebar and hero banner
- eda.py: Exploratory Data Analysis tab

- predict.py: Prediction tab
- metrics.py: Model metrics tab
- experiments.py: Experiments framework tab
"""

from frontend.styles import set_page_config, apply_custom_css
from frontend.common import render_sidebar, render_hero
from frontend.eda import render_tab_eda
from frontend.predict import render_tab_predict
from frontend.metrics import render_tab_metrics
from frontend.experiments import render_tab_experiments

__all__ = [
    'set_page_config',
    'apply_custom_css',
    'render_sidebar',
    'render_hero',
    'render_tab_eda',
    'render_tab_predict',
    'render_tab_metrics',
    'render_tab_experiments',
]
