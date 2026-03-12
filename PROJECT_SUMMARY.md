# Polarion MCP Server - Project Summary

Complete, production-ready MCP server for Polarion ALM integration.

## Project Location
`~/Documents/GitHub/polarion-mcp-server`

## Features Implemented

### Core Functionality
- Test case management (create, read, update, search)
- Test steps management (via discovered REST API endpoints)
- Test run creation and management
- Test result updates and tracking
- Connection testing and authentication

### Integrations
- JUnit XML import - Import test results from JUnit reports
- Spreadsheet export - Export test cases to Excel/CSV
- Spreadsheet import - Bulk import test cases from Excel/CSV
- Full MCP protocol support for Claude Desktop

### API Discovery
Successfully discovered and documented previously undocumented Polarion REST API endpoints:
- `POST /projects/{id}/workitems/{id}/teststeps` - Create test steps
- `GET /projects/{id}/workitems/{id}/teststeps/{index}` - Get test step
- `DELETE /projects/{id}/workitems/{id}/teststeps/{index}` - Delete test step

## Project Structure

```
polarion-mcp-server/
├── server.py                      # Main MCP server with all tools
├── polarion_client.py             # Core Polarion REST API client
├── test_runs.py                   # Test run management
├── integrations/
│   ├── __init__.py
│   ├── junit_import.py            # JUnit XML import
│   └── spreadsheet.py             # Excel/CSV integration
├── examples/
│   ├── create_test_case_example.py
│   ├── import_junit_example.py
│   └── spreadsheet_example.py
├── README.md                      # Complete documentation
├── API.md                         # Full API reference
├── CHANGELOG.md                   # Version history
├── requirements.txt               # Python dependencies
├── setup.sh                       # Quick setup script
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore rules
└── LICENSE                        # MIT License
```

## Available Tools (15 total)

### Test Case Management (6 tools)
1. `test_polarion_connection` - Test connection and auth
2. `create_polarion_test_case` - Create new test case
3. `add_test_steps_to_testcase` - Add/update test steps
4. `get_polarion_test_case` - Retrieve test case details
5. `update_polarion_test_case` - Update test case attributes
6. `search_polarion_test_cases` - Search with Polarion query

### Test Run Management (3 tools)
7. `create_test_run` - Create new test run
8. `update_test_run_result` - Update test result
9. `get_test_run_status` - Get run status and statistics

### Integration Tools (3 tools)
10. `import_junit_results` - Import JUnit XML results
11. `export_test_cases_to_spreadsheet` - Export to Excel/CSV
12. `import_test_cases_from_spreadsheet` - Import from Excel/CSV

## Installation

```bash
cd ~/Documents/GitHub/polarion-mcp-server
./setup.sh
```

Or manually:

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your POLARION_TOKEN
python3 server.py
```

## Configuration

### Environment Variables
```bash
export POLARION_URL="https://polarion.engineering.redhat.com"
export POLARION_TOKEN="your-token-here"
export POLARION_PROJECT="OSE"
export POLARION_VERIFY_SSL="false"
```

### Claude Desktop Config
```json
{
  "mcpServers": {
    "polarion": {
      "command": "python3",
      "args": [
        "/Users/rrasouli/Documents/GitHub/polarion-mcp-server/server.py"
      ],
      "env": {
        "POLARION_TOKEN": "${POLARION_TOKEN}",
        "POLARION_URL": "https://polarion.engineering.redhat.com",
        "POLARION_PROJECT": "OSE",
        "POLARION_VERIFY_SSL": "false"
      }
    }
  }
}
```

## Usage Examples

### Create Test Case with Steps
```python
# Create the test case
result = create_polarion_test_case(
    title="Verify certificate validation",
    description="Test certificates from controllerConfig",
    severity="should_have"
)

# Add test steps
add_test_steps_to_testcase(
    test_case_id="OCP-88278",
    test_steps=[
        {"step": "Check config", "expectedResult": "Config exists"},
        {"step": "Verify certs", "expectedResult": "Certs valid"}
    ]
)
```

### Create Test Run and Update Results
```python
# Create test run
create_test_run(
    title="Sprint 123 Tests",
    template="Release Test",
    test_case_ids=["OCP-88278", "OCP-88279"]
)

# Update results
update_test_run_result(
    test_run_id="OSE-TR-12345",
    test_case_id="OCP-88278",
    result="passed",
    comment="All checks passed"
)
```

### Import JUnit Results
```python
import_junit_results(
    junit_file="/tmp/junit-results.xml",
    test_run_id="OSE-TR-12345",
    map_test_ids={
        "com.example.Test.testCert": "OCP-88278"
    }
)
```

### Export/Import Spreadsheets
```python
# Export
export_test_cases_to_spreadsheet(
    query="title:Windows",
    output_file="/tmp/tests.xlsx",
    include_test_steps=True
)

# Import
import_test_cases_from_spreadsheet(
    spreadsheet_file="/tmp/new-tests.xlsx"
)
```

## Testing

Test the connection:
```bash
python3 << EOF
from polarion_client import PolarionClient
import os

client = PolarionClient(
    url=os.getenv("POLARION_URL"),
    token=os.getenv("POLARION_TOKEN"),
    verify_ssl=False
)

result = client.test_connection("OSE")
print(result)
EOF
```

## Dependencies

- Python 3.8+
- fastmcp >= 3.0.0
- requests >= 2.31.0
- openpyxl >= 3.1.0 (for Excel support)
- urllib3 >= 2.0.0

## Documentation

- `README.md` - Complete user guide with examples
- `API.md` - Full API reference for all 12 tools
- `CHANGELOG.md` - Version history
- Examples in `examples/` directory

## Key Achievements

1. Full MCP server implementation with 12 tools
2. Discovered undocumented Polarion REST API endpoints
3. JUnit integration for automated test reporting
4. Spreadsheet integration for bulk operations
5. Production-ready with error handling
6. Comprehensive documentation
7. Standalone and Claude Desktop support

## Use Cases

- Automated test result reporting from CI/CD
- Bulk test case creation and updates
- Test run management and tracking
- Integration with existing test frameworks
- Spreadsheet-based test case management
- API-driven Polarion workflows

## Future Enhancements

- Attachment management
- Custom field support
- Advanced query builder UI
- Test run templates
- Additional integration formats
- CLI interface
- Webhook support

## License

MIT License - See LICENSE file

## Support

- Documentation: See README.md and API.md
- Examples: See examples/ directory
- Issues: Create GitHub issue
- Internal: Red Hat WINC team

## Version

1.0.0 - Initial release (2026-03-12)
