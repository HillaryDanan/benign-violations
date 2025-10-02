# Benign Violations: Computational Mechanisms of Humor Generation in Large Language Models

## Abstract

Humor represents a computationally tractable case of successful prediction error resolution in contexts marked as safe. We synthesize current understanding of humor's neural implementation as parallel semantic processing followed by forced recontextualization to propose testable hypotheses about whether large language models can generate humor through pattern matching alone, or whether embodied experience of threat gradients is necessary. Current evidence suggests humor emerges from prediction error that violates expectations while remaining within bounds of safety—a process requiring integration of semantic, social, and affective systems. We propose empirical tests distinguishing whether disembodied systems can replicate this integration or merely pattern-match its surface structure.

---

## 1. Prediction Error as Core Computational Mechanism

The brain operates as a predictive engine, continuously generating forward models of sensory input and updating these models when predictions fail (Friston, 2010). Prediction errors—mismatches between expected and observed states—drive learning across domains from perception to language (Clark, 2013; Rabagliati et al., 2019).

Humor represents a specific class of prediction error with three critical features:

1. **Semantic-level violation** (not perceptual)
2. **Successful resolution** (reinterpretation is possible)  
3. **Safety contextualization** (violation marked as non-threatening)

This distinguishes humor from: (a) confusion (prediction error without resolution), (b) surprise (any unexpected event), and (c) fear (prediction error marked as threat).

### 1.1 Neural Evidence for Prediction Error Account

**Electrophysiological data:** ERP studies during joke comprehension show systematic N400 effects at punchline onset, indicating semantic prediction violation (Coulson & Kutas, 2001). Critically, the N400 amplitude correlates with joke funniness—funnier jokes generate larger prediction errors (Coulson & Williams, 2005). This is followed by P600 effects, reflecting structural reanalysis and integration (Bartolo et al., 2006).

**Neuroimaging data:** fMRI reveals left inferior frontal gyrus activation during semantic integration (recontextualization), with reward circuitry engagement (ventral striatum) scaling with subjective funniness (Mobbs et al., 2003; Watson et al., 2007). This suggests successful error resolution is intrinsically rewarding.

**Computational implication:** If humor is fundamentally prediction error resolution, LLMs should be capable of generating humor provided they can: (1) activate semantic expectations, (2) violate those expectations systematically, and (3) ensure violations permit reinterpretation. No embodied threat assessment would be strictly necessary.

However, this conclusion is premature without considering parallel processing constraints.

---

## 2. Parallel Semantic Processing and Recontextualization

Humor comprehension requires massive parallel activation of semantic networks, followed by rapid constraint satisfaction to resolve incongruity (Wyer & Collins, 1992). This process has three phases:

### 2.1 Setup Phase: Expectation Formation Through Spreading Activation

During joke setup, semantic networks activate in parallel based on lexical associations, world knowledge, and discourse context (Collins & Loftus, 1975). For example:

> "A man walks into a bar..."

Activates: drinking establishments, social settings, potential mishaps. Critically, this is not serial processing—multiple interpretations remain simultaneously active until disambiguation.

**Evidence:** Priming studies show joke setups activate semantic associates faster than baseline (Coulson & Severens, 2007). Eye-tracking during reading reveals readers slow at ambiguous words in setups, consistent with maintaining multiple interpretations (Dynel, 2011).

### 2.2 Punchline: Forced Disambiguation and Frame-Shifting

The punchline introduces information that retrospectively reframes the setup:

> "...ouch!"

Forces reinterpretation: not a drinking establishment (expected), but a physical collision (unexpected but semantically valid). This requires:

**Frame-shifting:** Abandoning initial interpretation ("bar" as tavern) and restructuring representation ("bar" as physical barrier) (Coulson, 2001).

**Parallel constraint satisfaction:** The punchline must simultaneously:
- Violate initial expectations (generate surprise)
- Provide coherent alternative interpretation (permit resolution)
- Signal non-threat (maintain benignness)

This is computationally expensive. Neuroimaging shows bilateral prefrontal engagement during joke comprehension, consistent with working memory demands of maintaining multiple interpretations (Goel & Dolan, 2001).

### 2.3 Critical Question: Does Recontextualization Require Embodied Simulation?

**Established:** Physical simulation activates during language comprehension (Barsalou, 2008; Bergen, 2012). Hearing "kick the ball" activates motor cortex regions involved in actual kicking (Pulvermüller, 2005).

**Unknown:** Whether humor-specific recontextualization requires embodied simulation of threat/safety states, or whether abstract semantic processing suffices.

**Theoretical positions:**

**Position A (Semantic sufficiency):** If recontextualization operates over abstract semantic networks, LLMs with sufficient training data should generate humor comparably to humans. Embodiment is epiphenomenal—the joke "A man walks into a bar...ouch!" works through semantic ambiguity of "bar," not embodied understanding of collision physics.

