# Full Study Scaling Plan

## Overview

Based on pilot findings (N=131 jokes), this plan outlines full study (N=300 jokes, 75 per category) for statistical inference and publication.

---

## Pilot Findings Summary

### Quantitative Results

**Generation success gradient:** Linguistic 91% > Others 67%

**Predictability gradient (STRONGEST FINDING):** Linguistic 0.70 < Others 0.91-0.94

**Explanation quality:** Models explain linguistic humor semantically (correct), physical humor semantically (incorrect - should be embodied)

### Qualitative Validation

Manual inspection of explanations confirmed:
- Linguistic jokes: Models correctly identify semantic mechanisms (wordplay, puns, double meaning)
- Physical jokes: Models explain via semantic frameworks (metaphor, absurdity) NOT embodied frameworks (collision, pain, bodily sensation)
- Pattern is genuine, not artifact of keyword detection

### Conclusion

MODERATE TO STRONG support for H3 (hybrid hypothesis). Limitations: Small N, keyword detection issues resolved via qualitative analysis, need manual validation for full study.

---

## Full Study Parameters

### Sample Size

**Target:** N=300 jokes
- 75 per category (linguistic, physical, social, dark)
- 2 models (GPT-4o, Claude) × 75 = 150 jokes per category
- Excludes Gemini (systematic 18% failure in pilot)

**Rationale:** With N=75 per cell, can detect medium effect sizes (d=0.5) at 80% power, α=0.05 in mixed-effects models.

### Generation Parameters

- **Temperature:** 0.7 (optimal from pilot)
- **Max tokens:** 150
- **Format:** Setup/Punchline structure
- **Novel prompts:** Extended from pilot, unusual topic combinations

### Cost & Time Estimates

**Generation:**
- 300 jokes × $0.15 average = $45-75
- Time: 45-60 minutes

**Surprise analysis:**
- 100 jokes (25 per category) × $0.10 = $10
- Time: 10-15 minutes

**Explanation collection:**
- Option A: 300 jokes × 3 models = 900 explanations ($270)
- Option B: 150 jokes × 3 models = 450 explanations ($135)
- Recommendation: Option B (sufficient for validation)

**Total: $190-355** depending on sampling decisions

---

## Analysis Pipeline

### 1. Structural Analysis

Parse all 300 jokes:
- Setup/punchline validity
- Length appropriateness
- Format compliance
- Compare by category/model

### 2. Surprise Analysis

Sample 100 jokes (25 per category):
- Calculate punchline predictability
- Test category differences
- Confirm pilot gradient

### 3. Explanation Collection

**Recommended approach:** Sample 150 jokes (balanced across categories)
- Collect explanations from 3 models
- Total: 450 explanations
- Cost: $135

### 4. Manual Validation (CRITICAL)

