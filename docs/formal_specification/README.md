# AnalytiCase Z++ Formal Specification

## Overview

This directory contains the formal specification of the AnalytiCase system using Z++ (an object-oriented extension of the Z notation). The specification provides a rigorous mathematical foundation for the system's core components, operations, and invariants.

## What is Z++?

Z++ is an object-oriented extension of the Z formal specification language. It combines:
- The mathematical precision of Z notation
- Object-oriented concepts (classes, inheritance)
- Pre/post-conditions and invariants
- State-based modeling

Z++ is particularly well-suited for specifying complex systems with:
- Rich data structures
- State transitions
- Complex invariants
- Multi-component interactions

## Contents

### Main Specification Document

- **analyticase_zpp_spec.tex**: The complete Z++ specification in LaTeX format

### Specification Structure

The specification is organized into the following sections:

1. **Introduction**
   - Purpose and scope
   - System overview

2. **Basic Types**
   - Given sets (CASEID, NODEID, EDGEID, etc.)
   - Free types (NODETYPE, CASESTATUS, etc.)

3. **Core Data Structures**
   - Node class (entities in hypergraph)
   - Hyperedge class (relationships)
   - Hypergraph class (complete graph structure)

4. **Legal Case Management**
   - Party class (plaintiff, defendant)
   - LegalCase class (complete case structure)
   - Case operations (create, update, add documents)

5. **ZA Judiciary Integration**
   - CourtOnlineCase class (e-filing system)
   - Document class (case documents)
   - CaseLinesBundle class (evidence bundles)

6. **Simulation Models**
   - Agent class (investigators, attorneys, judges)
   - SimulationEvent class (discrete events)
   - SimulationRun class (complete simulation)

7. **Analysis Operations**
   - Community detection
   - Centrality analysis
   - Temporal pattern detection
   - Link prediction

8. **System Invariants**
   - Hypergraph consistency
   - Case status transitions
   - Bundle submission rules
   - Event temporal ordering

9. **Example Specifications**
   - Trust fraud case example
   - Hypergraph construction example

## Compiling the Specification

To compile the LaTeX document to PDF:

```bash
# Install required LaTeX packages
sudo apt-get install texlive texlive-latex-extra texlive-science

# Compile the specification
cd docs/formal_specification
pdflatex analyticase_zpp_spec.tex
pdflatex analyticase_zpp_spec.tex  # Run twice for references
```

