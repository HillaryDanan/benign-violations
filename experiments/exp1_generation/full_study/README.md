# Full Study Data Directory

This directory contains (or will contain) full study generation results for N=300 jokes.

---

## Purpose

Scale pilot study (N=131) to full study (N=300) for statistical inference and publication.

**Pilot findings:** Moderate to strong evidence for H3 (hybrid hypothesis) - linguistic humor shows highest generation success, lowest surprise scores (most predictable), and appropriate semantic explanations.

**Full study goal:** Confirm patterns with larger sample, conduct inferential statistics, enable manual validation.

---

## Files Structure

### Generated Data
- `full_study_data_YYYYMMDD_HHMMSS.json` - Raw generation results (300 jokes)
- `structural_analysis.csv` - Structural metrics for all jokes
- `structural_analysis.json` - Detailed structural data
- `surprise_analysis.csv` - Predictability scores (sampled subset)
- `surprise_analysis.json` - Detailed surprise analysis
- `comprehensive_report.txt` - Synthesized findings across all measures

### Analysis Outputs
- `generation_summary.txt` - Success rates by category/model
- `figures/` - Publication-quality plots (created during analysis)

---

## How to Generate Full Study Data

### Prerequisites

```bash
# Navigate to project
cd ~/Desktop/benign-violations

# Activate virtual environment
source venv/bin/activate

# Ensure API keys are set in .env
# Verify with:
python3 src/config.py
```

### Step 1: Generate Jokes

```bash
python3 experiments/exp1_generation/scripts/full_study_generation.py
```

**What it does:**
- Generates 300 jokes (75 per category)
- Uses GPT-4o and Claude only (excludes Gemini)
- Temperature: 0.7 (optimal from pilot)
- Novel prompts to minimize training data retrieval

**Time:** 45-60 minutes  
**Cost:** $50-75  
**Output:** `full_study_data_YYYYMMDD_HHMMSS.json`

### Step 2: Structural Analysis

```bash
python3 experiments/exp1_generation/scripts/analyze_structure.py
```

**What it does:**
- Parse all 300 jokes
- Calculate validity, length, format metrics
- Compare by category/model

**Time:** < 1 minute  
**Cost:** Free  
**Output:** `structural_analysis.csv`, `structural_analysis.json`

### Step 3: Surprise Analysis

```bash
python3 experiments/exp1_generation/scripts/analyze_surprise.py 100
```

**What it does:**
- Sample 100 jokes (25 per category)
- Calculate punchline predictability
- Test if linguistic jokes are most predictable

**Time:** 10-15 minutes  
**Cost:** ~$10  
**Output:** `surprise_analysis.csv`, `surprise_analysis.json`

### Step 4: Explanation Collection

```bash
python3 experiments/exp2_explanation/scripts/full_study_explanations.py
```

**What it does:**
- Collect explanations for 150 jokes (balanced sampling)
- Use all 3 models (GPT-4o, Claude, Gemini)
- Total: 450 explanations

**Time:** 30-45 minutes  
**Cost:** ~$135  
**Output:** `experiments/exp2_explanation/outputs/full_study_explanations_YYYYMMDD_HHMMSS.json`

### Step 5: Explanation Analysis

```bash
python3 experiments/exp2_explanation/scripts/analyze_explanations.py
```

**What it does:**
- Code explanations for feature types
- Test if models explain linguistic vs embodied humor differently

**Time:** < 1 minute  
**Cost:** Free  
**Output:** `experiments/exp2_explanation/outputs/explanation_analysis.csv`

### Step 6: Comprehensive Report

```bash
python3 experiments/exp1_generation/scripts/comprehensive_analysis.py
```

**What it does:**
- Synthesize all analyses
- Generate comprehensive report
- Test H3 predictions

**Time:** < 1 minute  
**Cost:** Free  
**Output:** `comprehensive_report.txt`

---

## Total Resource Requirements

### Cost
- Generation: $50-75
- Surprise analysis: $10
- Explanation collection: $135
- **Total: $195-220**

### Time
- Generation: 45-60 min
- Analyses: 45-60 min
- Manual validation (separate): 6-8 hours
- **Total automated: ~2 hours**

### Storage
- Raw data: ~50 MB
- Processed data: ~10 MB
- **Total: ~60 MB**

---

## Data Format

### Generation Data (JSON)

```json
{
  "id": "gpt4o_linguistic_full_0",
  "timestamp": "2025-10-03T12:00:00",
  "model": "gpt4o",
  "category": "linguistic",
  "temperature": 0.7,
  "raw_response": "Setup: ... Punchline: ...",
  "setup": "...",
  "punchline": "...",
  "full_text": "...",
  "metrics": {
    "total_words": 32,
    "setup_words": 15,
    "punchline_words": 17
  }
}
```

---

## Quality Checks

After generation, verify:
1. All 300 jokes generated successfully
2. Balanced distribution across categories
3. All jokes have valid structure (setup + punchline)
4. Lengths are reasonable (15-50 words target)
5. No obvious duplicates or errors

---

## Next Steps After Data Collection

1. **Manual validation:** 2-3 coders independently rate 50 explanations
2. **Statistical analysis:** Mixed-effects models, effect sizes
3. **Manuscript writing:** Update results section with full study
4. **Submission:** Conference or journal

See `docs/SCALING_PLAN.md` for complete roadmap.

---

## Troubleshooting

### Generation fails
- Check API keys in `.env`
- Verify sufficient API credits
- Check internet connection
- Review error messages in output

### Analysis errors
- Ensure generation completed successfully
- Verify JSON files are valid
- Check file paths in scripts
- Review terminal output for specific errors

### High costs
- Reduce explanation sample size (e.g., 100 instead of 150 jokes)
- Skip surprise analysis (pilot finding is strong)
- Use only 2 models instead of 3 for explanations

---

## Contact

Questions or issues? 
- Open GitHub issue at repository
- Check `docs/SCALING_PLAN.md` for detailed guidance
- Review `STATUS.md` for project context