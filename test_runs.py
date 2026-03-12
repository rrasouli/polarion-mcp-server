"""
Test Run Management
Handles creation and management of Polarion test runs
"""

from typing import Optional, Dict, Any, List


class TestRunManager:
    """Manager for Polarion test run operations"""

    def __init__(self, client):
        self.client = client

    def create_test_run(
        self,
        title: str,
        template: str,
        project_id: str,
        test_case_ids: Optional[List[str]] = None,
        query: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new test run"""

        test_run_data = {
            "data": [{
                "type": "testruns",
                "attributes": {
                    "title": title,
                    "template": template,
                    "projectId": project_id
                }
            }]
        }

        # Add test cases via query or IDs
        if query:
            test_run_data["data"][0]["attributes"]["query"] = query
        elif test_case_ids:
            test_run_data["data"][0]["relationships"] = {
                "testCases": {
                    "data": [
                        {"type": "workitems", "id": f"{project_id}/{tc_id}"}
                        for tc_id in test_case_ids
                    ]
                }
            }

        result = self.client._make_request(
            "POST",
            f"projects/{project_id}/testruns",
            data=test_run_data
        )

        if "error" in result:
            return {
                "status": "failed",
                "error": result["error"]
            }

        test_run = result.get("data", [{}])[0] if isinstance(result.get("data"), list) else result.get("data", {})
        test_run_id = test_run.get("id", "unknown")

        return {
            "status": "success",
            "message": "Test run created successfully",
            "test_run_id": test_run_id,
            "title": title,
            "url": f"{self.client.url}/polarion/#/project/{project_id}/testrun?id={test_run_id}"
        }

    def update_test_result(
        self,
        test_run_id: str,
        test_case_id: str,
        result: str,
        project_id: str,
        comment: Optional[str] = None,
        executed_by: Optional[str] = None,
        duration: Optional[int] = None
    ) -> Dict[str, Any]:
        """Update test result within a test run"""

        # Build the test record update
        attributes = {
            "result": result
        }

        if comment:
            attributes["comment"] = {
                "type": "text/html",
                "value": comment.replace("\n", "<br/>")
            }

        if executed_by:
            attributes["executedBy"] = executed_by

        if duration:
            attributes["duration"] = duration

        update_data = {
            "data": {
                "type": "testrecords",
                "attributes": attributes
            }
        }

        # Update the test record
        # Note: We need to find the test record ID first
        endpoint = f"projects/{project_id}/testruns/{test_run_id}/testrecords/{test_case_id}"

        result_data = self.client._make_request(
            "PATCH",
            endpoint,
            data=update_data
        )

        if "error" in result_data:
            return {
                "status": "failed",
                "error": result_data["error"]
            }

        return {
            "status": "success",
            "message": f"Updated result for {test_case_id} in {test_run_id}",
            "test_run_id": test_run_id,
            "test_case_id": test_case_id,
            "result": result
        }

    def get_test_run_status(
        self,
        test_run_id: str,
        project_id: str
    ) -> Dict[str, Any]:
        """Get test run status and statistics"""

        result = self.client._make_request(
            "GET",
            f"projects/{project_id}/testruns/{test_run_id}"
        )

        if "error" in result:
            return {
                "status": "failed",
                "error": result["error"]
            }

        test_run = result.get("data", {}).get("attributes", {})

        # Get test records
        records_result = self.client._make_request(
            "GET",
            f"projects/{project_id}/testruns/{test_run_id}/testrecords"
        )

        records = records_result.get("data", [])

        # Calculate statistics
        stats = {
            "total": len(records),
            "passed": 0,
            "failed": 0,
            "blocked": 0,
            "not_executed": 0
        }

        for record in records:
            result_val = record.get("attributes", {}).get("result", "not_executed")
            if result_val == "passed":
                stats["passed"] += 1
            elif result_val == "failed":
                stats["failed"] += 1
            elif result_val == "blocked":
                stats["blocked"] += 1
            else:
                stats["not_executed"] += 1

        return {
            "status": "success",
            "test_run_id": test_run_id,
            "title": test_run.get("title"),
            "run_status": test_run.get("status"),
            "statistics": stats,
            "url": f"{self.client.url}/polarion/#/project/{project_id}/testrun?id={test_run_id}"
        }

    def add_test_cases_to_run(
        self,
        test_run_id: str,
        test_case_ids: List[str],
        project_id: str
    ) -> Dict[str, Any]:
        """Add additional test cases to an existing test run"""

        update_data = {
            "data": [
                {"type": "workitems", "id": f"{project_id}/{tc_id}"}
                for tc_id in test_case_ids
            ]
        }

        result = self.client._make_request(
            "POST",
            f"projects/{project_id}/testruns/{test_run_id}/relationships/testCases",
            data=update_data
        )

        if "error" in result:
            return {
                "status": "failed",
                "error": result["error"]
            }

        return {
            "status": "success",
            "message": f"Added {len(test_case_ids)} test cases to {test_run_id}",
            "test_run_id": test_run_id,
            "added_count": len(test_case_ids)
        }
