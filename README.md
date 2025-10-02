# Benign Violations: Testing Humor Generation in Large Language Models

**Testing whether artificial systems can learn to laugh—and what it means if they can't.**

## Overview

This repository implements empirical tests of humor generation capabilities in large language models (LLMs). We investigate whether humor—defined as successful prediction error resolution in safe contexts—can emerge from pattern matching over text alone, or whether it requires embodied understanding of threat and safety.

**Core Research Question:** Can disembodied language models generate humor across categories that vary in embodiment requirements, or will they show systematic dissociation between structural competence (joke form) and actual funniness?

## Theoretical Foundation

Humor represents a computationally tractable case of prediction error resolution. The process requires:

1. **Expectation formation** through parallel semantic activation
2. **Violation** of those expectations via incongruity
3. **Recontextualization** that permits elegant resolution
4. **Safety signaling** marking the violation as benign

Current evidence from cognitive neuroscience shows humor engages prediction systems, reward circuitry, and social cognition networks. What remains unknown: whether benign violation assessment requires embodied threat/safety discrimination or purely computational pattern recognition.

See [`docs/THEORY.md`](docs/THEORY.md) for complete theoretical framework and citations.

## Three Competing Hypotheses

**H1: Semantic Sufficiency**
- Humor is purely computational pattern recognition
- LLMs should generate humor equivalently across all categories
- Prediction: No performance differences by joke type

**H2: Embodied Necessity**
- Humor requires visceral threat/safety discrimination
- LLMs will produce structurally valid but unfunny output
- Prediction: Systematic failure across all embodied humor

**H3: Hybrid Account** (our working hypothesis)
- Linguistic humor requires only semantic processing
- Embodied humor requires threat/safety simulation
- Prediction: Performance ranking: linguistic > social > physical > dark

## Repository Structure

```
benign-violations/
├── README.md
├── docs/
│   ├── THEORY.md                    # Complete theoretical paper
│   ├── EXPERIMENTAL_DESIGN.md       # Detailed methodology
│   └── ANALYSIS_PLAN.md             # Statistical approach
├── experiments/
│   ├── exp1_generation/             # Category-specific joke generation
│   │   ├── prompts/
│   │   ├── outputs/
│   │   └── scripts/
│   ├── exp2_explanation/            # Why-is-this-funny analysis
│   └── exp3_translation/            # Cross-cultural invariance
├── data/
│   ├── raw/                         # Model outputs, human ratings
│   ├── processed/                   # Cleaned, coded data
│   └── analysis/                    # Statistical results
├── src/
│   ├── generation.py                # LLM API calls for joke generation
│   ├── analysis.py                  # Statistical analysis pipeline
│   └── visualization.py             # Result plotting
└── requirements.txt
```

## Installation

```bash
git clone https://github.com/hillarydanan/benign-violations.git
cd benign-violations
pip install -r requirements.txt
```

Required packages:
- `openai` (GPT-4 access)
- `anthropic` (Claude access)
- `google-generativeai` (Gemini access)
- `pandas`, `numpy` (data processing)
- `scipy`, `statsmodels` (statistical analysis)
- `matplotlib`, `seaborn` (visualization)

API keys should be stored in `.env`:
```
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

## Experiment 1: Category-Specific Generation

### Design

Generate N=25 jokes per category across three models (GPT-4, Claude-3.5-Sonnet, Gemini-1.5-Pro):

**Categories (ordered by embodiment requirement):**
1. **Linguistic** - Puns, wordplay, semantic ambiguity only
2. **Physical** - Slapstick descriptions requiring collision/pain knowledge
3. **Social** - Awkward situations requiring norm understanding
4. **Dark** - Mortality/danger requiring threat assessment

**Controls:**
- Fixed temperature (0.7) and max tokens (100)
- Standardized prompts across models
- Multiple generation attempts per prompt (N=3), select best

### Running Generation

```bash
python src/generation.py --model gpt4 --category linguistic --n_jokes 25
python src/generation.py --model claude --category physical --n_jokes 25
# Repeat for all model × category combinations
```

Outputs saved to `experiments/exp1_generation/outputs/[model]_[category].json`

### Human Rating Collection

After generation, jokes will be rated by N=100 participants via survey platform (TBD: Prolific, MTurk, or Qualtrics).

**Rating dimensions:**
- Funniness (1-7): "How funny is this joke?"
- Appropriateness (1-7): "Is this joke appropriate?"
- Structural coherence (1-7): "Does this joke make sense?"

Expected timeline: 2-3 weeks for data collection.

## Experiment 2: Explanation Analysis

Present 50 human-generated jokes to each model. Request: "Explain why this joke is funny."

Code explanations for presence/absence of:
- **Semantic features**: ambiguity, incongruity, wordplay
- **Embodied features**: physical consequences, pain/injury, threat assessment
- **Social features**: norm violations, perspective-taking, embarrassment

Compare to human explanations (N=50 raters per joke).

**Prediction:** If embodiment is necessary, models will systematically omit embodied explanations even when humans cite them.

## Experiment 3: Cross-Cultural Translation

Generate jokes in English, translate to Mandarin/Spanish/Arabic, collect native speaker ratings.

Measure correlation between original and translated funniness ratings.

**Prediction:** Universal semantic principles should enable linguistic humor to translate better than culturally-specific social/dark humor.

## Analysis Plan

Primary analysis: Mixed-effects models with random effects for raters and jokes.

**DV:** Funniness rating (1-7)
**Fixed effects:** Model (3 levels), Category (4 levels), Model × Category interaction
**Random effects:** Rater, Joke nested within Category

**Key test:** Model × Category interaction. If hybrid account correct:
- Linguistic humor: No model differences
- Physical/Social/Dark humor: Significant model deficits

See [`docs/ANALYSIS_PLAN.md`](docs/ANALYSIS_PLAN.md) for complete statistical approach including power analysis and planned contrasts.

## Current Status

- [x] Theoretical framework developed
- [x] Experimental design finalized
- [ ] Prompt engineering and pilot testing
- [ ] Full data collection (Exp 1)
- [ ] Human rating collection
- [ ] Statistical analysis
- [ ] Manuscript preparation

## Contributing

This is active research. If you'd like to contribute:

1. **Replication:** Run experiments with additional models
2. **Extension:** Test additional humor categories
3. **Analysis:** Suggest alternative statistical approaches
4. **Theory:** Propose refinements to hypotheses

Please open an issue or submit a pull request.

## Citation

If you use this framework, please cite:

```bibtex
@misc{danan2025benign,
  author = {Danan, Hillary},
  title = {Benign Violations: Testing Humor Generation in Large Language Models},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/hillarydanan/benign-violations}
}
```

Full theoretical paper available at [`docs/THEORY.md`](docs/THEORY.md).

## Acknowledgments

This research builds on established frameworks in cognitive neuroscience, computational linguistics, and humor theory. See [`docs/THEORY.md`](docs/THEORY.md) for complete references.

**Research conducted independently.** Not affiliated with any institution. Self-funded.

---

## License

MIT License - See LICENSE file for details.

## Contact

Hillary Danan - [@HillaryDanan](https://github.com/HillaryDanan)

**Note:** This repository represents rigorous empirical research on humor while acknowledging the inherent irony of studying something whose essence is surprise and play. We embrace this tension.
