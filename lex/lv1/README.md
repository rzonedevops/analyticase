# Level 1: First-Order Principles (Known Legal Maxims)

## Overview

This directory contains the foundational legal maxims and principles that form the basis of all legal reasoning in the AnalytiCase framework. These are **inference level 1** - the first-order principles from which higher-order legal principles are derived through the inference engine.

## Inference Level Hierarchy

```
Level 2 (lv2): Meta-Principles (Legal Foundations/Theories)
    ↓ Deductive/Abductive Inference
Level 1 (lv1): First-Order Principles (This Layer)
    ↓ Inductive/Abductive Inference
Level 0: Enumerated Laws
    ↓
Level -1: Specific Cases
```

## Purpose

Level 1 principles serve as the foundation for:

1. **Legal Reasoning**: All legal arguments trace back to these fundamental principles, which themselves derive from Level 2 jurisprudential theories
2. **Inference Generation**: Higher-level principles are derived from combinations of these laws, and these laws are derived from Level 2 meta-principles
3. **Framework Derivation**: The scheme frameworks in `lex/civ/`, `lex/cri/`, etc. are based on these principles
4. **Confidence Scoring**: Level 1 principles have confidence = 1.0 (explicitly stated, universally recognized)
5. **Theoretical Grounding**: Each principle can be traced to its jurisprudential foundation in `lex/lv2/`

## Contents

### known_laws.scm

A comprehensive collection of 60+ fundamental legal maxims organized by category:

#### General Legal Principles (13)
- **pacta-sunt-servanda**: Agreements must be kept
- **consensus-ad-idem**: Meeting of the minds
- **nemo-plus-iuris**: No one can transfer more rights than they have
- **audi-alteram-partem**: Hear the other side
- **nemo-iudex-in-causa-sua**: No one should be a judge in their own cause
- **lex-specialis-derogat-legi-generali**: Specific law overrides general law
- And more...

#### Criminal Law Principles (4)
- **nullum-crimen-sine-lege**: No crime without law
- **nulla-poena-sine-lege**: No punishment without law
- **in-dubio-pro-reo**: When in doubt, for the accused
- **actus-non-facit-reum-nisi-mens-sit-rea**: Requires both act and guilty mind

#### Delict/Tort Principles (4)
- **damnum-injuria-datum**: Loss wrongfully caused
- **volenti-non-fit-injuria**: No injury to one who consents
- **culpa**: Fault or negligence
- **res-ipsa-loquitur**: The thing speaks for itself

#### Constitutional Principles (4)
- **supremacy-of-constitution**: Constitution is supreme
- **rule-of-law**: Everyone equal before law
- **separation-of-powers**: Division of government powers
- **ubuntu**: African philosophy of interconnectedness

#### Administrative Law Principles (4)
- **legality**: Administrative action must be authorized
- **rationality**: Decisions must be rational
- **procedural-fairness**: Fair procedures required
- **legitimate-expectation**: Reasonable expectations protected

#### Equity Principles (4)
- **equity-will-not-suffer-a-wrong-without-remedy**: Equity provides remedies
- **he-who-seeks-equity-must-do-equity**: Must act fairly to receive equity
- **equality-is-equity**: Treat all equally
- **equity-follows-the-law**: Supplement but don't contradict

#### Evidence Principles (4)
- **onus-probandi**: Burden of proof
- **best-evidence-rule**: Original evidence preferred
- **relevance**: Evidence must be relevant
- **hearsay-rule**: Hearsay generally inadmissible

#### Statutory Interpretation Principles (4)
- **literal-rule**: Ordinary meaning of words
- **golden-rule**: Literal unless absurd
- **mischief-rule**: Suppress mischief, advance remedy
- **purposive-approach**: Interpret by purpose

#### Time and Limitation Principles (3)
- **tempus-regit-actum**: Time governs the act
- **prescription**: Rights lost through inaction
- **laches**: Delay can bar relief

#### Remedies Principles (3)
- **restitutio-in-integrum**: Restoration to original position
- **specific-performance**: Actual performance ordered
- **injunction**: Court order to do/refrain

#### Legal Capacity Principles (2)
- **doli-incapax**: Incapable of crime
- **compos-mentis**: Of sound mind

#### Good Faith Principles (3)
- **bona-fides**: Good faith
- **contra-bonos-mores**: Against good morals
- **ex-turpi-causa-non-oritur-actio**: No action from dishonourable cause

#### Relationship Principles (2)
- **qui-facit-per-alium-facit-per-se**: Acts through another
- **respondeat-superior**: Employer liability

#### Causation Principles (2)
- **causa-sine-qua-non**: But-for causation
- **novus-actus-interveniens**: Intervening act breaks chain

## Integration with Inference Engine

The first-order principles in this directory integrate with the inference engine (`models/ggmlex/hypergraphql/inference.py`) as follows:

### Level 1 Properties
```python
{
    "inference_level": 1,
    "confidence": 1.0,
    "inference_type": "FIRST_ORDER_PRINCIPLE",
    "source": "known_laws.scm"
}
```

### Derivation Examples

