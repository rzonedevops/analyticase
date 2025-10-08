# AnalytiCase: ZA Judiciary Integration

## Overview

This repository contains the integration between HyperGNN Analysis Framework and South African judiciary systems (Court Online and CaseLines). The integration provides a comprehensive data mapping architecture that enables seamless communication between analytical capabilities and official court systems.

## Repository Structure

```
za_judiciary_integration/
├── api/                    # API implementation files
│   ├── main_za_enhanced.py # Enhanced main API with ZA judiciary integration
│   └── za_judiciary_api.py # ZA judiciary specific API endpoints
├── docs/                   # Documentation
│   ├── DATA_MAPPING_ZA_JUDICIARY.md  # Comprehensive data mapping documentation
│   ├── FIELD_MAPPING_EXAMPLES.md     # Field-by-field mapping examples with sample data
│   ├── ZA_JUDICIARY_INTEGRATION.md   # Integration overview and features
│   └── images/             # Documentation images
│       └── data_mapping_diagram.png  # Visual data mapping diagram
├── presentation/           # Presentation files for ZA judiciary integration
│   ├── title_slide.html    # Title slide
│   ├── integration_overview.html
│   ├── core_entity_mappings.html
│   └── ...                 # Additional presentation slides
└── schema/                 # Database schema files
    └── za_judiciary_schema.sql  # ZA judiciary database schema
```

## Key Features

### Court Online Integration

- Electronic Filing (E-Filing) capabilities
- Digital Case Management
- Automatic Document Routing
- Real-time Notifications
- Electronic Service

### CaseLines Integration

- Digital Bundle Creation
- Document Management
- Redaction Tools
- Electronic Presentation
- Multi-media Evidence Support
- Collaboration Tools

### Database Schema Alignment

- ZA-specific tables for court registry, case types, and evidence bundles
- Case number format compliance
- Full audit trail and legal compliance features

### API Endpoints

- ZA judiciary specific endpoints
- Enhanced core endpoints with ZA integration
- Compliance reporting

## Implementation Status

- ✅ Database schema design and deployment
- ✅ Core API endpoints implementation
- ✅ Court Online case format validation
- ✅ CaseLines bundle structure alignment
- ✅ Basic compliance framework
- ✅ ZA court registry population
- 🔄 Full Court Online API integration
- 🔄 CaseLines document upload integration
- 🔄 Advanced compliance reporting
- 🔄 Electronic signature validation

## Getting Started

1. Clone this repository
2. Set up the database using the schema files in `schema/`
3. Implement the API endpoints from `api/`
4. Configure environment variables for Court Online and CaseLines access

## Documentation

For detailed documentation on the integration architecture, refer to the files in the `docs/` directory:

- [ZA Judiciary Integration Overview](za_judiciary_integration/docs/ZA_JUDICIARY_INTEGRATION.md)
- [Data Mapping Documentation](za_judiciary_integration/docs/DATA_MAPPING_ZA_JUDICIARY.md)
- [Field Mapping Examples](za_judiciary_integration/docs/FIELD_MAPPING_EXAMPLES.md)

## Presentation

The `presentation/` directory contains HTML slides that provide a visual overview of the integration architecture. These slides can be viewed in any modern web browser.

## Contact

For questions or support regarding this integration, please contact the development team.
