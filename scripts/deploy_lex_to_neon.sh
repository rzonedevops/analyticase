#!/bin/bash
# Deploy Lex Scheme to Neon database

PROJECT_ID="sweet-sea-69912135"
DATABASE_NAME="neondb"
SCHEMA_FILE="schema/lex_scheme_enhanced.sql"

echo "Deploying Lex Scheme to Neon database..."
echo "Project: $PROJECT_ID"
echo "Database: $DATABASE_NAME"
echo ""

# Read the schema file and execute
if [ -f "$SCHEMA_FILE" ]; then
    echo "Schema file found: $SCHEMA_FILE"
    echo "Executing schema deployment via Neon MCP..."
    
    # Use the prepare_database_migration tool
    manus-mcp-cli tool call prepare_database_migration \
        --server neon \
        --input "{\"params\": {\"projectId\": \"$PROJECT_ID\", \"databaseName\": \"$DATABASE_NAME\", \"migrationSql\": \"$(cat $SCHEMA_FILE | tr '\n' ' ' | sed 's/"/\\"/g')\" }}"
else
    echo "Error: Schema file not found: $SCHEMA_FILE"
    exit 1
fi

echo ""
echo "Deployment initiated. Check the output above for results."
