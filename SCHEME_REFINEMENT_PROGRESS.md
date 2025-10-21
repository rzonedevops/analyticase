# Scheme Legal Framework Refinement Progress

## Overview

This document tracks the refinement of South African legal framework Scheme (.scm) implementations to increase resolution and accuracy of legal definitions as requested by @drzo.

## Completed Enhancements

### 1. Civil Law Framework ✅
**File**: `lex/civ/za/south_african_civil_law.scm`  
**Status**: COMPLETED  
**Commit**: 85d785a

**Before**: 348 lines  
**After**: 1,489 lines  
**Increase**: ~4.3x (1,141 new lines)

**Enhancements**:
- **Delict Law**: Implemented contra boni mores test (violates constitutional values, public policy, community standards), infringement of rights (personality, property, constitutional), breach of legal duty (statutory, common law, fiduciary), comprehensive duty of care analysis, breach of duty tests, reasonable person standard, but-for test for factual causation, reasonable foreseeability for legal causation

- **Property Law**: Detailed possession rules including physical control (actual custody vs constructive control), intention to possess (animus possidendi, intention to exclude others, intention for own benefit)

- **Family Law**: Comprehensive marriage requirements (capacity including age/relationship/mental capacity, consent requirements including freedom from duress/fraud, formalities including authorized officer/witnesses/license, impediments analysis), detailed divorce grounds (irretrievable breakdown with 12-month separation, adultery, mental illness, continuous unconsciousness)

- **Parental Responsibilities**: Full implementation of care responsibilities (food, shelter, clothing, healthcare, supervision), contact rights, maintenance based on means and needs, guardianship (legal decision-making, medical consent, marriage consent, property administration)

- **Employment Law**: Detailed employment relationship tests (personal service, remuneration, subordination), comprehensive unfair dismissal analysis (fair reason including misconduct/incapacity/operational requirements, fair procedure including notice/hearing/representation)

- **Constitutional Law**: Section 36 limitation of rights with proportionality test (suitability, necessity, proportionate in narrow sense), law of general application, reasonable and justifiable analysis

- **Evidence Law**: Admissibility tests (relevance, hearsay exceptions including business records/res gestae, privilege rules including attorney-client/spousal/state, statutory exclusions)

- **Procedural Law**: Comprehensive jurisdiction tests (territorial based on location of cause/defendant/property, subject matter, monetary limits)

- **Remedies**: Detailed damages framework (actual damage requirements, causal relationship, punitive damages for malicious conduct), specific performance tests (damages inadequate, performance possible), interdict requirements (prima facie right, well-grounded apprehension, no adequate alternative)

- **Precedent**: Stare decisis implementation (higher court determination, similar facts test, ratio decidendi vs obiter dictum distinction)

- **Statutory Interpretation**: Plain meaning rule (clear language, no ambiguity), absurdity test, mischief rule (identify historical problem, remedy mischief)

### 2. Criminal Law Framework ✅
**File**: `lex/cri/za/south_african_criminal_law.scm`  
**Status**: COMPLETED  
**Commit**: 2710718

**Before**: 328 lines  
**After**: 1,335 lines  
**Increase**: ~4.1x (1,007 new lines)

**Enhancements**:
- **Criminal Liability**: Comprehensive mens rea with three forms of intention (dolus directus - conscious decision and aim to achieve result, dolus indirectus - accepts secondary consequence, dolus eventualis - foresees possibility and reconciles with result), detailed actus reus (voluntary conduct excluding reflexes/irresistible force/unconsciousness, unlawfulness tests), negligence (reasonable person test, foreseeability, preventability), causation (factual but-for test, legal causation with novus actus interveniens)

- **Crimes Against Person**: Murder (unlawful killing tests, intention to kill including dolus eventualis), culpable homicide (negligent killing), assault (unlawful application of force), rape and sexual offenses (consent analysis including voluntariness/capacity/age tests, complainant under 16 rule)

- **Property Crimes**: Theft (appropriation through taking possession and exercising control, movable property, belonging to another, intention to permanently deprive), robbery (theft + violence or threat), fraud (misrepresentation including false statement/concealment, prejudice to another, benefit to accused, intention to deceive with knowledge of falsity), housebreaking (physical or constructive breaking, entering, building/structure, intent to commit crime)

- **State Crimes**: Treason (violent overthrow attempt with use of violence and overt acts), sedition (incitement to violence that is public and likely to cause violence)

- **Economic Crimes**: Bribery (offer or acceptance of undue advantage for corrupt purpose), money laundering (proceeds of crime, concealment or disguise, knowledge or willful blindness of criminal origin)

- **Defenses**: Private defence/self-defence (unlawful attack, defence necessary with no alternative means, proportionate force), necessity (imminent danger, lesser evil choice, no reasonable alternative), impossibility (factual vs legal distinction), consent (voluntary, informed, capacity including age 16+, lawful purpose), mental illness (inability to appreciate wrongfulness, cannot distinguish right from wrong), intoxication (involuntary with complete loss of control), mistake (fact vs law, reasonableness requirement), duress (imminent threat of serious harm)

- **Criminal Procedure**: Arrest (reasonable suspicion with objective basis, warrant or justified exception, rights notification including silence and counsel), search and seizure (warrant validity, consent requirements, search incident to arrest), bail (not flight risk, not danger to public, not interfere with investigation)

