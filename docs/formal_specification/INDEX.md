# AnalytiCase Formal Specification - Index

Welcome to the AnalytiCase Z++ formal specification. This index helps you navigate the documentation.

## Quick Start

**New to formal specifications?**
1. Start with [README.md](README.md) - Overview and introduction
2. Read [NOTATION_GUIDE.md](NOTATION_GUIDE.md) - Learn Z++ notation
3. Explore [EXAMPLES.md](EXAMPLES.md) - See practical examples

**Implementing from the specification?**
1. Read [SPECIFICATION.md](SPECIFICATION.md) - Complete formal spec
2. Follow [VERIFICATION_CHECKLIST.md](VERIFICATION_CHECKLIST.md) - Verify your implementation
3. Reference [EXAMPLES.md](EXAMPLES.md) - See code examples

**Using LaTeX?**
1. Compile [analyticase_zpp_spec.tex](analyticase_zpp_spec.tex) - Full formal specification

## Documentation Files

### Core Documentation

| File | Purpose | Audience |
|------|---------|----------|
| [README.md](README.md) | Overview, introduction, and guide | All users |
| [SPECIFICATION.md](SPECIFICATION.md) | Complete Z++ formal specification (Markdown) | Developers, Researchers |
| [analyticase_zpp_spec.tex](analyticase_zpp_spec.tex) | Complete Z++ formal specification (LaTeX) | Formal methods experts |

### Supporting Documentation

| File | Purpose | Audience |
|------|---------|----------|
| [NOTATION_GUIDE.md](NOTATION_GUIDE.md) | Z++ notation reference and tutorial | Beginners, Reference |
| [EXAMPLES.md](EXAMPLES.md) | Practical implementation examples | Developers |
| [VERIFICATION_CHECKLIST.md](VERIFICATION_CHECKLIST.md) | Implementation verification guide | QA, Developers |

## Specification Coverage

### Data Structures (Section 3)

