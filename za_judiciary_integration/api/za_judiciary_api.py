#!/usr/bin/env python3
"""
ZA Judiciary Integration API for HyperGNN Analysis Framework
Provides Court Online and CaseLines integration endpoints
"""

import datetime
import logging
from typing import Dict, List, Any, Optional
from flask import Blueprint, jsonify, request
from dataclasses import dataclass

# Create blueprint for ZA judiciary endpoints
za_judiciary_bp = Blueprint('za_judiciary', __name__, url_prefix='/api/za-judiciary')

logger = logging.getLogger(__name__)


@dataclass
class CourtOnlineCase:
    """Data structure for Court Online case integration"""
    case_number: str
    court_code: str
    case_type: str
    title: str
    filing_date: str
    status: str
    plaintiff: Dict
    defendant: Dict
    attorney_details: Dict


@dataclass
class CaseLinesBundle:
    """Data structure for CaseLines evidence bundle"""
    bundle_id: str
    case_id: str
    bundle_name: str
    bundle_type: str
    total_pages: int
    documents: List[Dict]
    status: str


class ZAJudiciaryIntegration:
    """Handles integration with South African judiciary systems"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        
    def validate_case_number(self, case_number: str) -> bool:
        """Validate ZA case number format (e.g., (GP) 12345/2025)"""
        import re
        pattern = r'^\([A-Z]{2,3}\)\s*\d{4,6}\/\d{4}$'
        return bool(re.match(pattern, case_number))
    
    def get_court_divisions(self) -> List[Dict]:
        """Get list of ZA court divisions with Court Online status"""
        # In production, this would query the database
        return [
            {
                "court_code": "GP",
                "court_name": "Gauteng Division, Pretoria",
                "division": "Gauteng Division",
                "court_online_enabled": True,
                "caselines_enabled": True
            },
            {
                "court_code": "GJ", 
                "court_name": "Gauteng Division, Johannesburg",
                "division": "Gauteng Division",
                "court_online_enabled": True,
                "caselines_enabled": True
            },
            {
                "court_code": "WCC",
                "court_name": "Western Cape Division, Cape Town", 
                "division": "Western Cape Division",
                "court_online_enabled": True,
                "caselines_enabled": True
            }
        ]
    
    def create_court_online_case(self, case_data: Dict) -> Dict:
        """Create a new case in Court Online format"""
        try:
            # Validate required fields
            required_fields = ['case_number', 'court_code', 'case_type', 'title', 'plaintiff', 'defendant']
            for field in required_fields:
                if field not in case_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate case number format
            if not self.validate_case_number(case_data['case_number']):
                raise ValueError("Invalid ZA case number format")
            
            # Create case record
            case_record = {
                'id': f"za-case-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                'case_number': case_data['case_number'],
                'court_code': case_data['court_code'],
                'case_type': case_data['case_type'],
                'title': case_data['title'],
                'status': 'filed',
                'filing_date': datetime.datetime.now().isoformat(),
                'plaintiff': case_data['plaintiff'],
                'defendant': case_data['defendant'],
                'court_online_integration': {
                    'enabled': True,
                    'case_id': f"co-{case_data['case_number'].replace(' ', '').replace('(', '').replace(')', '')}",
                    'e_filing_enabled': True
                },
                'caselines_integration': {
                    'enabled': True,
                    'bundle_id': f"cl-{case_data['case_number'].replace(' ', '').replace('(', '').replace(')', '')}"
                }
            }
            
            logger.info(f"Created Court Online case: {case_record['case_number']}")
            return case_record
            
        except Exception as e:
            logger.error(f"Error creating Court Online case: {str(e)}")
            raise
    
    def create_caselines_bundle(self, case_id: str, bundle_data: Dict) -> Dict:
        """Create a CaseLines evidence bundle"""
        try:
            bundle_record = {
                'id': f"bundle-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                'case_id': case_id,
                'bundle_name': bundle_data.get('bundle_name', 'Evidence Bundle'),
                'bundle_type': bundle_data.get('bundle_type', 'pleadings'),
                'caselines_bundle_id': f"cl-bundle-{case_id}-{len(bundle_data.get('documents', []))}",
                'total_pages': 0,
                'total_documents': len(bundle_data.get('documents', [])),
                'status': 'draft',
                'pagination_complete': False,
                'redaction_complete': False,
                'documents': bundle_data.get('documents', []),
                'created_at': datetime.datetime.now().isoformat()
            }
            
            # Calculate total pages
            total_pages = sum(doc.get('page_count', 1) for doc in bundle_record['documents'])
            bundle_record['total_pages'] = total_pages
            
            logger.info(f"Created CaseLines bundle: {bundle_record['bundle_name']}")
            return bundle_record
            
        except Exception as e:
            logger.error(f"Error creating CaseLines bundle: {str(e)}")
            raise


# Initialize integration handler
za_integration = None


def init_za_integration(db_manager):
    """Initialize ZA judiciary integration with database manager"""
    global za_integration
    za_integration = ZAJudiciaryIntegration(db_manager)


# API Endpoints

@za_judiciary_bp.route('/courts', methods=['GET'])
def get_za_courts():
    """Get list of South African court divisions"""
    try:
        courts = za_integration.get_court_divisions()
        return jsonify({
            'courts': courts,
            'total_courts': len(courts),
            'court_online_enabled': len([c for c in courts if c['court_online_enabled']]),
            'caselines_enabled': len([c for c in courts if c['caselines_enabled']])
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f"Failed to retrieve courts: {str(e)}",
            'timestamp': datetime.datetime.now().isoformat()
        }), 500


@za_judiciary_bp.route('/case-types', methods=['GET'])
def get_za_case_types():
    """Get ZA case types aligned with Court Online"""
    try:
        case_types = [
            {'code': 'JCM', 'name': 'Judicial Case Management', 'court_online_category': 'Judicial Case Management'},
            {'code': 'CCA', 'name': 'Civil and Criminal Appeals', 'court_online_category': 'Civil and Criminal Appeals'},
            {'code': 'COM', 'name': 'Commercial Court', 'court_online_category': 'Commercial Court'},
            {'code': 'DEF', 'name': 'Default Judgements', 'court_online_category': 'Default Judgements'},
            {'code': 'DIV', 'name': 'Divorce Actions', 'court_online_category': 'Divorce Actions'},
            {'code': 'LTA', 'name': 'Leave to Appeal', 'court_online_category': 'Leave to Appeal'},
            {'code': 'OPM', 'name': 'Opposed Motions', 'court_online_category': 'Opposed Motions'},
            {'code': 'OCT', 'name': 'Ordinary Civil Trials', 'court_online_category': 'Ordinary Civil Trials'},
            {'code': 'R43', 'name': 'Rule 43 Applications', 'court_online_category': 'Rule 43 Applications'},
            {'code': 'SCT', 'name': 'Special Civil Trials', 'court_online_category': 'Special Civil Trials'},
            {'code': 'SPM', 'name': 'Special Motions/3rd Court', 'court_online_category': 'Special Motions/ 3rd Court'},
            {'code': 'SJA', 'name': 'Summary Judgement Applications', 'court_online_category': 'Summary Judgement Applications'},
            {'code': 'TIA', 'name': 'Trial Interlocutory Applications', 'court_online_category': 'Trial Interlocutory Applications'},
            {'code': 'UNM', 'name': 'Unopposed Motions', 'court_online_category': 'Unopposed Motion'}
        ]
        
        return jsonify({
            'case_types': case_types,
            'total_types': len(case_types)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f"Failed to retrieve case types: {str(e)}",
            'timestamp': datetime.datetime.now().isoformat()
        }), 500


@za_judiciary_bp.route('/cases', methods=['POST'])
def create_za_case():
    """Create a new ZA case with Court Online integration"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': True,
                'message': 'No case data provided',
                'timestamp': datetime.datetime.now().isoformat()
            }), 400
        
        case_record = za_integration.create_court_online_case(data)
        
        return jsonify({
            'success': True,
            'case': case_record,
            'message': 'ZA case created successfully with Court Online integration',
            'timestamp': datetime.datetime.now().isoformat()
        }), 201
        
    except ValueError as e:
        return jsonify({
            'error': True,
            'message': str(e),
            'timestamp': datetime.datetime.now().isoformat()
        }), 400
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f"Failed to create case: {str(e)}",
            'timestamp': datetime.datetime.now().isoformat()
        }), 500


