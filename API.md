# Polarion MCP Server - API Reference

Complete API reference for all available MCP tools.

## Connection Management

### test_polarion_connection

Test connection to Polarion and verify authentication.

**Returns:**
```json
{
  "status": "success",
  "message": "Successfully connected to Polarion",
  "polarion_url": "https://polarion.engineering.redhat.com",
  "project_id": "OSE",
  "project_name": "OpenShift",
  "authentication": "verified"
}
```

## Test Case Management

### create_polarion_test_case

Create a new test case in Polarion.

**Parameters:**
- `title` (string, required): Test case title
- `description` (string, required): Detailed description
- `project_id` (string, optional): Project ID (default: from env)
- `test_steps` (string, optional): Test steps (newline-separated)
- `expected_results` (string, optional): Expected outcomes
- `severity` (string, optional): must_have, should_have, nice_to_have, will_not_have (default: should_have)
- `status` (string, optional): draft, approved, etc. (default: draft)

**Returns:**
```json
{
  "status": "success",
  "message": "Test case created successfully",
  "test_case_id": "OSE/OCP-88278",
  "title": "Test case title",
  "project": "OSE",
  "url": "https://polarion.../workitem?id=OSE/OCP-88278"
}
```

### add_test_steps_to_testcase

Add or replace test steps for a test case.

**Parameters:**
- `test_case_id` (string, required): Test case ID (e.g., "OCP-88278")
- `test_steps` (array, required): List of test steps
  ```json
  [
    {
      "step": "Step description",
      "expectedResult": "Expected result"
    }
  ]
  ```
- `project_id` (string, optional): Project ID (default: from env)

**Returns:**
```json
{
  "status": "success",
  "message": "Added 9 test steps to OCP-88278",
  "test_case_id": "OCP-88278",
  "steps_added": 9,
  "url": "https://polarion.../workitem?id=OCP-88278"
}
```

### get_polarion_test_case

Retrieve details of a specific test case.

**Parameters:**
- `test_case_id` (string, required): Test case ID
- `project_id` (string, optional): Project ID (default: from env)
- `include_test_steps` (boolean, optional): Include test steps (default: true)

**Returns:**
```json
{
  "status": "success",
  "test_case_id": "OCP-88278",
  "title": "Test title",
  "type": "testcase",
  "status": "draft",
  "severity": "should_have",
  "description": "Test description...",
  "url": "https://polarion.../workitem?id=OCP-88278"
}
```

### update_polarion_test_case

Update an existing test case.

**Parameters:**
- `test_case_id` (string, required): Test case ID
- `project_id` (string, optional): Project ID (default: from env)
- `title` (string, optional): New title
- `description` (string, optional): New description
- `status` (string, optional): New status
- `severity` (string, optional): New severity

**Returns:**
```json
{
  "status": "success",
  "message": "Test case OCP-88278 updated successfully",
  "updated_fields": ["title", "status"]
}
```

### search_polarion_test_cases

Search for test cases using Polarion query language.

**Parameters:**
- `query` (string, required): Polarion query (e.g., "title:Windows AND author:rrasouli")
- `project_id` (string, optional): Project ID (default: from env)
- `limit` (integer, optional): Max results (default: 10)

**Returns:**
```json
{
  "status": "success",
  "query": "title:Windows",
  "total_results": 5,
  "test_cases": [
    {
      "id": "OSE/OCP-88278",
      "title": "Test title",
      "status": "draft",
      "severity": "should_have",
      "url": "https://polarion.../workitem?id=OSE/OCP-88278"
    }
  ]
}
```

## Test Run Management

### create_test_run

Create a new test run.

**Parameters:**
- `title` (string, required): Test run title
- `template` (string, required): Template name (e.g., "Release Test")
- `project_id` (string, optional): Project ID (default: from env)
- `test_case_ids` (array, optional): Test case IDs to include
- `query` (string, optional): Query to select test cases

**Returns:**
```json
{
  "status": "success",
  "message": "Test run created successfully",
  "test_run_id": "OSE-TR-12345",
  "title": "Sprint 123 - Certificate Tests",
  "url": "https://polarion.../testrun?id=OSE-TR-12345"
}
```

### update_test_run_result

Update the result of a test case within a test run.

**Parameters:**
- `test_run_id` (string, required): Test run ID
- `test_case_id` (string, required): Test case ID
- `result` (string, required): passed, failed, blocked
- `project_id` (string, optional): Project ID (default: from env)
- `comment` (string, optional): Comment about the result
- `executed_by` (string, optional): Who executed the test
- `duration` (integer, optional): Duration in seconds