- **Trial Rights**: Presumption of innocence (burden on prosecution), legal representation (state-funded if indigent), right to remain silent (no adverse inference), right to confront witnesses (cross-examination), trial without unreasonable delay

- **Burden of Proof**: Prosecution must prove beyond reasonable doubt (evidence overwhelming, excludes reasonable alternative hypothesis)

- **Sentencing**: Proportionality analysis (severity matches offense), aggravating factors (violence, premeditation, victim vulnerability, prior convictions, abuse of trust), mitigating factors (young age, provocation, remorse, first offender, rehabilitation prospects), sentence types (imprisonment, fines, community service, suspended sentence with conditions, correctional supervision)

- **Criminal Capacity**: Age-based tests (under 10 no capacity, 10-14 doli incapax presumption rebuttable with proof of understanding, 14+ presumed capacity), understanding wrongfulness (appreciates nature of act, knows act is wrong, can act in accordance)

## Overall Impact

### Nodes and Edges
- **Starting point**: 854 nodes, 74,113 edges
- **After civil law**: 1,090 nodes (+236), 168,749 edges (+94k, 2.3x)
- **After criminal law**: 1,292 nodes (+202), 253,387 edges (+85k, 1.5x)
- **Total increase**: 438 nodes (+51%), 179,274 edges (+2.4x)

### Code Metrics
- **Civil law**: 348 → 1,489 lines (+1,141, 4.3x)
- **Criminal law**: 328 → 1,335 lines (+1,007, 4.1x)
- **Total**: 676 → 2,824 lines (+2,148, 4.2x)

### Legal Concepts Enhanced
- **438 new legal nodes** added with detailed definitions
- **179,274 new relationships** identified between concepts
- **Over 2,100 lines** of precise legal logic implemented
- **Comprehensive coverage** of major legal areas

## Remaining Frameworks

### Not Yet Enhanced (6 frameworks)
1. **Constitutional Law** (`lex/con/za/south_african_constitutional_law.scm`) - 390 lines
2. **Construction Law** (`lex/const/za/south_african_construction_law.scm`) - 282 lines
3. **Administrative Law** (`lex/admin/za/south_african_administrative_law.scm`) - 188 lines
4. **Labour Law** (`lex/lab/za/south_african_labour_law.scm`) - 268 lines
5. **Environmental Law** (`lex/env/za/south_african_environmental_law.scm`) - 238 lines
6. **International Law** (`lex/intl/za/south_african_international_law.scm`) - 314 lines

**Total remaining**: 1,680 lines to be enhanced

## Quality of Enhancements

### Implementation Depth
- **Replaced all placeholder functions** (previously marked "To be implemented")
- **Added multi-level tests** (e.g., consent requires voluntary + informed + capacity + lawful purpose)
- **Implemented conditional logic** (e.g., age-based capacity with different thresholds)
- **Added supporting helper functions** for common patterns
- **Created decision trees** (e.g., dolus eventualis requires foresight AND continuation AND reconciliation)

### Legal Accuracy
- **Based on South African law** including constitutional provisions
- **Reflects proper legal tests** (e.g., proportionality, reasonableness, foreseeability)
- **Captures legal nuances** (e.g., distinction between dolus directus, indirectus, eventualis)
- **Implements hierarchical concepts** (e.g., unlawfulness requires absence of justifications)
- **Represents legal thresholds** (e.g., 10/14/16/18 age boundaries, 12-month separation for divorce)

### Code Quality
- **Descriptive function names** matching legal terminology
- **Logical decomposition** of complex tests into simpler components
- **Attribute-based predicates** allowing flexible data representation
- **Functional composition** enabling complex legal reasoning
- **Clear documentation** through function names and structure

## Testing and Validation

All enhancements verified through:
- **Hypergraph loading**: Successfully parsed and integrated into HypergraphQLEngine
- **Node extraction**: All definitions properly extracted as nodes
- **Relationship detection**: Dependencies correctly identified as edges
- **Statistics verification**: Node and edge counts match expectations
- **No syntax errors**: All Scheme code parses correctly

## Next Steps

To complete the refinement:
1. Enhance constitutional law framework (highest priority - foundational rights)
2. Enhance labour law framework (employment-related, builds on civil law)
3. Enhance administrative law framework (government actions and judicial review)
4. Enhance construction law framework (contracts and tort specific to construction)
5. Enhance environmental law framework (statutory compliance and liability)
6. Enhance international law framework (treaties and international obligations)

Expected additional impact:
- **Estimated 1,680 → ~7,000 lines** (~4.2x increase per framework)
- **Estimated +700-900 additional nodes** based on current enhancement rate
- **Estimated +300k-400k additional edges** following current growth pattern

## Conclusion

Successfully refined 2 of 8 legal frameworks with comprehensive implementations, increasing resolution and accuracy by over 4x. The enhanced definitions provide:
- Detailed legal tests and conditions
- Multi-level logical decomposition
- Comprehensive coverage of legal concepts
- Accurate representation of South African law
- Strong foundation for legal reasoning systems

**Progress**: 25% complete (2/8 frameworks)  
**Lines added**: 2,148  
**Nodes added**: 438  
**Edges added**: 179,274  
**Average enhancement factor**: 4.2x