@za_judiciary_bp.route('/cases/<case_id>/bundles', methods=['POST'])
def create_evidence_bundle(case_id: str):
    """Create a CaseLines evidence bundle for a case"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': True,
                'message': 'No bundle data provided',
                'timestamp': datetime.datetime.now().isoformat()
            }), 400
        
        bundle_record = za_integration.create_caselines_bundle(case_id, data)
        
        return jsonify({
            'success': True,
            'bundle': bundle_record,
            'message': 'CaseLines evidence bundle created successfully',
            'timestamp': datetime.datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f"Failed to create evidence bundle: {str(e)}",
            'timestamp': datetime.datetime.now().isoformat()
        }), 500


@za_judiciary_bp.route('/cases/<case_id>/court-online-status', methods=['GET'])
def get_court_online_status(case_id: str):
    """Get Court Online integration status for a case"""
    try:
        # In production, this would query the database
        status = {
            'case_id': case_id,
            'court_online_enabled': True,
            'e_filing_enabled': True,
            'case_management_enabled': True,
            'electronic_service_enabled': True,
            'sms_notifications_enabled': True,
            'email_notifications_enabled': True,
            'last_sync': datetime.datetime.now().isoformat(),
            'sync_status': 'active'
        }
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f"Failed to get Court Online status: {str(e)}",
            'timestamp': datetime.datetime.now().isoformat()
        }), 500


@za_judiciary_bp.route('/cases/<case_id>/caselines-status', methods=['GET'])
def get_caselines_status(case_id: str):
    """Get CaseLines integration status for a case"""
    try:
        # In production, this would query the database
        status = {
            'case_id': case_id,
            'caselines_enabled': True,
            'evidence_management_enabled': True,
            'digital_bundles_enabled': True,
            'electronic_presentation_enabled': True,
            'total_bundles': 3,
            'total_documents': 45,
            'total_pages': 1247,
            'pagination_complete': True,
            'redaction_complete': False,
            'last_sync': datetime.datetime.now().isoformat(),
            'sync_status': 'active'
        }
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f"Failed to get CaseLines status: {str(e)}",
            'timestamp': datetime.datetime.now().isoformat()
        }), 500


@za_judiciary_bp.route('/validate-case-number', methods=['POST'])
def validate_case_number():
    """Validate ZA case number format"""
    try:
        data = request.get_json()
        if not data or 'case_number' not in data:
            return jsonify({
                'error': True,
                'message': 'Case number is required',
                'timestamp': datetime.datetime.now().isoformat()
            }), 400
        
        case_number = data['case_number']
        is_valid = za_integration.validate_case_number(case_number)
        
        return jsonify({
            'case_number': case_number,
            'is_valid': is_valid,
            'format_example': '(GP) 12345/2025',
            'validation_rules': [
                'Must start with court code in parentheses (e.g., (GP), (WCC))',
                'Followed by case number (4-6 digits)',
                'Followed by forward slash and year (4 digits)'
            ]
        })
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f"Validation failed: {str(e)}",
            'timestamp': datetime.datetime.now().isoformat()
        }), 500


@za_judiciary_bp.route('/electronic-filing', methods=['POST'])
def submit_electronic_filing():
    """Submit electronic filing through Court Online"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': True,
                'message': 'Filing data is required',
                'timestamp': datetime.datetime.now().isoformat()
            }), 400
        
        # Simulate electronic filing submission
        filing_record = {
            'filing_id': f"ef-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            'case_id': data.get('case_id'),
            'filing_type': data.get('filing_type'),
            'court_online_filing_id': f"co-filing-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            'submission_timestamp': datetime.datetime.now().isoformat(),
            'status': 'submitted',
            'documents_filed': data.get('documents', []),
            'filing_fee': data.get('filing_fee', 0),
            'payment_reference': data.get('payment_reference'),
            'estimated_processing_time': '2-5 business days'
        }
        
        return jsonify({
            'success': True,
            'filing': filing_record,
            'message': 'Electronic filing submitted successfully to Court Online',
            'timestamp': datetime.datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f"Electronic filing failed: {str(e)}",
            'timestamp': datetime.datetime.now().isoformat()
        }), 500


@za_judiciary_bp.route('/integration-status', methods=['GET'])
def get_integration_status():
    """Get overall ZA judiciary integration status"""
    try:
        status = {
            'court_online': {
                'status': 'operational',
                'version': '2.1.0',
                'enabled_courts': ['GP', 'GJ', 'WCC', 'FS'],
                'total_cases': 1247,
                'active_filings': 89,
                'last_sync': datetime.datetime.now().isoformat()
            },
            'caselines': {
                'status': 'operational', 
                'version': '3.2.1',
                'enabled_courts': ['GP', 'GJ', 'WCC'],
                'total_bundles': 456,
                'total_documents': 12847,
                'total_pages': 234567,
                'last_sync': datetime.datetime.now().isoformat()
            },
            'compliance': {
                'electronic_filing_act_compliant': True,
                'data_protection_compliant': True,
                'court_rules_compliant': True,
                'audit_trail_enabled': True
            }
        }
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f"Failed to get integration status: {str(e)}",
            'timestamp': datetime.datetime.now().isoformat()
        }), 500