Or use an online LaTeX editor like [Overleaf](https://www.overleaf.com/).

## Key Components Specified

### Hypergraph Model

The specification formally defines the hypergraph data structure used for legal case analysis:

- **Nodes**: Entities (people, organizations, events, documents)
- **Hyperedges**: Multi-way relationships between nodes
- **Invariants**: Consistency rules ensuring graph integrity

Example operations:
- `AddNode`: Add a node with validation
- `AddHyperedge`: Add a hyperedge connecting multiple nodes
- `GetNodeNeighbors`: Find all connected nodes
- `HypergraphStatistics`: Compute graph metrics

### Legal Case Management

Formal specification of case creation and management:

- **CreateCase**: Initialize a new legal case with parties
- **UpdateCaseStatus**: Transition case through valid states
- **AddDocument**: Attach documents to a case
- **ValidateCaseNumber**: Ensure ZA case number format

Status transitions are formally specified to prevent invalid state changes.

### ZA Judiciary Integration

Precise specification of Court Online and CaseLines integration:

- **CourtOnlineCase**: E-filing and digital signature management
- **CaseLinesBundle**: Evidence bundle preparation and submission
- **Document**: File management with pagination and redaction

Invariants ensure bundles meet submission requirements before acceptance.

### Simulation Framework

Formal model of the simulation engine:

- **Agent**: Case participants with workload and efficiency
- **SimulationEvent**: Temporal events with ordering constraints
- **SimulationRun**: Complete simulation lifecycle

Events are guaranteed to be temporally ordered through formal invariants.

## Using the Specification

### For Developers

The specification can be used to:

1. **Verify Implementation**: Check that code matches the formal specification
2. **Generate Tests**: Derive test cases from pre/post-conditions
3. **Understand Requirements**: Precise definition of system behavior
4. **Identify Edge Cases**: Formal invariants reveal boundary conditions

### For Verification

The specification supports:

1. **Formal Proof**: Prove properties using Z theorem provers
2. **Model Checking**: Verify finite-state properties
3. **Refinement Checking**: Verify implementation refines specification
4. **Consistency Checking**: Ensure specifications are self-consistent

### For Documentation

The specification provides:

1. **Precise Definitions**: Unambiguous component descriptions
2. **Mathematical Rigor**: Formal foundation for discussions
3. **Complete Coverage**: All major components specified
4. **Traceability**: Clear mapping to implementation

## Tools and Resources

### Z++ Tools

- **Z/EVES**: Interactive Z theorem prover
- **Fuzz**: Z type checker
- **ProofPower**: Proof assistant for Z specifications
- **CZT (Community Z Tools)**: Eclipse-based Z toolkit

### Learning Resources

- *The Z Notation: A Reference Manual* by Spivey
- *Object-Z/Z++ Specification of an Object-Oriented System* by Duke et al.
- *Z++ Documentation* from University of Queensland
- *Formal Specification Using Z* by Ben Potter et al.

### Online Resources

- [Z Notation Wiki](http://wiki.c2.com/?ZedNotation)
- [Formal Methods Resources](https://formalmethods.wikia.org/)
- [CZT Community](http://czt.sourceforge.net/)

## Mapping to Implementation

### Python Implementation Correspondence

The Z++ classes map to Python implementations:

| Z++ Class | Python Implementation |
|-----------|----------------------|
| Node | `models/hyper_gnn/hypergnn_model.py::Node` |
| Hyperedge | `models/hyper_gnn/hypergnn_model.py::Hyperedge` |
| Hypergraph | `models/hyper_gnn/hypergnn_model.py::Hypergraph` |
| CourtOnlineCase | `za_judiciary_integration/api/za_judiciary_api.py::CourtOnlineCase` |
| CaseLinesBundle | `za_judiciary_integration/api/za_judiciary_api.py::CaseLinesBundle` |
| Agent | `models/agent_based/*.py` |
| SimulationRun | `simulations/*.py` |

### Database Schema Correspondence

Z++ schemas map to database tables:

| Z++ Schema | SQL Table |
|-----------|-----------|
| LegalCase | `cases` (inferred) |
| SimulationRun | `simulation_runs` |
| Agent | `agent_simulation_results` |
| SimulationEvent | `discrete_event_results` |

## Verification Strategy

### Invariant Checking

Key invariants to verify in implementation:

1. **Hypergraph Consistency**
   - All edge nodes exist in node set
   - Node-to-edge mapping is consistent
   - No orphaned edges or nodes

2. **Case Status Transitions**
   - Only valid state transitions occur
   - Terminal states are enforced
   - Status history is maintained

3. **Bundle Submission**
   - Pagination complete before submission
   - Redaction complete before submission
   - Non-empty document list

4. **Event Ordering**
   - Temporal sequence preserved
   - Timestamps monotonically increasing
   - No future-dated events

### Testing Approach

1. **Property-Based Testing**: Generate tests from Z++ pre/post-conditions
2. **Invariant Monitoring**: Add runtime checks for Z++ invariants
3. **State Machine Testing**: Verify valid state transitions
4. **Boundary Testing**: Test edge cases from formal constraints

## Extending the Specification

To add new components:

1. Define new basic types or classes
2. Specify operations with pre/post-conditions
3. Add invariants to ensure consistency
4. Provide examples demonstrating usage
5. Update this README with mappings

## Contributing

When adding to the specification:

1. Follow Z++ notation conventions
2. Maintain mathematical rigor
3. Include pre/post-conditions for all operations
4. Document invariants clearly
5. Provide examples for complex schemas

## License

This formal specification is part of the AnalytiCase project and follows the same license as the main repository.

## Contact

For questions about the formal specification:
- Open an issue on GitHub
- Contact the AnalytiCase development team
- Refer to the main project documentation

## References

1. Spivey, J. M. (1992). *The Z Notation: A Reference Manual*. Prentice Hall.
2. Duke, R., Rose, G., & Smith, G. (1995). *Object-Z: A Specification Language Advocated for the Description of Standards*. Computer Standards & Interfaces.
3. Potter, B., Sinclair, J., & Till, D. (1996). *An Introduction to Formal Specification and Z*. Prentice Hall.
4. Woodcock, J., & Davies, J. (1996). *Using Z: Specification, Refinement, and Proof*. Prentice Hall.
