"""
Polarion REST API Client
Core client for interacting with Polarion REST API
"""

import os
import requests
from typing import Optional, Dict, Any, List


class PolarionClient:
    """Client for Polarion REST API operations"""

    def __init__(self, url: str, token: str, verify_ssl: bool = True):
        self.url = url
        self.token = token
        self.verify_ssl = verify_ssl
        self.base_url = f"{url}/polarion/rest/v1"

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make authenticated request to Polarion REST API"""

        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params,
                timeout=30,
                verify=self.verify_ssl
            )

            if response.status_code == 401:
                return {
                    "error": "Authentication failed. Check POLARION_TOKEN.",
                    "status": 401
                }

            if response.status_code >= 400:
                try:
                    error_data = response.json()
                    return {
                        "error": error_data.get("errors", [{}])[0].get("detail", "Unknown error"),
                        "status": response.status_code,
                        "response": error_data
                    }
                except:
                    return {
                        "error": response.text,
                        "status": response.status_code
                    }

            return response.json() if response.content else {"success": True}

        except Exception as e:
            return {"error": str(e), "status": 0}

    def test_connection(self, project_id: str) -> Dict[str, Any]:
        """Test connection to Polarion"""
        result = self._make_request("GET", f"projects/{project_id}")

        if "error" in result:
            return {
                "status": "failed",
                "message": "Connection test failed",
                "error": result["error"]
            }

        project_data = result.get("data", {})
        return {
            "status": "success",
            "message": "Successfully connected to Polarion",
            "polarion_url": self.url,
            "project_id": project_data.get("id"),
            "project_name": project_data.get("attributes", {}).get("name"),
            "authentication": "verified"
        }

    def create_test_case(
        self,
        title: str,
        description: str,
        project_id: str,
        test_steps: Optional[str] = None,
        expected_results: Optional[str] = None,
        severity: str = "should_have",
        status: str = "draft"
    ) -> Dict[str, Any]:
        """Create a new test case"""

        full_description = description
        if test_steps:
            full_description += f"\n\n## Test Steps\n{test_steps}"
        if expected_results:
            full_description += f"\n\n## Expected Results\n{expected_results}"

        workitem_data = {
            "data": [{
                "type": "workitems",
                "attributes": {
                    "type": "testcase",
                    "title": title,
                    "description": {
                        "type": "text/html",
                        "value": full_description.replace("\n", "<br/>")
                    },
                    "status": status,
                    "severity": severity
                }
            }]
        }

        result = self._make_request(
            "POST",
            f"projects/{project_id}/workitems",
            data=workitem_data
        )

        if "error" in result:
            return {
                "status": "failed",
                "error": result["error"]
            }

        test_case_data = result.get("data", [{}])[0] if isinstance(result.get("data"), list) else result.get("data", {})
        test_case_id = test_case_data.get("id", "unknown")

        return {
            "status": "success",
            "message": "Test case created successfully",
            "test_case_id": test_case_id,
            "title": title,
            "project": project_id,
            "url": f"{self.url}/polarion/#/project/{project_id}/workitem?id={test_case_id}"
        }

    def add_test_steps(
        self,
        test_case_id: str,
        test_steps: List[Dict[str, str]],
        project_id: str
    ) -> Dict[str, Any]:
        """Add test steps to a test case"""

        try:
            # Delete existing test steps first
            check_url = f"projects/{project_id}/workitems/{test_case_id}/relationships/testSteps"
            existing = self._make_request("GET", check_url)

            if "error" not in existing:
                existing_steps = existing.get("data", [])
                for step in existing_steps:
                    step_id = step.get("id", "").split("/")[-1]
                    self._make_request(
                        "DELETE",
                        f"projects/{project_id}/workitems/{test_case_id}/teststeps/{step_id}"
                    )

            # Build test steps payload
            steps_data = []
            for step in test_steps:
                step_obj = {
                    "type": "teststeps",
                    "attributes": {
                        "keys": ["step", "expectedResult"],
                        "values": [
                            {"type": "text/html", "value": step.get("step", "").replace("\n", "<br/>")},
                            {"type": "text/html", "value": step.get("expectedResult", "").replace("\n", "<br/>")}
                        ]
                    }
                }
                steps_data.append(step_obj)

            # POST test steps
            result = self._make_request(
                "POST",
                f"projects/{project_id}/workitems/{test_case_id}/teststeps",
                data={"data": steps_data}
            )

            if "error" in result:
                return {
                    "status": "failed",
                    "error": result["error"]
                }

            created_steps = result.get("data", [])

            return {
                "status": "success",
                "message": f"Added {len(created_steps)} test steps to {test_case_id}",
                "test_case_id": test_case_id,
                "steps_added": len(created_steps),
                "url": f"{self.url}/polarion/#/project/{project_id}/workitem?id={test_case_id}"
            }

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }

    def get_test_case(
        self,
        test_case_id: str,
        project_id: str,
        include_test_steps: bool = True
    ) -> Dict[str, Any]:
        """Get test case details"""

        params = {}
        if include_test_steps:
            params["include"] = "testSteps"

        result = self._make_request(
            "GET",
            f"projects/{project_id}/workitems/{test_case_id}",
            params=params
        )

        if "error" in result:
            return {
                "status": "failed",
                "error": result["error"]
            }

        test_case = result.get("data", {}).get("attributes", {})

        return {
            "status": "success",
            "test_case_id": test_case_id,
            "title": test_case.get("title"),
            "type": test_case.get("type"),
            "status": test_case.get("status"),
            "severity": test_case.get("severity"),
            "description": test_case.get("description", {}).get("value", ""),
            "url": f"{self.url}/polarion/#/project/{project_id}/workitem?id={test_case_id}"
        }

    def update_test_case(
        self,
        test_case_id: str,
        project_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Update test case"""

        attributes = {}
        if kwargs.get("title"):
            attributes["title"] = kwargs["title"]
        if kwargs.get("description"):
            attributes["description"] = {
                "type": "text/html",
                "value": kwargs["description"].replace("\n", "<br/>")
            }
        if kwargs.get("status"):
            attributes["status"] = kwargs["status"]
        if kwargs.get("severity"):
            attributes["severity"] = kwargs["severity"]

        if not attributes:
            return {
                "status": "failed",
                "error": "No fields provided to update"
            }

        update_data = {
            "data": {
                "type": "workitems",
                "id": f"{project_id}/{test_case_id}",
                "attributes": attributes
            }
        }

        result = self._make_request(
            "PATCH",
            f"projects/{project_id}/workitems/{test_case_id}",
            data=update_data
        )

        if "error" in result:
            return {
                "status": "failed",
                "error": result["error"]
            }

        return {
            "status": "success",
            "message": f"Test case {test_case_id} updated successfully",
            "updated_fields": list(attributes.keys())
        }

    def search_test_cases(
        self,
        query: str,
        project_id: str,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Search for test cases"""

        params = {
            "query": f"type:testcase AND {query}",
            "fields[workitems]": "title,type,status,severity",
            "page[size]": limit
        }

        result = self._make_request(
            "GET",
            f"projects/{project_id}/workitems",
            params=params
        )

        if "error" in result:
            return {
                "status": "failed",
                "error": result["error"]
            }

        test_cases = result.get("data", [])
        results = []
        for tc in test_cases:
            tc_id = tc.get("id", "")
            attrs = tc.get("attributes", {})
            results.append({
                "id": tc_id,
                "title": attrs.get("title"),
                "status": attrs.get("status"),
                "severity": attrs.get("severity"),
                "url": f"{self.url}/polarion/#/project/{project_id}/workitem?id={tc_id}"
            })

        return {
            "status": "success",
            "query": query,
            "total_results": len(results),
            "test_cases": results
        }
