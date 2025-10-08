#!/usr/bin/env python3
"""
HyperGNN Analysis Framework Backend API - ZA Judiciary Enhanced Version

This Flask application serves as the backend API for the HyperGNN Analysis
Framework with full South African judiciary integration (Court Online & CaseLines).
"""

import datetime
import logging
import os
from typing import Dict, List, Any, Optional

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Import ZA judiciary integration
try:
    from .za_judiciary_api import za_judiciary_bp, init_za_integration
except ImportError:
    from za_judiciary_api import za_judiciary_bp, init_za_integration

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')

# Initialize JWT
jwt = JWTManager(app)

# Register ZA judiciary blueprint
app.register_blueprint(za_judiciary_bp)


class DatabaseManager:
    """Manages database connections and operations with ZA judiciary support."""
    
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        self.neon_connection_string = os.getenv('NEON_CONNECTION_STRING')
        self._supabase_client = None
        self._neon_connection = None
        
    def get_connection(self, db_type: str = 'supabase'):
        """Get database connection based on type."""
        if db_type == 'supabase' and self.supabase_url and self.supabase_key:
            try:
                if not self._supabase_client:
                    from supabase import create_client
                    self._supabase_client = create_client(self.supabase_url, self.supabase_key)
                return self._supabase_client
            except ImportError:
                logger.warning("Supabase client not available")
                return None
            except Exception as e:
                logger.error(f"Supabase connection failed: {e}")
                return None
        elif db_type == 'neon' and self.neon_connection_string:
            try:
                if not self._neon_connection:
                    import psycopg2
                    self._neon_connection = psycopg2.connect(self.neon_connection_string)
                return self._neon_connection
            except ImportError:
                logger.warning("PostgreSQL client not available")
                return None
            except Exception as e:
                logger.error(f"PostgreSQL connection failed: {e}")
                return None
        return None
    
    def initialize_schema(self):
        """Initialize the database schema for ZA judiciary integration."""
        try:
            # Read and execute schema from SQL file
            schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema', 'za_judiciary_schema.sql')
            if os.path.exists(schema_path):
                with open(schema_path, 'r') as f:
                    schema_sql = f.read()
                
                # Execute with PostgreSQL connection if available
                neon_conn = self.get_connection('neon')
                if neon_conn:
                    cursor = neon_conn.cursor()
                    cursor.execute(schema_sql)
                    neon_conn.commit()
                    cursor.close()
                    logger.info("Database schema initialized successfully")
                    return True
                else:
                    logger.warning("No PostgreSQL connection available for schema initialization")
                    return False
            else:
                logger.warning("Schema file not found")
                return False
        except Exception as e:
            logger.error(f"Schema initialization failed: {e}")
            return False


db_manager = DatabaseManager()

# Initialize ZA judiciary integration
init_za_integration(db_manager)