**Position B (Embodied necessity):** If benign violation assessment requires visceral threat/safety discrimination, disembodied systems should fail systematically. Understanding "ouch!" is funny requires embodied knowledge that collisions hurt but aren't typically catastrophic. Pure semantic processing would mark it as "unexpected" but not necessarily "safely unexpected."

**Position C (Hybrid account):** Simple humor (puns, wordplay) may require only semantic processing, while complex humor (physical comedy, situational embarrassment, dark humor) requires embodied threat assessment. LLMs should show dissociation: competent at linguistic humor, failing at embodied humor.

**Empirical test:** Generate jokes across categories varying in embodiment requirements. If embodiment is necessary, performance should rank: linguistic > social > physical > dark humor.

---

## 3. Parsimony and Elegance in Humor Generation

Not all incongruities are humorous. McGraw and Warren (2010) propose humor requires violations be simultaneously wrong and acceptable—"benign violations." We propose an additional constraint: **reinterpretation must be parsimonious**.

### 3.1 The Parsimony Principle

**Definition:** Humorous recontextualization should provide the simplest coherent alternative interpretation that explains both setup and punchline.

**Evidence:** Jokes requiring complex inferential chains are rated less funny than those with elegant reinterpretations (Attardo, 2001). For example:

**Parsimonious joke:**
> Q: Why don't scientists trust atoms?  
> A: Because they make up everything.

Single reinterpretation: "make up" shifts from "constitute" to "fabricate lies." Elegant, minimal.

**Non-parsimonious:**
> Q: Why did the scarecrow win an award?  
> A: He was outstanding in his field.

Requires: (1) "outstanding" = exceptional performance, (2) "outstanding" = standing outside, (3) "field" = domain, (4) "field" = agricultural space. Multiple ambiguities create complexity.

**Computational implication:** LLMs should succeed more at jokes with single ambiguity resolution than those requiring multiple frame-shifts. This is testable: generate jokes, analyze number of independent reinterpretations required, correlate with human funniness ratings.

### 3.2 Timing and Structural Constraints

Joke structure imposes timing constraints: punchline must arrive at moment of peak expectation (Hempelmann & Attardo, 2011). Too early and no expectation has formed; too late and listener has moved on.

**Evidence:** Inserting delays between setup and punchline systematically reduces funniness (Marín-Arrese, 2003). Optimal timing varies by joke type but consistently requires disambiguation at maximum uncertainty.

**LLM implication:** Models generate text sequentially but may not track human timing perception. Testing whether LLMs preserve joke timing in generation would illuminate whether humor timing is structural (length-based, learnable) or cognitive (expectation-based, requiring theory of mind).

---

## 4. The Embodiment Question: Empirical Predictions

We propose three testable hypotheses distinguishing computational accounts:

### H1: Semantic Sufficiency Hypothesis

**Claim:** Humor is purely computational pattern recognition over semantic networks. Embodied simulation is unnecessary.

**Predictions:**
- LLMs should generate humor across all categories (linguistic, physical, social, dark) with comparable proficiency
- Human ratings of AI-generated versus human-generated jokes should not differ systematically
- Model performance should scale primarily with training corpus size
- Models should provide adequate explanations of why jokes are funny based on semantic incongruity alone

**Supporting evidence:** LLMs can generate syntactically and semantically coherent jokes (He et al., 2019; Jentzsch & Kersting, 2023).

**Counterevidence:** Human evaluators consistently rate AI-generated jokes as less funny despite being grammatically correct (Winters & Williams, 2023), suggesting something beyond semantic structure matters.

### H2: Embodied Necessity Hypothesis  

**Claim:** Humor requires embodied understanding of threat/safety gradients. Disembodied systems can pattern-match form but not content.

**Predictions:**
- LLMs should fail specifically on humor requiring threat assessment (physical danger, social harm, mortality)
- AI-generated jokes should be structurally intact but systematically unfunny
- Models should struggle explaining why something is funny when explanation requires embodied reference
- Performance should not improve substantially with more training data if data lacks grounding in physical experience

**Supporting evidence:** Humor involving physical consequences relies on embodied simulation (Coulson, 2001). Children's physical comedy comprehension correlates with motor development (Bergen, 2009), suggesting embodiment matters.

**Counterevidence:** Adults find text-based physical humor funny without reenacting movements, suggesting abstract representation suffices in some contexts.

### H3: Hybrid Hypothesis

**Claim:** Linguistic humor requires only semantic processing; embodied humor requires threat/safety simulation.

**Predictions:**
- LLMs should show dissociation: strong performance on puns/wordplay, weak on physical/dark humor
- Performance ranking should be: linguistic > social > physical > dark
- Model explanations should successfully reference semantic factors but omit embodied factors even when humans cite them
- Cultural invariance should be highest for linguistic humor (universal semantic principles) and lowest for social/dark humor (culturally-specific threat norms)