**Protocol:**
- 2-3 human coders
- Independently code 50 random explanations
- Binary judgments: "Does this explanation appropriately cite X features?"
- Calculate inter-rater reliability (Cohen's kappa)
- Resolve disagreements through discussion
- Refine keyword lists based on patterns
- Apply refined coding to full dataset

**Quality threshold:** Cohen's kappa > 0.70

### 5. Statistical Inference

**Primary analysis:** Mixed-effects models

```
Model: Surprise ~ Category + (1|Joke) + (1|Model)
```

**Planned contrasts:**
- Linguistic vs Physical
- Linguistic vs Social
- Linguistic vs Dark

**Expected:** Linguistic significantly lower surprise (more predictable) than all other categories.

**Secondary analyses:**
- Generation success by category (chi-square test)
- Explanation feature citations by category (Poisson regression)
- Structural metrics by category (ANOVA)

---

## Implementation Steps

### Phase 1: Generation (Day 1)

```bash
cd ~/Desktop/benign-violations
source venv/bin/activate
python3 experiments/exp1_generation/scripts/full_study_generation.py
```

Output: 300 jokes saved to `experiments/exp1_generation/full_study/`

### Phase 2: Initial Analysis (Day 1-2)

```bash
# Structural analysis
python3 experiments/exp1_generation/scripts/analyze_structure.py

# Surprise analysis (sample 100)
python3 experiments/exp1_generation/scripts/analyze_surprise.py 100
```

### Phase 3: Explanation Collection (Day 2-3)

```bash
python3 experiments/exp2_explanation/scripts/full_study_explanations.py
```

Collects explanations for sampled jokes (recommended: 150 jokes × 3 models)

### Phase 4: Manual Validation (Day 3-5)

**Process:**
1. Export 50 random explanations to spreadsheet
2. Create coding rubric with examples
3. Train 2-3 coders on rubric
4. Independent coding session
5. Calculate kappa
6. Resolve disagreements
7. Refine keyword lists
8. Apply refined coding to full dataset

### Phase 5: Full Analysis (Day 5-7)

- Re-run automated coding with refined keywords
- Run mixed-effects models
- Calculate effect sizes
- Generate publication-quality figures
- Write results section

### Phase 6: Manuscript (Week 2)

- Update methods section
- Write results with inferential statistics
- Expand discussion
- Prepare supplementary materials
- Format for target venue
- Submit to conference/journal

---

## Quality Controls

1. **Novelty check:** Web search 30 random jokes to verify originality
2. **Format validation:** Automated check that all jokes have setup + punchline
3. **Length filter:** Exclude jokes outside 10-60 word range (if any)
4. **Manual inspection:** Read random sample of 10 jokes per category
5. **Inter-rater reliability:** Cohen's kappa > 0.70 for explanation coding

---

## Statistical Analysis Plan

### Descriptive Statistics

- Success rates by category/model (percentages)
- Mean surprise scores by category (M, SD, range)
- Feature citation frequencies (counts, proportions)

### Inferential Tests

**H3 Test 1: Generation Success**
```
Model: Success ~ Category
Method: Logistic regression
Expected: Linguistic > Others
```

**H3 Test 2: Predictability (PRIMARY TEST)**
```
Model: Surprise ~ Category + (1|Joke) + (1|Model)
Method: Linear mixed-effects model
Post-hoc: Tukey HSD for pairwise comparisons
Expected: Linguistic < Physical, Social, Dark
```

**H3 Test 3: Explanation Quality**
```
Model 1: SemanticFeatures ~ Category
Model 2: EmbodiedFeatures ~ Category
Method: Poisson regression (count data)
Expected: 
  - Semantic features: Linguistic > Others
  - Embodied features: Physical low (if dissociation exists)
```

### Effect Sizes

- Cohen's d for surprise comparisons
- Odds ratios for generation success
- Rate ratios for feature citations

### Visualization

- Bar plots with error bars: Success rates by category
- Violin plots: Surprise distributions by category
- Heatmap: Feature citations by category
- Scatter plot: Surprise vs structural metrics (exploratory)

---

## Timeline

### Week 1: Data Collection & Initial Analysis

- **Day 1:** Generation + structural analysis (4-5 hours)
- **Day 2:** Surprise analysis + begin explanation collection (4-5 hours)
- **Day 3:** Complete explanations + export for manual coding (3-4 hours)
- **Day 4-5:** Manual validation coding (6-8 hours total across coders)
- **Day 6-7:** Refine coding + statistical analysis (4-6 hours)

### Week 2: Manuscript Writing

- **Day 8-10:** Write full manuscript (8-10 hours)
- **Day 11-12:** Revision + supplementary materials (4-6 hours)
- **Day 13-14:** Final formatting + submission (2-4 hours)

**Total time commitment: 40-50 hours over 2 weeks**

---

## Success Criteria

### Minimum for Publication

1. N=300 jokes successfully generated
2. Surprise gradient confirmed (linguistic < others) with p < 0.05
3. Inter-rater reliability kappa > 0.70
4. Qualitative evidence of explanation dissociation documented
5. Honest limitation discussion included

### Ideal Outcome

- All H3 predictions confirmed across multiple measures
- Large effect sizes (d > 0.5 for surprise gradient)
- Clear qualitative examples of dissociation
- Exact replication of pilot patterns at larger scale

---

## Backup Plans

### If Results Don't Replicate

- Report honestly as pilot vs full study comparison
- Discuss possible reasons for differences (sampling, models, prompts)
- Explore alternative explanations
- Still publishable as methods paper or null results

### If Costs Exceed Budget

- Reduce explanation sample to 100 jokes (still sufficient)
- Skip surprise analysis entirely (pilot finding already strong)
- Focus resources on generation + explanations
- Use single coder with spot-checks instead of full inter-rater reliability

### If Timeline Extends

- Break into smaller phases
- Take breaks between phases to avoid burnout
- Consider recruiting collaborators for manual coding
- Extend timeline to 3-4 weeks if needed

---

## Next Steps After Full Study

### Publication Path

1. **Submit to conference** (deadline permitting)
   - CogSci (Cognitive Science Society) - interdisciplinary
   - ACL (Association for Computational Linguistics) - methods focus
   - NAACL (North American ACL) - similar to ACL

2. **Revise based on feedback**
   - Address reviewer concerns
   - Add requested analyses
   - Clarify methods/results

3. **Submit to journal**
   - Cognitive Science (interdisciplinary, high impact)
   - Computational Linguistics (methods/theory)
   - Artificial Intelligence (AI limitations)

4. **Post preprint**
   - arXiv (computer science)
   - PsyArXiv (psychology/cognitive science)
   - Both allowed for most venues

5. **Disseminate findings**
   - Share on academic Twitter/X
   - Post to Reddit r/MachineLearning, r/LanguageTechnology
   - Present at local research groups
   - Write accessible blog post

### Extensions to Consider

1. **Cross-cultural replication:** Test in multiple languages
2. **Multimodal models:** Test GPT-4V on visual slapstick
3. **Fine-tuning intervention:** Train on embodied language
4. **Neural analysis:** Compare LLM activation patterns
5. **Developmental study:** Test children's humor understanding

---

## Resources Needed

### Technical
- API access (OpenAI, Anthropic, Google)
- Python 3.12 environment
- Sufficient API credits ($200-350)
- Data storage (~500 MB)

### Human
- Primary researcher time (40-50 hours)
- 2-3 coders for validation (4-6 hours each)
- Optional: Feedback from collaborators

### Optional
- Prolific/MTurk for additional human validation
- Statistical consultation
- Professional editing/proofreading

---

## Contact for Collaboration

If interested in collaboration or have questions:
- Open GitHub issue at repository
- Email primary researcher (add contact)
- Join ongoing discussions

Areas where collaboration would be valuable:
- Manual explanation coding (coders)
- Cross-cultural replication (multilingual researchers)
- Statistical analysis consultation
- Embodied cognition theory discussion
- Multimodal extension (vision researchers)