**Inductive Inference** (Level 1 → Level 2):
```scheme
;; Level 1 principles
(audi-alteram-partem)  ;; Hear the other side
(nemo-iudex-in-causa-sua)  ;; No one judge in own cause
(procedural-fairness)  ;; Fair procedures required

;; Inferred Level 2 meta-principle
→ "Natural justice requires fair hearing and impartial adjudication"
   (confidence: 0.85)
```

**Abductive Inference** (Level 1 → Level 3):
```scheme
;; Level 1 observations
(actus-non-facit-reum-nisi-mens-sit-rea)  ;; Guilty act + guilty mind
(culpa)  ;; Fault required
(bona-fides)  ;; Good faith

;; Abduced Level 3 higher meta-principle
→ "Legal liability requires mental culpability for fairness"
   (confidence: 0.65)
```

## Usage

### Loading Known Laws

```python
from models.ggmlex.hypergraphql import HypergraphQLEngine

# Load hypergraph with known laws
engine = HypergraphQLEngine()

# Get all Level 1 first-order principles
known_laws = engine.get_first_order_principles()
print(f"Loaded {len(known_laws.nodes)} known legal principles")

# Filter by category
contract_principles = [
    law for law in known_laws.nodes 
    if "pacta" in law.name.lower() or "consensus" in law.name.lower()
]
```

### Deriving Higher Principles

```python
from models.ggmlex.hypergraphql import InferenceEngine, InferenceType

# Create inference engine
inference = InferenceEngine(engine)

# Select related known laws
procedural_laws = [
    law for law in known_laws.nodes
    if "audi-alteram-partem" in law.content or 
       "procedural-fairness" in law.content or
       "nemo-iudex" in law.content
]

# Infer meta-principle
result = inference.infer_principles(
    source_nodes=procedural_laws,
    inference_type=InferenceType.INDUCTIVE,
    target_level=2
)

print(f"Inferred: {result.principle.name}")
print(f"Confidence: {result.principle.confidence}")
```

### Tracing Derivations

```python
# Get frameworks derived from known law
frameworks = engine.query_derived_from(
    known_law="pacta-sunt-servanda"
)

# Shows all contract law rules derived from this principle
for framework in frameworks.nodes:
    print(f"- {framework.name} (level {framework.inference_level})")
```

## Relationship to Scheme Frameworks

The scheme frameworks in other `lex/` directories are derived from these known laws:

| Framework | Known Laws Used |
|-----------|----------------|
| `lex/civ/za/` | pacta-sunt-servanda, nemo-plus-iuris, consensus-ad-idem, damnum-injuria-datum |
| `lex/cri/za/` | nullum-crimen-sine-lege, actus-non-facit-reum-nisi-mens-sit-rea, in-dubio-pro-reo |
| `lex/con/za/` | supremacy-of-constitution, rule-of-law, separation-of-powers, ubuntu |
| `lex/admin/za/` | audi-alteram-partem, legality, rationality, procedural-fairness |

## Relationship to Legal Foundations (Level 2)

First-order principles are derived from jurisprudential theories in `lex/lv2/`:

| First-Order Principle | Derived From (Level 2) |
|----------------------|------------------------|
| pacta-sunt-servanda, consensus-ad-idem | will-theory, contract-theory |
| rule-of-law, human-dignity | natural-law-theory, constitutional-theory |
| nullum-crimen-sine-lege, nulla-poena-sine-lege | legal-positivism |
| audi-alteram-partem, nemo-iudex-in-causa-sua | procedural-fairness-theory, natural-law-theory |
| ubuntu | ubuntu-philosophy, African-legal-philosophy |
| restitutio-in-integrum, damnum-injuria-datum | corrective-justice, tort-theory |
| supremacy-of-constitution | constitutional-supremacy-theory |
| literal-rule, golden-rule | textualism, purposivism |
| stare-decisis | legal-realism, predictive-theory-of-law |

See `lex/lv2/README.md` for comprehensive documentation of legal foundations.

## Contributing

When adding new known laws:

1. Ensure they are universally recognized legal maxims
2. Provide both Latin term and English translation
3. Add to appropriate category section
4. Include in combine-known-laws function if related to other laws
5. Maintain confidence = 1.0 (first-order principles are axiomatic)

## References

### Legal Theory
- Hart, H.L.A. "The Concept of Law" (1961)
- Dworkin, Ronald. "Taking Rights Seriously" (1977)
- Van der Walt, J.W.G. "Law of Property" (2014)

### Legal Maxims
- Broom, Herbert. "A Selection of Legal Maxims" (1845)
- Hiemstra, V.G. "Handbook on Legal Latin" (1999)

### South African Law
- Constitution of South Africa, 1996
- Neethling, J. et al. "Law of Delict" (2015)
- Christie, R.H. "The Law of Contract in South Africa" (2016)

## See Also

- **Legal Foundations (Level 2)**: `lex/lv2/README.md`
- **Inference Engine**: `models/ggmlex/INFERENCE_ENGINE_README.md`
- **HypergraphQL**: `models/ggmlex/README.md`
- **Legal Frameworks**: `lex/README.md`
- **Testing**: `models/ggmlex/test_inference_engine.py`