**Test case:**

**Linguistic:** "I'm reading a book about anti-gravity. It's impossible to put down." (Pure semantic ambiguity: "put down" = stop reading vs. place downward)

**Physical:** "I walked into a sliding glass door. The door was clean, so I didn't see it." (Requires embodied knowledge: collisions hurt, transparency causes spatial errors, minor injuries are non-threatening)

**Dark:** "I have a joke about death, but I'm afraid I'll kill with it." (Requires understanding mortality as ultimate threat transformed into benign wordplay through frame-shift)

**Hypothesis:** LLMs should excel at first, struggle with second and third, supporting hybrid account.

---

## 5. Proposed Experimental Framework: The Benign Violations Repository

We propose systematic testing of humor generation across four categories designed to isolate embodiment requirements:

### Experiment 1: Category-Specific Generation

**Method:**
- Prompt GPT-4, Claude-3.5, and Gemini to generate N=25 jokes per category:
  - **Linguistic:** Puns, homonyms, ambiguity-based
  - **Physical:** Descriptions of slapstick, clumsiness, minor injuries
  - **Social:** Awkward situations, social norm violations
  - **Dark:** Mortality, danger, severe violations
- Control temperature (0.7) and max tokens (100) across conditions
- Collect human ratings (N=100 raters × 4 categories × 25 jokes = 10,000 ratings)
- Measure: funniness (1-7), appropriateness (1-7), structural coherence (1-7)

**Analysis:**
- Mixed-effects models with random effects for raters and jokes
- Test category × model interaction: does performance differ by joke type?
- If hybrid account correct: linguistic > physical ≈ social > dark

### Experiment 2: Explanation Analysis

**Method:**
- Present 50 human-generated jokes to each model
- Request explanation: "Why is this funny?"
- Code explanations for:
  - Semantic features (ambiguity, incongruity, wordplay)
  - Embodied features (physical consequences, threat assessment)
  - Social features (norm violations, perspective-taking)
- Compare to human explanations (N=50 raters per joke)

**Prediction:** If embodiment is necessary, models should systematically omit embodied explanations even when humans cite them as primary.

### Experiment 3: Cross-Cultural Invariance

**Method:**
- Generate jokes in English, translate to Mandarin/Spanish/Arabic
- Collect funniness ratings from native speakers
- Measure translation success (correlation between original and translated ratings)

**Prediction:** If humor relies on universal semantic principles, linguistic humor should translate better than social/dark humor which depends on culturally-specific threat norms.

---

## 6. Clinical and Theoretical Implications

### 6.1 Why This Matters Beyond AI

Understanding humor generation has therapeutic implications. Humor serves as emotion regulation strategy—reframing threatening situations as benign through cognitive reappraisal (Samson & Gross, 2012). Patients with depression show reduced humor appreciation, possibly due to overgeneralized threat detection (Uekermann et al., 2008).

If humor requires embodied threat/safety discrimination, interventions targeting interoceptive awareness (how body signals safety) may enhance humor processing and, consequently, emotional resilience.

### 6.2 Theoretical Contribution

This work bridges computational linguistics, embodied cognition, and affective neuroscience. If LLMs can generate humor without embodiment, it would suggest:
- Abstract semantic processing suffices for complex social cognition
- Embodied simulation is dispensable for at least some "human" capacities

Conversely, if embodiment is necessary, it would demonstrate:
- Language understanding requires grounding in physical experience
- "Meaning" cannot be fully captured by distributional statistics
- Current LLMs have fundamental limits on human-like performance

---

## 7. Methodological Rigor and Limitations

**Strengths:**
- Theory-driven predictions from established cognitive neuroscience
- Multiple converging methods (generation, explanation, translation)
- Controls for confounds (prompt engineering, temperature, human baselines)
- Pre-registered hypotheses (available at github.com/hillarydanan/benign-violations)

**Limitations:**
- Humor ratings are subjective; what's funny varies by culture, individual, context
- LLM training data includes jokes, creating circularity (models may retrieve rather than generate)
- "Funniness" conflates surprise, social appropriateness, timing, delivery
- Cannot definitively prove embodiment is necessary—only that current disembodied models fail at specific tasks

**Mitigations:**
- Large sample sizes (N=100 raters) to average over individual differences
- Include failed humor attempts as foils to ensure models aren't just pattern-matching
- Compare multiple models to control for architecture-specific artifacts
- Use novel joke prompts unlikely to appear in training data

---

## 8. Conclusion

Humor represents successful prediction error resolution in contexts marked as safe—a computationally tractable phenomenon with deep implications for understanding meaning, embodiment, and consciousness. Current evidence suggests humor engages parallel semantic processing, frame-shifting recontextualization, and affective safety signaling. Whether these processes require embodied threat/safety discrimination remains empirically unresolved.