**Returns:**
```json
{
  "status": "success",
  "message": "Updated result for OCP-88278 in OSE-TR-12345",
  "test_run_id": "OSE-TR-12345",
  "test_case_id": "OCP-88278",
  "result": "passed"
}
```

### get_test_run_status

Get the status and summary of a test run.

**Parameters:**
- `test_run_id` (string, required): Test run ID
- `project_id` (string, optional): Project ID (default: from env)

**Returns:**
```json
{
  "status": "success",
  "test_run_id": "OSE-TR-12345",
  "title": "Sprint 123 Tests",
  "run_status": "in_progress",
  "statistics": {
    "total": 10,
    "passed": 7,
    "failed": 2,
    "blocked": 1,
    "not_executed": 0
  },
  "url": "https://polarion.../testrun?id=OSE-TR-12345"
}
```

## Integration Tools

### import_junit_results

Import test results from JUnit XML file.

**Parameters:**
- `junit_file` (string, required): Path to JUnit XML file
- `test_run_id` (string, required): Test run ID to update
- `project_id` (string, optional): Project ID (default: from env)
- `map_test_ids` (object, optional): Mapping of JUnit test names to Polarion IDs
  ```json
  {
    "com.example.Test.testMethod": "OCP-88278"
  }
  ```
- `auto_create_test_run` (boolean, optional): Create test run if missing (default: false)

**Returns:**
```json
{
  "status": "success",
  "message": "Imported 15 of 20 test results",
  "junit_file": "/tmp/junit-results.xml",
  "test_run_id": "OSE-TR-12345",
  "statistics": {
    "total": 20,
    "imported": 15,
    "skipped": 5,
    "errors": ["No mapping for com.example.Test.unknownTest"]
  }
}
```

### export_test_cases_to_spreadsheet

Export test cases to Excel or CSV spreadsheet.

**Parameters:**
- `query` (string, required): Polarion query to select test cases
- `output_file` (string, required): Output file path (.xlsx or .csv)
- `project_id` (string, optional): Project ID (default: from env)
- `include_test_steps` (boolean, optional): Include test steps (default: true)
- `format` (string, optional): xlsx or csv (default: xlsx)

**Returns:**
```json
{
  "status": "success",
  "message": "Exported 25 test cases to /tmp/tests.xlsx",
  "output_file": "/tmp/tests.xlsx",
  "test_cases_count": 25
}
```

### import_test_cases_from_spreadsheet

Bulk import test cases from spreadsheet.

**Parameters:**
- `spreadsheet_file` (string, required): Input spreadsheet path (.xlsx or .csv)
- `project_id` (string, optional): Project ID (default: from env)
- `update_existing` (boolean, optional): Update existing test cases (default: false)

**Returns:**
```json
{
  "status": "success",
  "message": "Imported 10 test cases",
  "spreadsheet_file": "/tmp/new-tests.xlsx",
  "statistics": {
    "total": 12,
    "created": 10,
    "updated": 0,
    "errors": ["Skipped row with no title", "Failed to create..."]
  }
}
```

## Error Handling

All tools return error information in a consistent format:

```json
{
  "status": "failed",
  "error": "Error message here",
  "details": {...}
}
```

Common error scenarios:
- Authentication failure (401)
- Resource not found (404)
- Validation errors (400)
- Permission denied (403)

## Polarion Query Language

Examples of queries for searching test cases:

- `type:testcase` - All test cases
- `type:testcase AND title:Windows` - Test cases with "Windows" in title
- `type:testcase AND author:rrasouli` - Test cases by specific author
- `type:testcase AND status:approved` - Only approved test cases
- `type:testcase AND severity:must_have` - Critical test cases
- `type:testcase AND (title:Windows OR title:Linux)` - Multiple criteria

## REST API Endpoints

The server uses these Polarion REST API endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/projects/{id}` | GET | Get project info |
| `/projects/{id}/workitems` | POST | Create workitem |
| `/projects/{id}/workitems` | GET | Search workitems |
| `/projects/{id}/workitems/{id}` | GET | Get workitem |
| `/projects/{id}/workitems/{id}` | PATCH | Update workitem |
| `/projects/{id}/workitems/{id}/teststeps` | POST | Add test steps |
| `/projects/{id}/workitems/{id}/teststeps/{i}` | GET | Get test step |
| `/projects/{id}/workitems/{id}/teststeps/{i}` | DELETE | Delete test step |
| `/projects/{id}/testruns` | POST | Create test run |
| `/projects/{id}/testruns/{id}` | GET | Get test run |
| `/projects/{id}/testruns/{id}/testrecords/{id}` | PATCH | Update test result |
