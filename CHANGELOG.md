# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-03-12

### Added
- Initial release of Polarion MCP Server
- Test case management (create, update, search, delete)
- Test steps management via discovered REST API endpoint
- Test run creation and management
- Test run results updates
- JUnit XML import integration
- Spreadsheet (Excel/CSV) import/export
- Full MCP server implementation with FastMCP
- Comprehensive documentation and examples
- Support for Red Hat Engineering Polarion instance

### Discovered
- Undocumented Polarion REST API endpoints for test steps:
  - POST `/projects/{id}/workitems/{id}/teststeps` - Create test steps
  - GET `/projects/{id}/workitems/{id}/teststeps/{index}` - Get test step
  - DELETE `/projects/{id}/workitems/{id}/teststeps/{index}` - Delete test step

### Documentation
- Complete README with usage examples
- API reference for all tools
- Integration guides for JUnit and spreadsheets
- Example scripts for common operations
- Troubleshooting guide

## [Future]

### Planned Features
- Attachment management for test cases and runs
- Custom field support
- Advanced query builder
- Test run templates
- Bulk operations optimization
- Additional integration formats (TestRail, Zephyr)
- Webhook support for CI/CD
- CLI interface for standalone usage
