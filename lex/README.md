# Legal Framework Directory Structure

This directory contains a comprehensive legal framework organized by legal branches and jurisdictions.

## Directory Structure

```
lex/
├── cri/                    # Criminal Law
│   └── za/                 # South African Criminal Law
│       └── south_african_criminal_law.scm
├── civ/                    # Civil Law
│   └── za/                 # South African Civil Law
│       └── south_african_civil_law.scm
├── con/                    # Constitutional Law
│   └── za/                 # South African Constitutional Law
│       └── south_african_constitutional_law.scm
├── const/                  # Construction Law
│   └── za/                 # South African Construction Law
│       └── south_african_construction_law.scm
├── admin/                  # Administrative Law
│   └── za/                 # South African Administrative Law
│       └── south_african_administrative_law.scm
├── lab/                    # Labour Law
│   └── za/                 # South African Labour Law
│       └── south_african_labour_law.scm
├── env/                    # Environmental Law
│   └── za/                 # South African Environmental Law
│       └── south_african_environmental_law.scm
└── intl/                   # International Law
    └── za/                 # South African International Law
        └── south_african_international_law.scm
```

## Legal Framework Coverage

This directory contains comprehensive Scheme-based implementations of South African law across 8 major legal branches:

### 1. Civil Law (`civ/za/`)
- Legal personhood and capacity
- Contract Law - Offer, acceptance, consideration, capacity
- Delict Law (Tort Law) - Wrongfulness, fault, causation, damages
- Property Law - Ownership, possession, real vs personal rights
- Family Law - Marriage, divorce, parental responsibilities
- Evidence Law - Admissibility, burden of proof
- Procedural Law - Jurisdiction, limitation periods
- Remedies - Damages, specific performance, injunctions

### 2. Criminal Law (`cri/za/`)
- Criminal liability elements (actus reus, mens rea)
- Specific crimes (murder, theft, fraud, etc.)
- Criminal defences (self-defence, necessity, insanity)
- Criminal procedure (arrest, search, trial rights)
- Sentencing and juvenile justice

### 3. Constitutional Law (`con/za/`)
- Founding principles and constitutional supremacy
- Bill of Rights (all fundamental rights)
- Limitation of rights (Section 36)
- Separation of powers
- Cooperative government

### 4. Construction Law (`const/za/`)
- Construction contracts (JBCC, FIDIC, NEC, GCC)
- Contractor and employer obligations
- Variations and claims
- Defects and warranties
- Health and safety compliance

### 5. Administrative Law (`admin/za/`)
- PAJA (Promotion of Administrative Justice Act)
- Procedural fairness
- Judicial review grounds
- Legitimate expectation
- Administrative remedies

### 6. Labour Law (`lab/za/`)
- Employment relationships
- Labour Relations Act (LRA)
- Unfair dismissal
- Basic Conditions of Employment Act (BCEA)
- Employment Equity Act (EEA)

### 7. Environmental Law (`env/za/`)
- NEMA principles
- Environmental Impact Assessment (EIA)
- Pollution and waste management
- Biodiversity and conservation
- Climate change response

### 8. International Law (`intl/za/`)
- Treaties and conventions
- Customary international law
- Diplomatic and consular law
- International humanitarian law
- International criminal law (ICC)

## Implementation Features

All frameworks include:
- Rule-based legal reasoning structures
- Precedent system support
- Statutory interpretation rules
- Comprehensive placeholder functions for future implementation
- Extensible architecture for additional legal rules
- Integration with HypergraphQL engine

## Statistics

- **Total Legal Principles**: 823 (across all 8 frameworks)
- **Total Functions**: 800+ placeholder functions ready for implementation
- **Jurisdictions**: South Africa (za) with extensibility for other jurisdictions

## Integration with HypergraphQL

The legal frameworks automatically load into the HypergraphQL engine (see `models/ggmlex/hypergraphql/`), enabling:
- Graph traversal and querying of legal concepts
- Pattern matching over legal structures
- Path finding between legal principles
- Content-based search across all frameworks

## Testing

Run the legal framework integration tests:
```bash
python models/ggmlex/test_legal_frameworks.py
```

## Future Extensions

The framework includes placeholder functions that can be implemented with:
- Specific legal rules and algorithms
- Machine learning models
- Integration with legal databases and APIs
- Natural language processing for legal text
- Case law citation networks
- Statutory interpretation engines

## Usage

This framework provides the foundational structure for implementing:
- Legal reasoning systems
- Expert systems for legal analysis
- Automated legal document analysis
- Case prediction systems
- Compliance checking tools
- Legal education platforms