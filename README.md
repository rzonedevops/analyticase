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
- ✅ Full Court Online API integration
- ✅ CaseLines document upload integration
- ✅ Advanced compliance reporting
- ✅ Electronic signature validation
- ✅ Comprehensive test suite
- ✅ Production deployment configuration
- ✅ API documentation and examples

## Getting Started

### Prerequisites
- Python 3.11 or higher
- PostgreSQL database (or Supabase account)
- Court Online API credentials (when available)
- CaseLines API credentials (when available)

### Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/rzonedevops/analyticase.git
   cd analyticase
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database and API credentials
   ```

4. **Initialize the database**
   ```bash
   python za_judiciary_integration/scripts/init_database.py
   ```

5. **Run the API server**
   ```bash
   cd za_judiciary_integration/api
   python main_za_enhanced.py
   ```

6. **Test the installation**
   ```bash
   python test_api.py
   ```

### Docker Deployment

For production deployment:

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t za-judiciary-api .
docker run -p 5000:5000 --env-file .env za-judiciary-api
```

## Documentation

For detailed documentation on the integration architecture, refer to the files in the `docs/` directory:

- [ZA Judiciary Integration Overview](za_judiciary_integration/docs/ZA_JUDICIARY_INTEGRATION.md)
- [Data Mapping Documentation](za_judiciary_integration/docs/DATA_MAPPING_ZA_JUDICIARY.md)
- [Field Mapping Examples](za_judiciary_integration/docs/FIELD_MAPPING_EXAMPLES.md)

## Presentation

The `presentation/` directory contains HTML slides that provide a visual overview of the integration architecture. These slides can be viewed in any modern web browser.

## Contact

For questions or support regarding this integration, please contact the development team.
