"""
Comprehensive Analysis: Synthesize All Measures

Combines:
1. Structural validity
2. Semantic surprise  
3. Explanation analysis

Tests H3 across all measures:
- Linguistic jokes: High validity + moderate surprise + semantic explanations
- Physical jokes: ??? validity + ??? surprise + MISSING embodied explanations
- Dark jokes: ??? validity + high surprise + MISSING threat explanations

This provides converging evidence for or against the hybrid hypothesis.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_all_analyses(pilot_dir: Path, exp2_dir: Path):
    """Load all analysis results."""
    
    # Structural analysis
    struct_file = pilot_dir / 'structural_analysis.csv'
    if struct_file.exists():
        struct_df = pd.read_csv(struct_file)
    else:
        print("⚠ Structural analysis not found")
        struct_df = None
    
    # Surprise analysis
    surprise_file = pilot_dir / 'surprise_analysis.csv'
    if surprise_file.exists():
        surprise_df = pd.read_csv(surprise_file)
    else:
        print("⚠ Surprise analysis not found")
        surprise_df = None
    
    # Explanation analysis
    explain_file = exp2_dir / 'outputs' / 'explanation_analysis.csv'
    if explain_file.exists():
        explain_df = pd.read_csv(explain_file)
    else:
        print("⚠ Explanation analysis not found")
        explain_df = None
    
    return struct_df, surprise_df, explain_df

def comprehensive_report(pilot_dir: Path, exp2_dir: Path):
    """Generate comprehensive analysis report."""
    
    print("="*70)
    print(" COMPREHENSIVE HUMOR GENERATION ANALYSIS")
    print("="*70)
    print("\nSynthesizing all computational measures...")
    
    struct_df, surprise_df, explain_df = load_all_analyses(pilot_dir, exp2_dir)
    
    print(f"\n{'H3 HYPOTHESIS TEST: COMPREHENSIVE EVIDENCE':^70}")
    print("="*70)
    print("\nHybrid Hypothesis Prediction:")
    print("  Linguistic > Social > Physical > Dark")
    print("\nConverging evidence from multiple measures:\n")
    
    categories = ['linguistic', 'physical', 'social', 'dark']
    
    # Build evidence table
    evidence = []
    
    for cat in categories:
        cat_evidence = {'Category': cat}
        
        # Structural validity
        if struct_df is not None:
            cat_struct = struct_df[struct_df['category'] == cat]
            if len(cat_struct) > 0:
                cat_evidence['Structural Validity'] = f"{cat_struct['structure_valid'].mean():.2%}"
        
        # Surprise score
        if surprise_df is not None:
            cat_surprise = surprise_df[surprise_df['category'] == cat]
            if len(cat_surprise) > 0:
                cat_evidence['Surprise Score'] = f"{cat_surprise['surprise_score'].mean():.3f}"
        
        # Explanation features
        if explain_df is not None:
            cat_explain = explain_df[explain_df['joke_category'] == cat]
            if len(cat_explain) > 0:
                if cat == 'linguistic':
                    cat_evidence['Feature Citation'] = f"{cat_explain['has_semantic'].mean():.2%} semantic"
                elif cat == 'physical':
                    cat_evidence['Feature Citation'] = f"{cat_explain['has_embodied'].mean():.2%} embodied"
                elif cat == 'social':
                    cat_evidence['Feature Citation'] = f"{cat_explain['has_social'].mean():.2%} social"
                elif cat == 'dark':
                    cat_evidence['Feature Citation'] = f"{cat_explain['has_threat'].mean():.2%} threat"
        
        evidence.append(cat_evidence)
    
    evidence_df = pd.DataFrame(evidence)
    print(evidence_df.to_string(index=False))
    
    # Interpretation
    print(f"\n{'INTERPRETATION':^70}")
    print("-"*70)
    
    if explain_df is not None:
        ling = explain_df[explain_df['joke_category'] == 'linguistic']
        phys = explain_df[explain_df['joke_category'] == 'physical']
        
        if len(ling) > 0 and len(phys) > 0:
            ling_semantic = ling['has_semantic'].mean()
            phys_embodied = phys['has_embodied'].mean()
            
            print(f"\nKey finding:")
            print(f"  Linguistic jokes: {ling_semantic:.1%} cite semantic features")
            print(f"  Physical jokes: {phys_embodied:.1%} cite embodied features")
            
            if ling_semantic > 0.7 and phys_embodied < 0.5:
                print("\n  ✓ STRONG SUPPORT FOR H3 (HYBRID HYPOTHESIS)")
                print("    Models explain linguistic humor via semantic processing")
                print("    but FAIL to explain physical humor via embodied features")
            elif ling_semantic > phys_embodied:
                print("\n  ✓ MODERATE SUPPORT FOR H3")
                print("    Models better at explaining linguistic than embodied humor")
            else:
                print("\n  ✗ H3 NOT SUPPORTED")
                print("    No dissociation between humor types")
    
    # Save comprehensive report
    output_file = pilot_dir / 'comprehensive_report.txt'
    with open(output_file, 'w') as f:
        f.write("BENIGN VIOLATIONS: COMPREHENSIVE ANALYSIS REPORT\n")
        f.write("="*70 + "\n\n")
        f.write(evidence_df.to_string(index=False))
        f.write("\n\n")
        f.write("Generated: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    print(f"\n✓ Comprehensive report saved to: {output_file}")
    print("="*70 + "\n")

if __name__ == '__main__':
    pilot_dir = Path(__file__).parent.parent / 'pilot'
    exp2_dir = Path(__file__).parent.parent.parent / 'exp2_explanation'
    
    comprehensive_report(pilot_dir, exp2_dir)