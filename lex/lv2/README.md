# Level 2: Meta-Principles (Legal Foundations)

## Overview

This directory contains the **legal foundations** - the known jurisprudential theories and philosophical frameworks from which first-order legal principles are derived. These are **inference level 2** meta-principles that provide the theoretical underpinning for all legal reasoning in the AnalytiCase framework.

## Inference Level Hierarchy

```
Level 2 (lv2): Meta-Principles (This Layer) - Legal Foundations/Theories
    ↓ Deductive/Abductive Inference
Level 1 (lv1): First-Order Principles - Legal Maxims
    ↓ Inductive/Abductive Inference  
Level 0: Enumerated Laws - Specific Legal Rules
```

## Purpose

Level 2 meta-principles serve as the theoretical foundation for:

1. **Jurisprudential Grounding**: All legal maxims trace back to fundamental legal theories
2. **Theoretical Coherence**: Ensures legal principles align with established legal philosophy
3. **Cross-Jurisdictional Universality**: Meta-principles transcend specific jurisdictions
4. **Legal Reasoning Framework**: Provides the "why" behind legal principles
5. **Scholarly Foundation**: Connects practice to academic legal theory

## Contents

### legal_foundations.scm

A comprehensive collection of known legal theories and jurisprudential frameworks organized by school of thought:

#### 1. Natural Law Theory
**Core Idea**: Law must conform to universal moral principles and human reason

- **natural-law-theory**: Universal moral principles as foundation of valid law
- **eternal-law**: Divine reason governing all creation (Aquinas)
- **natural-moral-law**: Moral principles accessible to human reason
- **human-dignity-principle**: Inherent worth and inviolability of persons

**Key Thinkers**: Aristotle, Thomas Aquinas, John Finnis, Lon Fuller

**Derived Level 1 Principles**:
- rule-of-law (law must be just and reasonable)
- human-dignity (constitutional rights)
- contra-bonos-mores (against good morals)
- bona-fides (good faith)

---

#### 2. Legal Positivism
**Core Idea**: Law is defined by social facts and authoritative sources, separate from morality

- **legal-positivism**: Law as system of human-created rules
- **rule-of-recognition**: Social rule identifying valid law (H.L.A. Hart)
- **grundnorm**: Basic norm presupposed as valid (Hans Kelsen)
- **separation-thesis**: Law and morality are conceptually distinct

**Key Thinkers**: John Austin, Hans Kelsen, H.L.A. Hart, Joseph Raz

**Derived Level 1 Principles**:
- nullum-crimen-sine-lege (no crime without law)
- legality (administrative action must be authorized)
- lex-posterior-derogat-legi-priori (later law prevails)
- literal-rule (ordinary meaning of words)

---

#### 3. Legal Realism
**Core Idea**: Law is what courts and officials actually do, not abstract rules

- **legal-realism**: Law as prediction of judicial behavior
- **predictive-theory-of-law**: Focus on actual decisions (Oliver Wendell Holmes)
- **sociological-jurisprudence**: Law responds to social needs (Roscoe Pound)

**Key Thinkers**: Oliver Wendell Holmes Jr., Karl Llewellyn, Jerome Frank, Roscoe Pound

**Derived Level 1 Principles**:
- stare-decisis (precedent binding)
- purposive-approach (interpret by purpose)
- contextual-interpretation (social context matters)

---

#### 4. Interpretive Theory (Ronald Dworkin)
**Core Idea**: Law as integrity - best interpretation of community's political practices

- **law-as-integrity**: Constructive interpretation of legal practice
- **rights-thesis**: Rights as trumps against collective goals
- **principle-policy-distinction**: Principles protect rights; policies promote goals

**Key Thinker**: Ronald Dworkin

**Derived Level 1 Principles**:
- rights-based-adjudication (individual rights paramount)
- purposive-interpretation (coherent reading)
- judicial-review (protecting individual rights)

---

#### 5. African Legal Philosophy
**Core Idea**: Community-centered values and restorative justice

- **ubuntu-philosophy**: "I am because we are" - interconnectedness and humanity
- **communitarian-ethics**: Individual identity from community membership
- **restorative-justice**: Focus on healing and reconciliation

**Key Concepts**: Ubuntu, customary law, community participation

**Derived Level 1 Principles**:
- ubuntu (humanity towards others)
- restorative-justice (reconciliation over punishment)
- community-participation (stakeholder involvement)

---

#### 6. Critical Legal Studies
**Core Idea**: Law perpetuates power structures; requires critical examination

- **legal-indeterminacy**: Legal rules inherently indeterminate
- **law-and-power**: Law reflects and reinforces hierarchies

**Key Thinkers**: Duncan Kennedy, Roberto Unger, Critical Race Theorists

