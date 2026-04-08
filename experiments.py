"""
SMS Spam Classification - Comprehensive Experiments Runner
Runs all experiments and generates detailed report
"""
import pandas as pd
import numpy as np
import os
import sys
from model import (
    load_data, preprocess_data, run_all_experiments, 
    create_comparison_table, generate_report
)
import json
from datetime import datetime


def save_results_to_file(all_results, df, output_dir='results'):
    """Save detailed results to files."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate and save report
    report = generate_report(all_results, df)
    report_path = os.path.join(output_dir, 'EXPERIMENT_REPORT.txt')
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"✅ Report saved to: {report_path}")
    
    # Save comparison table as CSV
    comparison_df = create_comparison_table(all_results)
    csv_path = os.path.join(output_dir, 'COMPARISON_TABLE.csv')
    comparison_df.to_csv(csv_path, index=False)
    print(f"✅ Comparison table saved to: {csv_path}")
    
    # Save detailed metrics as JSON
    metrics = {}
    
    # Main experiments
    for key, result in all_results['main_experiments'].items():
        metrics[key] = {
            'experiment_name': result['experiment_name'],
            'accuracy': float(result['accuracy']),
            'precision': float(result['precision']),
            'recall': float(result['recall']),
            'f1': float(result['f1']),
            'confusion_matrix': result['confusion_matrix'].tolist()
        }
    
    # Tweaks
    for key, result in all_results['tweaks'].items():
        metrics[key] = {
            'experiment_name': result['experiment_name'],
            'accuracy': float(result['accuracy']),
            'precision': float(result['precision']),
            'recall': float(result['recall']),
            'f1': float(result['f1']),
            'confusion_matrix': result['confusion_matrix'].tolist()
        }
    
    metrics_path = os.path.join(output_dir, 'METRICS.json')
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"✅ Metrics saved to: {metrics_path}")
    
    return report_path, csv_path, metrics_path


def main():
    """Main execution function."""
    print("="*80)
    print("SMS SPAM CLASSIFICATION - COMPREHENSIVE EXPERIMENTS")
    print("="*80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    # Load data
    print("Loading dataset...")
    df = load_data()
    print(f"Loaded {len(df):,} messages")
    print("")
    
    # Run all experiments
    print("Running all experiments...")
    print("This may take a few minutes...")
    print("")
    all_results = run_all_experiments(df)
    
    print("")
    print("Experiments completed!")
    print("")
    
    # Save results
    print("Saving results...")
    report_path, csv_path, metrics_path = save_results_to_file(all_results, df)
    
    # Print summary
    print("")
    print("="*80)
    print("SUMMARY OF RESULTS")
    print("="*80)
    
    comparison_df = create_comparison_table(all_results)
    print("")
    print(comparison_df.to_string(index=False))
    print("")
    
    # Find best
    main_exp_f1 = {
        k: v['f1'] for k, v in all_results['main_experiments'].items()
    }
    best_main = max(main_exp_f1.items(), key=lambda x: x[1])
    print("MAIN EXPERIMENTS - Best Performer:")
    print(f"  {best_main[0]}")
    print(f"  F1-Score: {best_main[1]:.4f}")
    print("")
    
    all_f1 = {}
    for k, v in all_results['main_experiments'].items():
        all_f1[v['experiment_name']] = v['f1']
    for k, v in all_results['tweaks'].items():
        all_f1[v['experiment_name']] = v['f1']
    
    best_overall = max(all_f1.items(), key=lambda x: x[1])
    print("ALL EXPERIMENTS - Best Performer:")
    print(f"  {best_overall[0]}")
    print(f"  F1-Score: {best_overall[1]:.4f}")
    print("")
    
    print("="*80)
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Full report saved to: results/")
    print("="*80)


if __name__ == "__main__":
    # Disable cache for this run to ensure fresh experiments
    import streamlit as st
    st.cache_data.clear()
    st.cache_resource.clear()
    
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