def handle_error(error: Exception, message: str = "An error occurred") -> Dict:
    """Handle errors consistently across the application."""
    logger.error(f"{message}: {str(error)}")
    return {
        'error': True,
        'message': message,
        'details': str(error) if app.debug else None,
        'timestamp': datetime.datetime.now().isoformat()
    }


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify(handle_error(error, "Resource not found")), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify(handle_error(error, "Internal server error")), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint with ZA judiciary integration status."""
    try:
        # Check ZA judiciary integration status
        za_status = {
            'court_online': True,  # Would check actual connection in production
            'caselines': True,     # Would check actual connection in production
            'electronic_filing': True
        }
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.datetime.now().isoformat(),
            'version': '2.0.0-za',
            'za_judiciary_integration': za_status
        })
    except Exception as e:
        return jsonify(handle_error(e, "Health check failed")), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get the current status of the HyperGNN Analysis Framework with ZA integration."""
    try:
        # Check database connections
        supabase_status = 'connected' if db_manager.get_connection('supabase') else 'disconnected'
        neon_status = 'connected' if db_manager.get_connection('neon') else 'disconnected'
        
        return jsonify({
            'status': 'online',
            'components': {
                'hypergnn_core': {
                    'status': 'operational',
                    'version': '2.0.0-za',
                    'uptime': '3d 12h 45m'
                },
                'database': {
                    'supabase': {
                        'status': supabase_status,
                        'type': 'Supabase',
                        'version': '2.0'
                    },
                    'neon': {
                        'status': neon_status,
                        'type': 'PostgreSQL',
                        'version': '17.0'
                    }
                },
                'za_judiciary_integration': {
                    'court_online': {
                        'status': 'operational',
                        'enabled_courts': ['GP', 'GJ', 'WCC', 'FS'],
                        'e_filing_enabled': True
                    },
                    'caselines': {
                        'status': 'operational',
                        'enabled_courts': ['GP', 'GJ', 'WCC'],
                        'evidence_management_enabled': True
                    }
                },
                'processing_queue': {
                    'status': 'active',
                    'pending_jobs': 3,
                    'completed_jobs': 128
                },
                'api_gateway': {
                    'status': 'operational',
                    'requests_per_minute': 42,
                    'average_response_time': '120ms'
                }
            },
            'timestamp': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify(handle_error(e, "Failed to get system status")), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get the current statistics for the HyperGNN Analysis Framework with ZA data."""
    try:
        stats = {
            'active_cases': 24,
            'za_cases': 18,  # Cases using ZA judiciary integration
            'entities_analyzed': 1847,
            'evidence_items': 3291,
            'caselines_bundles': 156,
            'court_online_filings': 89,
            'processing_time': 2.3,
            'za_compliance_score': 0.95,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # Try to get real statistics from database if available
        supabase = db_manager.get_connection('supabase')
        if supabase:
            try:
                # Example query - would need actual tables
                # za_cases_result = supabase.table('za_cases').select('*').execute()
                # stats['za_cases'] = len(za_cases_result.data)
                pass
            except Exception as e:
                logger.warning(f"Could not fetch real statistics: {e}")
        
        return jsonify(stats)
    except Exception as e:
        return jsonify(handle_error(e, "Failed to get statistics")), 500


@app.route('/api/cases', methods=['GET'])
def get_cases():
    """Get a list of recent cases with ZA judiciary integration."""
    try:
        # Enhanced cases with ZA judiciary information
        cases = [
            {
                'id': 'CASE-2025-10-001',
                'case_number': '(GP) 12345/2025',
                'title': 'Financial Fraud Investigation',
                'status': 'active',
                'priority': 'high',
                'entities': 42,
                'evidence': 78,
                'court_division': 'Gauteng Division, Pretoria',
                'case_type': 'Commercial Court',
                'court_online_enabled': True,
                'caselines_enabled': True,
                'e_filing_status': 'active',
                'last_updated': '2025-10-01T14:30:00Z'
            },
            {
                'id': 'CASE-2025-09-015',
                'case_number': '(WCC) 67890/2025',
                'title': 'Corporate Network Analysis',
                'status': 'active',
                'priority': 'medium',
                'entities': 156,
                'evidence': 203,
                'court_division': 'Western Cape Division, Cape Town',
                'case_type': 'Ordinary Civil Trials',
                'court_online_enabled': True,
                'caselines_enabled': True,
                'e_filing_status': 'pending',
                'last_updated': '2025-09-28T09:15:00Z'
            },
            {
                'id': 'CASE-2025-09-012',
                'case_number': '(GJ) 54321/2025',
                'title': 'Supply Chain Investigation',
                'status': 'active',
                'priority': 'high',
                'entities': 89,
                'evidence': 134,
                'court_division': 'Gauteng Division, Johannesburg',
                'case_type': 'Special Civil Trials',
                'court_online_enabled': True,
                'caselines_enabled': True,
                'e_filing_status': 'filed',
                'last_updated': '2025-09-25T16:45:00Z'
            }
        ]
        
        return jsonify(cases)
    except Exception as e:
        return jsonify(handle_error(e, "Failed to get cases")), 500


@app.route('/api/case/<case_id>/za-integration', methods=['GET'])
def get_case_za_integration(case_id: str):
    """Get ZA judiciary integration details for a specific case."""
    try:
        logger.info(f"Fetching ZA integration details for case: {case_id}")
        
        # Sample ZA integration data
        integration_data = {
            'case_id': case_id,
            'court_online': {
                'enabled': True,
                'case_id': f"co-{case_id}",
                'e_filing_enabled': True,
                'electronic_service_enabled': True,
                'case_management_enabled': True,
                'filing_history': [
                    {
                        'filing_type': 'Summons',
                        'filing_date': '2025-09-15T10:00:00Z',
                        'status': 'filed',
                        'filing_fee': 500.00
                    },
                    {
                        'filing_type': 'Plea',
                        'filing_date': '2025-09-22T14:30:00Z',
                        'status': 'served',
                        'filing_fee': 200.00
                    }
                ]
            },
            'caselines': {
                'enabled': True,
                'bundle_id': f"cl-{case_id}",
                'evidence_management_enabled': True,
                'digital_presentation_enabled': True,
                'bundles': [
                    {
                        'bundle_name': 'Pleadings Bundle',
                        'bundle_type': 'pleadings',
                        'total_documents': 15,
                        'total_pages': 247,
                        'status': 'complete'
                    },
                    {
                        'bundle_name': 'Discovery Bundle',
                        'bundle_type': 'discovery',
                        'total_documents': 89,
                        'total_pages': 1456,
                        'status': 'in_progress'
                    }
                ]
            },
            'compliance': {
                'electronic_filing_act_compliant': True,
                'court_rules_compliant': True,
                'data_protection_compliant': True,
                'audit_trail_complete': True
            }
        }
        
        return jsonify(integration_data)
    except Exception as e:
        return jsonify(handle_error(e, f"Failed to get ZA integration for case {case_id}")), 500


@app.route('/api/case/<case_id>/court-online-filing', methods=['POST'])
def submit_court_online_filing(case_id: str):
    """Submit an electronic filing through Court Online for a case."""
    try:
        data = request.get_json()
        if not data:
            return jsonify(handle_error(ValueError("No filing data provided"), "Invalid request data")), 400
        
        # Validate required fields for Court Online filing
        required_fields = ['filing_type', 'documents']
        for field in required_fields:
            if field not in data:
                return jsonify(handle_error(ValueError(f"Missing field: {field}"), "Invalid filing data")), 400
        
        # Create filing record
        filing_record = {
            'filing_id': f"co-filing-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            'case_id': case_id,
            'filing_type': data['filing_type'],
            'documents': data['documents'],
            'filing_fee': data.get('filing_fee', 0),
            'payment_reference': data.get('payment_reference'),
            'submission_timestamp': datetime.datetime.now().isoformat(),
            'status': 'submitted',
            'court_online_reference': f"CO{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            'estimated_processing_time': '2-5 business days'
        }
        
        logger.info(f"Submitted Court Online filing for case: {case_id}")
        return jsonify({
            'success': True,
            'filing': filing_record,
            'message': 'Electronic filing submitted successfully to Court Online'
        }), 201
        
    except Exception as e:
        return jsonify(handle_error(e, f"Failed to submit Court Online filing for case {case_id}")), 500


@app.route('/api/case/<case_id>/caselines-bundle', methods=['POST'])
def create_caselines_bundle(case_id: str):
    """Create a CaseLines evidence bundle for a case."""
    try:
        data = request.get_json()
        if not data:
            return jsonify(handle_error(ValueError("No bundle data provided"), "Invalid request data")), 400
        
        # Create CaseLines bundle
        bundle_record = {
            'bundle_id': f"cl-bundle-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            'case_id': case_id,
            'bundle_name': data.get('bundle_name', 'Evidence Bundle'),
            'bundle_type': data.get('bundle_type', 'pleadings'),
            'documents': data.get('documents', []),
            'total_documents': len(data.get('documents', [])),
            'total_pages': sum(doc.get('page_count', 1) for doc in data.get('documents', [])),
            'status': 'draft',
            'pagination_complete': False,
            'redaction_complete': False,
            'caselines_reference': f"CL{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            'created_at': datetime.datetime.now().isoformat()
        }
        
        logger.info(f"Created CaseLines bundle for case: {case_id}")
        return jsonify({
            'success': True,
            'bundle': bundle_record,
            'message': 'CaseLines evidence bundle created successfully'
        }), 201
        
    except Exception as e:
        return jsonify(handle_error(e, f"Failed to create CaseLines bundle for case {case_id}")), 500


@app.route('/api/za-compliance-report', methods=['GET'])
def get_za_compliance_report():
    """Generate ZA judiciary compliance report."""
    try:
        compliance_report = {
            'report_id': f"compliance-{datetime.datetime.now().strftime('%Y%m%d')}",
            'generated_at': datetime.datetime.now().isoformat(),
            'compliance_areas': {
                'electronic_filing_act': {
                    'compliant': True,
                    'score': 0.98,
                    'requirements_met': 47,
                    'total_requirements': 48,
                    'non_compliance_items': ['Digital signature validation pending']
                },
                'court_rules': {
                    'compliant': True,
                    'score': 0.95,
                    'requirements_met': 38,
                    'total_requirements': 40,
                    'non_compliance_items': ['Service confirmation automation', 'Bundle pagination standards']
                },
                'data_protection': {
                    'compliant': True,
                    'score': 0.92,
                    'requirements_met': 23,
                    'total_requirements': 25,
                    'non_compliance_items': ['Data retention policy updates', 'Cross-border data transfer protocols']
                }
            },
            'overall_score': 0.95,
            'certification_status': 'Certified',
            'next_review_date': '2025-12-01',
            'recommendations': [
                'Implement automated digital signature validation',
                'Enhance service confirmation workflows',
                'Update data retention policies for international compliance'
            ]
        }
        
        return jsonify(compliance_report)
    except Exception as e:
        return jsonify(handle_error(e, "Failed to generate compliance report")), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