**Derived Level 1 Principles**:
- substantive-equality (address historical disadvantage)
- transformative-constitutionalism (social transformation)
- contextual-interpretation (power dynamics matter)

---

#### 7. Feminist Jurisprudence
**Core Idea**: Address gender-based injustice and promote substantive equality

- **substantive-equality**: Address historical disadvantage, not just formal equality
- **care-ethics**: Moral reasoning based on relationships and care

**Key Thinkers**: Catharine MacKinnon, Martha Nussbaum, Carol Gilligan

**Derived Level 1 Principles**:
- equal-protection (substantive equality)
- anti-discrimination (affirmative action)
- child-centered-justice (care-based reasoning)

---

#### 8. Economic Analysis of Law
**Core Idea**: Law should promote efficiency and wealth maximization

- **efficiency-principle**: Minimize transaction costs, maximize social wealth
- **coase-theorem**: Efficient outcomes through bargaining (Ronald Coase)

**Key Thinkers**: Richard Posner, Guido Calabresi, Ronald Coase

**Derived Level 1 Principles**:
- property-rights (efficient allocation)
- liability-rules (internalize externalities)
- contract-default-rules (minimize transaction costs)

---

#### 9. Procedural Justice Theory
**Core Idea**: Fair procedures essential for legitimate legal outcomes

- **procedural-fairness-theory**: Justice requires fair process
- **adversarial-system**: Truth from contest before neutral arbiter
- **inquisitorial-system**: Court actively investigates truth

**Derived Level 1 Principles**:
- audi-alteram-partem (hear the other side)
- nemo-iudex-in-causa-sua (no judge in own cause)
- procedural-fairness (fair hearing required)

---

#### 10. Constitutional Theory
**Core Idea**: Principles of constitutional governance and rights protection

- **constitutional-supremacy-theory**: Constitution as supreme law
- **transformative-constitutionalism**: Constitution for social transformation
- **living-tree-doctrine**: Constitution evolves with society

**Derived Level 1 Principles**:
- supremacy-of-constitution (constitutional supremacy)
- separation-of-powers (division of government)
- judicial-review (constitutional oversight)

---

#### 11. Contract Theory
**Core Idea**: Philosophical bases for binding contractual obligations

- **will-theory**: Obligation from autonomous will
- **reliance-theory**: Protect reasonable reliance
- **efficiency-theory**: Facilitate voluntary exchange

**Derived Level 1 Principles**:
- pacta-sunt-servanda (agreements must be kept)
- consensus-ad-idem (meeting of minds)
- freedom-of-contract (autonomy in contracting)

---

#### 12. Tort/Delict Theory
**Core Idea**: Justifications for civil liability

- **corrective-justice**: Correct wrongful gains and losses
- **distributive-justice**: Distribute risks by social policy
- **deterrence-theory**: Deter harmful conduct

**Derived Level 1 Principles**:
- restitutio-in-integrum (restoration to original position)
- damnum-injuria-datum (loss wrongfully caused)
- fault-based-liability (negligence standard)

---

#### 13. Criminal Law Theory
**Core Idea**: Justifications for criminalization and punishment

- **retributive-justice**: Punishment as deserved response (just deserts)
- **utilitarian-theory**: Punishment for deterrence, rehabilitation
- **expressive-theory**: Criminal law expresses social condemnation

**Derived Level 1 Principles**:
- proportionality (punishment fits crime)
- actus-non-facit-reum-nisi-mens-sit-rea (act + guilty mind)
- rehabilitation (reform offenders)

---

#### 14. Property Theory
**Core Idea**: Justifications for property rights

- **labor-theory**: Rights from mixing labor with resources (John Locke)
- **utilitarian-property-theory**: Maximize utility through incentives
- **personality-theory**: Property for self-development (Hegel)