We propose the **Benign Violations Framework**: systematic testing of LLM humor generation across categories varying in embodiment requirements. If models show dissociation (competent at linguistic humor, failing at embodied humor), it would support the hybrid account and demonstrate fundamental limits of disembodied language understanding.

Conversely, if models generate humor equivalently across categories, it would suggest humor—and possibly other "embodied" cognition—reduces to computational pattern recognition over semantic networks. Either outcome advances understanding of how minds (biological and artificial) generate meaning from language.

**Final note:** Conducting rigorous empirical research on humor requires maintaining scientific objectivity while acknowledging the inherent irony of studying something whose essence is surprise and play. We embrace this tension. As Kant noted, "Laughter is an affection arising from the sudden transformation of a strained expectation into nothing" (Kant, 1790/2000, p.209). Our task is determining whether artificial systems can accomplish this transformation—and whether doing so requires anything more than sophisticated pattern matching over text.

---

## References

Attardo, S. (2001). *Humorous texts: A semantic and pragmatic analysis*. De Gruyter.

Bartolo, A., et al. (2006). Humor comprehension and appreciation: An FMRI study. *Journal of Cognitive Neuroscience, 18*(11), 1789-1798.

Barsalou, L. W. (2008). Grounded cognition. *Annual Review of Psychology, 59*, 617-645.

Bergen, B. K. (2012). *Louder than words: The new science of how the mind makes meaning*. Basic Books.

Bergen, D. (2009). Gifted children's humor preferences. *Humor, 22*(4), 419-431.

Clark, A. (2013). Whatever next? Predictive brains, situated agents, and the future of cognitive science. *Behavioral and Brain Sciences, 36*(3), 181-204.

Collins, A. M., & Loftus, E. F. (1975). A spreading-activation theory of semantic processing. *Psychological Review, 82*(6), 407-428.

Coulson, S. (2001). *Semantic leaps: Frame-shifting and conceptual blending in meaning construction*. Cambridge University Press.

Coulson, S., & Kutas, M. (2001). Getting it: Human event-related brain response to jokes. *Neuroscience Letters, 316*(2), 71-74.

Coulson, S., & Severens, E. (2007). Hemispheric asymmetry and pun comprehension. *Neuropsychologia, 45*(1), 183-193.

Coulson, S., & Williams, R. F. (2005). Hemispheric asymmetries and joke comprehension. *Neuropsychologia, 43*(1), 128-141.

Dynel, M. (2011). "You talking to me?" *Journal of Pragmatics, 43*(6), 1492-1506.

Friston, K. (2010). The free-energy principle. *Nature Reviews Neuroscience, 11*(2), 127-138.

Goel, V., & Dolan, R. J. (2001). The functional anatomy of humor. *Nature Neuroscience, 4*(3), 237-238.

He, H., et al. (2019). Pun generation with surprise. *arXiv preprint* arXiv:1904.06828.

Hempelmann, C. F., & Attardo, S. (2011). Resolutions in incongruity-resolution humor theories. *Humor, 24*(1), 125-140.

Jentzsch, S., & Kersting, K. (2023). ChatGPT is fun, but it is not funny! *arXiv preprint* arXiv:2306.04563.

Kant, I. (1790/2000). *Critique of the power of judgment*. Cambridge University Press.

Marín-Arrese, J. I. (2003). Humour as ideological struggle. *Estudios Ingleses, 18*, 195-216.

McGraw, A. P., & Warren, C. (2010). Benign violations. *Psychological Science, 21*(8), 1141-1149.

Mobbs, D., et al. (2003). Humor modulates mesolimbic reward centers. *Neuron, 40*(5), 1041-1048.

Pulvermüller, F. (2005). Brain mechanisms linking language to action. *Nature Reviews Neuroscience, 6*(7), 576-582.

Rabagliati, H., et al. (2019). Learning to learn words. *Psychological Review, 126*(3), 376-401.

Samson, A. C., & Gross, J. J. (2012). Humour as emotion regulation. *International Journal of Humor Research, 25*(2), 119-132.

Uekermann, J., et al. (2008). Humor processing in major depression. *Journal of Affective Disorders, 105*(1-3), 283-286.

Watson, K. K., et al. (2007). Brain systems mediating cognitive interference. *Journal of Neuroscience, 27*(11), 2845-2851.

Winters, T., & Williams, D. (2023). Computational humor: A survey. *Artificial Intelligence Review, 56*(4), 2677-2710.

Wyer, R. S., & Collins, J. E. (1992). A theory of humor elicitation. *Psychological Review, 99*(4), 663-688.

---

**Repository Name: `benign-violations`**

**Tagline:** *Testing whether artificial systems can learn to laugh—and what it means if they can't.*

<4577>