- **Node Class**: Entities in the hypergraph
  - Specification: [SPECIFICATION.md§3.1](SPECIFICATION.md#node-class)
  - Implementation: `models/hyper_gnn/hypergnn_model.py::Node`
  - Examples: [EXAMPLES.md§1](EXAMPLES.md#basic-hypergraph-example)
  
- **Hyperedge Class**: Multi-way relationships
  - Specification: [SPECIFICATION.md§3.2](SPECIFICATION.md#hyperedge-class)
  - Implementation: `models/hyper_gnn/hypergnn_model.py::Hyperedge`
  - Examples: [EXAMPLES.md§1](EXAMPLES.md#basic-hypergraph-example)
  
- **Hypergraph Class**: Complete graph structure
  - Specification: [SPECIFICATION.md§3.3](SPECIFICATION.md#hypergraph-class)
  - Implementation: `models/hyper_gnn/hypergnn_model.py::Hypergraph`
  - Examples: [EXAMPLES.md§1](EXAMPLES.md#basic-hypergraph-example)

### Legal Case Management (Section 4)

- **Party Class**: Case participants
  - Specification: [SPECIFICATION.md§4.1](SPECIFICATION.md#party-class)
  - Examples: [EXAMPLES.md§2](EXAMPLES.md#legal-case-example)
  
- **LegalCase Class**: Complete case structure
  - Specification: [SPECIFICATION.md§4.2](SPECIFICATION.md#legalcase-class)
  - Examples: [EXAMPLES.md§2](EXAMPLES.md#legal-case-example)

### ZA Judiciary Integration (Section 5)

- **CourtOnlineCase Class**: E-filing system integration
  - Specification: [SPECIFICATION.md§5.1](SPECIFICATION.md#courtonlinecase-class)
  - Implementation: `za_judiciary_integration/api/za_judiciary_api.py::CourtOnlineCase`
  - Examples: [EXAMPLES.md§3](EXAMPLES.md#za-judiciary-integration-example)
  
- **CaseLinesBundle Class**: Evidence bundle management
  - Specification: [SPECIFICATION.md§5.3](SPECIFICATION.md#caselinesBundle-class)
  - Implementation: `za_judiciary_integration/api/za_judiciary_api.py::CaseLinesBundle`
  - Examples: [EXAMPLES.md§3](EXAMPLES.md#za-judiciary-integration-example)

### Simulation Models (Section 6)

- **Agent Class**: Case participants in simulations
  - Specification: [SPECIFICATION.md§6.1](SPECIFICATION.md#agent-class)
  - Implementation: `models/agent_based/*.py`
  - Examples: [EXAMPLES.md§4](EXAMPLES.md#simulation-example)
  
- **SimulationRun Class**: Complete simulation execution
  - Specification: [SPECIFICATION.md§6.3](SPECIFICATION.md#simulationrun-class)
  - Implementation: `simulations/*.py`
  - Examples: [EXAMPLES.md§4](EXAMPLES.md#simulation-example)

### Analysis Operations (Section 7)

- Community Detection
  - Specification: [SPECIFICATION.md§7.1](SPECIFICATION.md#community-detection)
  - Verification: [VERIFICATION_CHECKLIST.md§6.1](VERIFICATION_CHECKLIST.md#community-detection)

- Centrality Analysis
  - Specification: [SPECIFICATION.md§7.2](SPECIFICATION.md#centrality-analysis)
  - Verification: [VERIFICATION_CHECKLIST.md§6.2](VERIFICATION_CHECKLIST.md#centrality-analysis)

- Temporal Pattern Detection
  - Specification: [SPECIFICATION.md§7.3](SPECIFICATION.md#temporal-pattern-detection)
  - Verification: [VERIFICATION_CHECKLIST.md§6.3](VERIFICATION_CHECKLIST.md#temporal-pattern-detection)

- Link Prediction
  - Specification: [SPECIFICATION.md§7.4](SPECIFICATION.md#link-prediction)
  - Verification: [VERIFICATION_CHECKLIST.md§6.4](VERIFICATION_CHECKLIST.md#link-prediction)

### System Invariants (Section 8)

- Hypergraph Consistency
  - Specification: [SPECIFICATION.md§8.1](SPECIFICATION.md#hypergraph-consistency)
  - Verification: [VERIFICATION_CHECKLIST.md§7.1](VERIFICATION_CHECKLIST.md#hypergraph-consistency)
  - Example: [EXAMPLES.md§5](EXAMPLES.md#verification-example)

- Case Status Transitions
  - Specification: [SPECIFICATION.md§8.2](SPECIFICATION.md#case-status-transitions)
  - Verification: [VERIFICATION_CHECKLIST.md§7.2](VERIFICATION_CHECKLIST.md#case-status-transitions)

- Bundle Submission Rules
  - Specification: [SPECIFICATION.md§8.3](SPECIFICATION.md#bundle-submission-rules)
  - Verification: [VERIFICATION_CHECKLIST.md§7.3](VERIFICATION_CHECKLIST.md#bundle-submission-rules)

- Event Temporal Ordering
  - Specification: [SPECIFICATION.md§8.4](SPECIFICATION.md#simulation-event-ordering)
  - Verification: [VERIFICATION_CHECKLIST.md§7.4](VERIFICATION_CHECKLIST.md#event-temporal-ordering)

## Usage Paths

### Path 1: Understanding the System

```
README.md
    ↓
SPECIFICATION.md (skim)
    ↓
EXAMPLES.md (read examples)
    ↓
Use the system
```

### Path 2: Implementing from Specification

```
README.md
    ↓
NOTATION_GUIDE.md (learn notation)
    ↓
SPECIFICATION.md (study carefully)
    ↓
EXAMPLES.md (see implementation patterns)
    ↓
Implement code
    ↓
VERIFICATION_CHECKLIST.md (verify implementation)
```

### Path 3: Formal Verification

```
analyticase_zpp_spec.tex (compile to PDF)
    ↓
Use Z theorem prover (Z/EVES, Fuzz, etc.)
    ↓
Prove properties
    ↓
VERIFICATION_CHECKLIST.md (runtime verification)
```

### Path 4: Quick Reference

```
NOTATION_GUIDE.md (bookmark for quick lookup)
    ↓
SPECIFICATION.md (search for specific schemas)
    ↓
EXAMPLES.md (copy/paste example code)
```

## Key Concepts

### Z++ Notation Elements

| Concept | Definition | Documentation |
|---------|-----------|---------------|
| Schema | Specification of state and operations | [NOTATION_GUIDE.md§3](NOTATION_GUIDE.md#schemas) |
| Class | Object-oriented specification unit | [NOTATION_GUIDE.md§2](NOTATION_GUIDE.md#z-object-oriented-extensions) |
| Invariant | Property that must always hold | [SPECIFICATION.md§8](SPECIFICATION.md#system-invariants) |
| Pre-condition | Must be true before operation | [EXAMPLES.md](EXAMPLES.md) |
| Post-condition | Must be true after operation | [EXAMPLES.md](EXAMPLES.md) |

### Domain Terms

| Term | Definition | Specification |
|------|-----------|---------------|
| Hypergraph | Graph with multi-way edges | [SPECIFICATION.md§3.3](SPECIFICATION.md#hypergraph-class) |
| Node | Entity in hypergraph | [SPECIFICATION.md§3.1](SPECIFICATION.md#node-class) |
| Hyperedge | Multi-way relationship | [SPECIFICATION.md§3.2](SPECIFICATION.md#hyperedge-class) |
| Case | Legal case with parties and evidence | [SPECIFICATION.md§4.2](SPECIFICATION.md#legalcase-class) |
| Bundle | Collection of case documents | [SPECIFICATION.md§5.3](SPECIFICATION.md#caselinesBundle-class) |
| Agent | Participant in simulation | [SPECIFICATION.md§6.1](SPECIFICATION.md#agent-class) |

## Tools and Resources

### For Reading LaTeX Specification

- **Online**: [Overleaf](https://www.overleaf.com/)
- **Desktop**: TeXLive, MiKTeX
- **Package**: `zed-csp` for Z notation

### For Z Verification

- **Z/EVES**: Interactive theorem prover
- **Fuzz**: Type checker for Z
- **CZT**: Community Z Tools (Eclipse-based)

### For Testing

- **pytest**: Python testing framework
- **hypothesis**: Property-based testing
- **mypy**: Static type checking

## Frequently Asked Questions

**Q: Do I need to understand Z++ to use AnalytiCase?**

A: No. The specification is for formal verification and implementation guidance. The Markdown version (SPECIFICATION.md) is readable without Z++ expertise.

**Q: How does this relate to the code?**

A: The specification defines what the code should do. See VERIFICATION_CHECKLIST.md for mapping between specification and implementation.

**Q: Can I use this to generate tests?**

A: Yes! Pre/post-conditions can be converted to test cases. See EXAMPLES.md for property-based testing examples.

**Q: What if I find a discrepancy between spec and implementation?**

A: Report it as a bug. The specification is the authoritative definition of correct behavior.

**Q: How do I compile the LaTeX version?**

A: See README.md for compilation instructions. You need LaTeX with the `zed-csp` package.

## Contributing

When updating the specification:

1. Update the LaTeX file (`analyticase_zpp_spec.tex`)
2. Update the Markdown version (`SPECIFICATION.md`)
3. Add/update examples in `EXAMPLES.md`
4. Update verification checklist if needed
5. Update this index if adding new sections

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-22 | Initial Z++ formal specification |

## License

This formal specification is part of the AnalytiCase project and follows the same license.

## Contact

For questions about the formal specification:
- Open an issue on GitHub: [rzonedevops/analyticase](https://github.com/rzonedevops/analyticase)
- See main project [README.md](../../README.md)

---

**Last Updated**: 2025-10-22

**Specification Version**: 1.0