**Derived Level 1 Principles**:
- nemo-dat-quod-non-habet (no one gives what they don't have)
- acquisition-by-labor (sweat equity)
- exclusion-rights (owner control)

---

#### 15. Evidence Theory
**Core Idea**: Principles for rational fact-finding

- **rational-proof-theory**: Ensure rational inference
- **truth-finding-theory**: Maximize accurate fact-finding
- **procedural-fairness-evidence**: Fair trial and prejudice protection

**Derived Level 1 Principles**:
- relevance (evidence must be relevant)
- best-evidence-rule (original preferred)
- hearsay-rule (hearsay inadmissible)

---

#### 16. Administrative Law Theory
**Core Idea**: Principles constraining administrative power

- **rule-of-law-theory**: Power exercised according to law
- **accountability-theory**: Administrative bodies must be accountable
- **regulatory-theory**: Balance regulation with rights

**Derived Level 1 Principles**:
- legality (action must be authorized)
- rationality (decisions must be rational)
- judicial-review (oversight of administration)

---

#### 17. Remedies Theory
**Core Idea**: Principles for legal remedies

- **compensation-principle**: Restore to position before wrong
- **deterrence-principle**: Deter future wrongdoing
- **equity-principle**: Equitable remedies when legal inadequate

**Derived Level 1 Principles**:
- restitutio-in-integrum (restoration)
- specific-performance (actual performance)
- injunction (court order)

---

#### 18. Statutory Interpretation Theory
**Core Idea**: Approaches to interpreting legislation

- **textualism**: Ordinary meaning of text
- **purposivism**: Advance underlying purpose
- **intentionalism**: Legislative intent

**Derived Level 1 Principles**:
- literal-rule (ordinary meaning)
- purposive-approach (interpret by purpose)
- mischief-rule (suppress mischief)

---

#### 19. International Law Theory
**Core Idea**: Nature and authority of international law

- **dualism**: International and domestic law separate
- **monism**: Single legal system
- **sovereignty-theory**: State consent as basis

**Derived Level 1 Principles**:
- treaty-ratification (state consent)
- customary-international-law (state practice)
- state-immunity (sovereign equality)

---

## Derivation Examples

### Example 1: Natural Law → First-Order Principles

```scheme
;; Level 2 meta-principle
(natural-law-theory)
  "Laws derive authority from universal moral principles"

;; Inferred Level 1 principles
→ (rule-of-law)       ;; Law must be just and reasonable
→ (human-dignity)     ;; Inherent worth of persons
→ (bona-fides)        ;; Good faith required
→ (equity-principles) ;; Fairness in application

;; Confidence: 0.9 (strong theoretical foundation)
;; Inference type: Deductive (from general theory to specific principles)
```

### Example 2: Legal Positivism → First-Order Principles

```scheme
;; Level 2 meta-principle
(legal-positivism)
  "Law defined by authoritative sources, separate from morality"

;; Inferred Level 1 principles
→ (nullum-crimen-sine-lege)  ;; No crime without law
→ (legality)                  ;; Must be legally authorized
→ (literal-rule)              ;; Ordinary meaning of words
→ (rule-of-recognition)       ;; Criteria for valid law

;; Confidence: 0.9 (well-established theory)
;; Inference type: Deductive
```

### Example 3: Ubuntu Philosophy → First-Order Principles

```scheme
;; Level 2 meta-principle
(ubuntu-philosophy)
  "I am because we are - interconnectedness and humanity"

;; Inferred Level 1 principles
→ (ubuntu)                    ;; Humanity towards others
→ (restorative-justice)       ;; Healing and reconciliation
→ (community-participation)   ;; Stakeholder involvement
→ (substantive-equality)      ;; Address historical disadvantage

;; Confidence: 0.85 (context-specific but influential)
;; Inference type: Deductive + Cultural context
```

## Integration with Inference Engine

The legal foundations integrate with the inference engine (`models/ggmlex/hypergraphql/inference.py`) as follows:

### Level 2 Properties
```python
{
    "inference_level": 2,
    "confidence": 0.85-0.95,  # High but not absolute (theoretical)
    "inference_type": "META_PRINCIPLE",
    "source": "legal_foundations.scm",
    "category": "jurisprudential_theory"
}
```

### Derivation Chain
```
Level 2 (Meta-Principles): Jurisprudential theories
    ↓ Deductive inference
Level 1 (First-Order Principles): Legal maxims and principles
    ↓ Inductive inference
Level 0 (Enumerated Laws): Specific laws in jurisdictions
```

## Relationship to First-Order Principles

| Legal Foundation | Derived Level 1 Principles |
|-----------------|---------------------------|
| Natural Law Theory | rule-of-law, human-dignity, contra-bonos-mores, bona-fides, equity principles |
| Legal Positivism | nullum-crimen-sine-lege, legality, literal-rule, separation-thesis |
| Legal Realism | stare-decisis, purposive-approach, contextual-interpretation |
| Ubuntu Philosophy | ubuntu, restorative-justice, community-participation |
| Procedural Justice | audi-alteram-partem, nemo-iudex-in-causa-sua, procedural-fairness |
| Constitutional Theory | supremacy-of-constitution, separation-of-powers, judicial-review |
| Contract Theory | pacta-sunt-servanda, consensus-ad-idem, freedom-of-contract |
| Tort/Delict Theory | restitutio-in-integrum, damnum-injuria-datum, fault-based-liability |
| Criminal Law Theory | proportionality, actus-non-facit-reum-nisi-mens-sit-rea |
| Property Theory | nemo-dat-quod-non-habet, acquisition-by-labor, exclusion-rights |

## Usage

### Loading Legal Foundations

```python
from models.ggmlex.hypergraphql import HypergraphQLEngine

# Load hypergraph with legal foundations
engine = HypergraphQLEngine()

# Get all Level 2 meta-principles
foundations = engine.get_meta_principles()
print(f"Loaded {len(foundations.nodes)} legal foundations")

# Filter by jurisprudential school
natural_law = [
    foundation for foundation in foundations.nodes 
    if "natural-law" in foundation.name.lower()
]
```

### Tracing Derivations

```python
# Trace a first-order principle to its foundation
principle = engine.get_node_by_name("pacta-sunt-servanda")

# Find the meta-principle foundation
foundation_chain = engine.trace_to_foundation(principle)

# Output:
# Level 1: pacta-sunt-servanda (agreements must be kept)
# ↑ derived from
# Level 2: will-theory (contract from autonomous will)
# ↑ part of
# Level 2: contract-theory (philosophical bases for obligations)
```

### Deriving New Principles

```python
from models.ggmlex.hypergraphql import InferenceEngine, InferenceType

# Create inference engine
inference = InferenceEngine(engine)

# Select a meta-principle
foundation = engine.get_node_by_name("procedural-fairness-theory")

# Derive new first-order principles
result = inference.infer_principles(
    source_nodes=[foundation],
    inference_type=InferenceType.DEDUCTIVE,
    target_level=1,
    context="administrative law"
)

print(f"Derived principle: {result.principle.name}")
print(f"Confidence: {result.principle.confidence}")
```

## Contributing

When adding new legal foundations:

1. Ensure they are recognized jurisprudential theories with academic support
2. Provide both the theory name and English explanation
3. Add to appropriate category section
4. Include key thinkers and references
5. Document which Level 1 principles derive from this foundation
6. Maintain confidence range 0.85-0.95 (theoretical foundations)

## References

### General Jurisprudence
- Hart, H.L.A. "The Concept of Law" (1961)
- Dworkin, Ronald. "Taking Rights Seriously" (1977)
- Finnis, John. "Natural Law and Natural Rights" (1980)
- Raz, Joseph. "The Authority of Law" (1979)
- Fuller, Lon L. "The Morality of Law" (1964)

### Legal Realism
- Holmes, Oliver Wendell Jr. "The Path of the Law" (1897)
- Llewellyn, Karl. "The Bramble Bush" (1930)
- Frank, Jerome. "Law and the Modern Mind" (1930)
- Pound, Roscoe. "An Introduction to the Philosophy of Law" (1922)

### African Legal Philosophy
- Mokgoro, Justice Yvonne. "Ubuntu and the Law in South Africa" (1998)
- Ramose, Mogobe B. "African Philosophy Through Ubuntu" (1999)
- Cornell, Drucilla & Muvangua, Nyoko. "Ubuntu and the Law" (2012)
- Bennett, T.W. "Customary Law in South Africa" (2004)

### Critical Approaches
- Kennedy, Duncan. "Legal Education and the Reproduction of Hierarchy" (1982)
- MacKinnon, Catharine. "Toward a Feminist Theory of the State" (1989)
- Crenshaw, Kimberlé. "Critical Race Theory" (1995)
- Unger, Roberto. "The Critical Legal Studies Movement" (1986)

### Economic Analysis
- Posner, Richard. "Economic Analysis of Law" (9th ed. 2014)
- Calabresi, Guido. "The Costs of Accidents" (1970)
- Coase, Ronald. "The Problem of Social Cost" (1960)

### South African Law
- Constitution of the Republic of South Africa, 1996
- Klare, Karl. "Legal Culture and Transformative Constitutionalism" (1998)
- Van der Walt, J.W.G. "Law of Property" (2014)
- Neethling, J. et al. "Law of Delict" (2015)

### Contract Law Theory
- Fried, Charles. "Contract as Promise" (1981)
- Atiyah, P.S. "The Rise and Fall of Freedom of Contract" (1979)
- Christie, R.H. "The Law of Contract in South Africa" (2016)

### Constitutional Theory
- Ackerman, Bruce. "We the People" (1991)
- Tribe, Laurence. "American Constitutional Law" (2000)
- De Vos, Pierre et al. "South African Constitutional Law in Context" (2014)

## See Also

- **First-Order Principles**: `lex/lv1/README.md`
- **Inference Engine**: `models/ggmlex/INFERENCE_ENGINE_README.md`
- **Inference Models**: `docs/formal_specification/INFERENCE_MODELS.md`
- **Legal Frameworks**: `lex/README.md`
- **HypergraphQL**: `models/ggmlex/README.md`
