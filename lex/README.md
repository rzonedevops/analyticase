# Legal Framework (lex) Directory v2.2

## Overview

This directory contains the enumerated Scheme (.scm) representations of the AnalytiCase legal framework. The framework is structured hierarchically to enable multi-level legal reasoning, from abstract jurisprudential theories down to concrete jurisdiction-specific rules.

## Framework Version: 2.2

**Last Updated**: 2025-11-02

**Enhancements in v2.2**:

- **Expanded Meta-Principles**: The Level 2 framework has been expanded from 15 to 22 jurisprudential theories, including Critical Legal Studies, Feminist Jurisprudence, Economic Analysis of Law, and Ubuntu Jurisprudence. See `lex/lv2/legal_foundations_v2.2.scm`.
- **Improved Integration**: Jurisdiction-specific frameworks now directly integrate with Level 1 first-order principles, with explicit case law and statutory references. See `lex/civ/za/south_african_civil_law_v2.2.scm` for the implementation template.
- **Quantitative Metrics**: The framework includes confidence scores, influence metrics, and temporal evolution tracking for all principles.
- **Detailed Progress Report**: See [Scheme Legal Framework Refinement Progress](SCHEME_REFINEMENT_PROGRESS_2025-11-02.md) for a detailed log of the v2.2 enhancements.

## Directory Structure

```
lex/
├── lv2/                     # Inference Level 2 - Meta-Principles (Legal Foundations)
│   ├── legal_foundations_v2.2.scm # 22 known jurisprudential theories and philosophies
│   └── README.md            # Documentation of legal foundations
├── lv1/                     # Inference Level 1 - First-Order Principles
│   ├── known_laws_enhanced.scm # 60+ fundamental legal maxims and principles
│   └── README.md            # Documentation of first-order principles
├── cri/                    # Criminal Law
│   └── za/                 # South African Criminal Law
├── civ/                    # Civil Law
│   └── za/                 # South African Civil Law (v2.2)
├── ... (and 6 other legal branches)
```

## Inference Level Hierarchy

The legal framework is organized into inference levels, reflecting the abstraction hierarchy of legal reasoning:

### Level 2: Meta-Principles (`lv2/`)

The jurisprudential foundations layer containing 22 known legal theories and philosophical frameworks, including:

- Natural Law Theory
- Legal Positivism
- Legal Realism
- Interpretive Theory (Dworkin)
- **Critical Legal Studies (New in v2.2)**
- **Feminist Jurisprudence (New in v2.2)**
- **Economic Analysis of Law (New in v2.2)**
- **Ubuntu Jurisprudence (New in v2.2)**
- **Restorative Justice Theory (New in v2.2)**
- **Critical Race Theory (New in v2.2)**

These meta-principles provide the theoretical grounding from which first-order principles are derived.

### Level 1: First-Order Principles (`lv1/`)

The foundational layer containing 60+ universally recognized legal maxims and principles, such as `pacta-sunt-servanda`, `audi-alteram-partem`, and `nemo-plus-iuris`.

### Level 0+: Derived Legal Frameworks

The jurisdiction-specific frameworks (`civ/za/`, `cri/za/`, etc.) are derived from Level 1 first-order principles through deductive, inductive, abductive, and analogical reasoning.

## Legal Framework Coverage

This directory contains comprehensive Scheme-based implementations of South African law across 8 major legal branches. The v2.2 enhancement has been fully implemented for the Civil Law framework, which serves as a template for other domains.

## Statistics (v2.2)

- **Level 2 Meta-Principles**: 22 known legal foundations and jurisprudential theories
- **Level 1 First-Order Principles**: 60+ fundamental legal maxims and principles
- **Total Legal Principles (ZA Civil)**: 45 (enhanced in v2.2)

## Integration with Simulation Models

The enhanced legal frameworks are now integrated with all v2.2 simulation models, enabling principle-aware analysis and more realistic simulation of legal system dynamics. The `unified_simulation_runner_v2.2.py` demonstrates how these frameworks are loaded and utilized.

## Testing

Run the legal framework integration tests:
```bash
python models/ggmlex/test_legal_frameworks.py
```

## Usage

This framework provides the foundational structure for implementing:
- Legal reasoning systems
- Expert systems for legal analysis
- Automated legal document analysis
- Case prediction systems
- Compliance checking tools
- Legal education platforms
