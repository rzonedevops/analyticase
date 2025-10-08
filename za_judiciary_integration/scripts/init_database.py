#!/usr/bin/env python3
"""
Database initialization script for ZA Judiciary Integration.
Creates tables and populates initial data.
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

def get_db_connection():
    """Get PostgreSQL database connection."""
    connection_string = os.getenv('NEON_CONNECTION_STRING')
    if not connection_string:
        print("❌ NEON_CONNECTION_STRING environment variable not set")
        return None
    
    try:
        conn = psycopg2.connect(connection_string)
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def execute_schema():
    """Execute the database schema."""
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema', 'za_judiciary_schema.sql')
    
    if not os.path.exists(schema_path):
        print(f"❌ Schema file not found: {schema_path}")
        return False
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        cursor = conn.cursor()
        cursor.execute(schema_sql)
        conn.commit()
        cursor.close()
        
        print("✅ Database schema created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Schema execution failed: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def populate_initial_data():
    """Populate initial data for ZA courts and case types."""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Insert ZA court registry data
        courts_data = [
            ('GP', 'Gauteng Division, Pretoria', 'Gauteng Division', 'Provincial', 'High Court', 
             '320 Thabo Sehume Street, Pretoria, 0002', 'Private Bag X807, Pretoria, 0001',
             '+27 12 492 5000', 'registrar.gp@judiciary.org.za', 'Ms. J. Smith', True, True),
            ('GJ', 'Gauteng Division, Johannesburg', 'Gauteng Division', 'Provincial', 'High Court',
             '1 Pritchard Street, Johannesburg, 2001', 'Private Bag X9, Johannesburg, 2000', 
             '+27 11 335 8000', 'registrar.gj@judiciary.org.za', 'Mr. P. Johnson', True, True),
            ('WCC', 'Western Cape Division, Cape Town', 'Western Cape Division', 'Provincial', 'High Court',
             '1 Queen Victoria Street, Cape Town, 8001', 'Private Bag X9027, Cape Town, 8000',
             '+27 21 469 5000', 'registrar.wcc@judiciary.org.za', 'Ms. A. Williams', True, True),
            ('FS', 'Free State Division, Bloemfontein', 'Free State Division', 'Provincial', 'High Court',
             'President Brand Street, Bloemfontein, 9301', 'Private Bag X20530, Bloemfontein, 9300',
             '+27 51 492 5000', 'registrar.fs@judiciary.org.za', 'Mr. D. Brown', True, False)
        ]
        
        insert_courts_sql = """
        INSERT INTO za_court_registry 
        (court_code, court_name, division, jurisdiction, court_type, physical_address, 
         postal_address, contact_number, email, registrar_name, is_court_online_enabled, is_caselines_enabled)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (court_code) DO NOTHING
        """
        
        cursor.executemany(insert_courts_sql, courts_data)
        
        # Insert case types
        case_types_data = [
            ('JCM', 'Judicial Case Management', 'Judicial Case Management', 'Case management proceedings', 500.00),
            ('CCA', 'Civil and Criminal Appeals', 'Civil and Criminal Appeals', 'Appeal proceedings', 1000.00),
            ('COM', 'Commercial Court', 'Commercial Court', 'Commercial disputes', 750.00),
            ('DEF', 'Default Judgements', 'Default Judgements', 'Unopposed judgement applications', 300.00),
            ('DIV', 'Divorce Actions', 'Divorce Actions', 'Divorce proceedings', 600.00),
            ('LTA', 'Leave to Appeal', 'Leave to Appeal', 'Applications for leave to appeal', 800.00),
            ('OPM', 'Opposed Motions', 'Opposed Motions', 'Contested motion proceedings', 650.00),
            ('OCT', 'Ordinary Civil Trials', 'Ordinary Civil Trials', 'Standard civil trial proceedings', 900.00),
            ('R43', 'Rule 43 Applications', 'Rule 43 Applications', 'Interim maintenance applications', 400.00),
            ('SCT', 'Special Civil Trials', 'Special Civil Trials', 'Specialized civil proceedings', 1200.00),
            ('SPM', 'Special Motions/3rd Court', 'Special Motions/ 3rd Court', 'Special motion proceedings', 700.00),
            ('SJA', 'Summary Judgement Applications', 'Summary Judgement Applications', 'Summary judgement proceedings', 550.00),
            ('TIA', 'Trial Interlocutory Applications', 'Trial Interlocutory Applications', 'Pre-trial applications', 450.00),
            ('UNM', 'Unopposed Motions', 'Unopposed Motion', 'Uncontested motion proceedings', 350.00)
        ]
        
        insert_case_types_sql = """
        INSERT INTO za_case_types 
        (case_type_code, case_type_name, court_online_category, description, standard_filing_fee)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (case_type_code) DO NOTHING
        """
        
        cursor.executemany(insert_case_types_sql, case_types_data)
        
        conn.commit()
        cursor.close()
        
        print("✅ Initial data populated successfully")
        return True
        
    except Exception as e:
        print(f"❌ Data population failed: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def verify_installation():
    """Verify the database installation."""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Count courts
        cursor.execute("SELECT COUNT(*) as count FROM za_court_registry")
        courts_count = cursor.fetchone()['count']
        
        # Count case types
        cursor.execute("SELECT COUNT(*) as count FROM za_case_types")
        case_types_count = cursor.fetchone()['count']
        
        cursor.close()
        
        print("✅ Database verification completed:")
        print(f"   📍 Courts registered: {courts_count}")
        print(f"   📋 Case types available: {case_types_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return False
    finally:
        conn.close()

def main():
    """Main initialization function."""
    print("🚀 Initializing ZA Judiciary Integration Database")
    print("=" * 60)
    
    # Check environment
    if not os.getenv('NEON_CONNECTION_STRING'):
        print("❌ Please set NEON_CONNECTION_STRING environment variable")
        print("   Example: postgresql://user:password@host:port/database")
        return False
    
    # Execute schema
    print("📋 Creating database schema...")
    if not execute_schema():
        return False
    
    # Populate initial data
    print("📊 Populating initial data...")
    if not populate_initial_data():
        return False
    
    # Verify installation
    print("✅ Verifying installation...")
    if not verify_installation():
        return False
    
    print("\n🎉 Database initialization completed successfully!")
    print("🔧 The ZA Judiciary Integration system is ready to use.")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)