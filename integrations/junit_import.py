"""
JUnit XML Results Importer
Import test results from JUnit XML format
"""

import os
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional


class JUnitImporter:
    """Importer for JUnit XML test results"""

    def __init__(self, client):
        self.client = client

    def import_junit_results(
        self,
        junit_file: str,
        test_run_id: str,
        project_id: str,
        map_test_ids: Dict[str, str],
        auto_create_test_run: bool = False
    ) -> Dict[str, Any]:
        """Import JUnit test results into Polarion test run"""

        if not os.path.exists(junit_file):
            return {
                "status": "failed",
                "error": f"JUnit file not found: {junit_file}"
            }

        try:
            tree = ET.parse(junit_file)
            root = tree.getroot()

            results = {
                "total": 0,
                "imported": 0,
                "skipped": 0,
                "errors": []
            }

            # Parse test suites
            for testsuite in root.findall(".//testsuite"):
                for testcase in testsuite.findall("testcase"):
                    results["total"] += 1

                    # Get test case info
                    classname = testcase.get("classname", "")
                    name = testcase.get("name", "")
                    time = float(testcase.get("time", "0"))
                    duration = int(time * 1000)  # Convert to milliseconds

                    # Build test identifier
                    test_identifier = f"{classname}.{name}"

                    # Map to Polarion test case ID
                    polarion_test_id = map_test_ids.get(test_identifier)

                    if not polarion_test_id:
                        results["skipped"] += 1
                        results["errors"].append(
                            f"No mapping for {test_identifier}"
                        )
                        continue

                    # Determine result
                    failure = testcase.find("failure")
                    error = testcase.find("error")
                    skipped = testcase.find("skipped")

                    if failure is not None:
                        result = "failed"
                        comment = f"Failure: {failure.get('message', '')}\n\n{failure.text or ''}"
                    elif error is not None:
                        result = "failed"
                        comment = f"Error: {error.get('message', '')}\n\n{error.text or ''}"
                    elif skipped is not None:
                        result = "blocked"
                        comment = f"Skipped: {skipped.get('message', '')}"
                    else:
                        result = "passed"
                        comment = "Test passed successfully"

                    # Get system output
                    system_out = testcase.find("system-out")
                    if system_out is not None and system_out.text:
                        comment += f"\n\nOutput:\n{system_out.text[:500]}"  # Limit length

                    # Update test result in Polarion
                    from test_runs import TestRunManager
                    test_run_mgr = TestRunManager(self.client)

                    update_result = test_run_mgr.update_test_result(
                        test_run_id=test_run_id,
                        test_case_id=polarion_test_id,
                        result=result,
                        project_id=project_id,
                        comment=comment[:1000],  # Limit comment length
                        duration=duration
                    )

                    if update_result.get("status") == "success":
                        results["imported"] += 1
                    else:
                        results["errors"].append(
                            f"Failed to update {polarion_test_id}: {update_result.get('error')}"
                        )

            return {
                "status": "success",
                "message": f"Imported {results['imported']} of {results['total']} test results",
                "junit_file": junit_file,
                "test_run_id": test_run_id,
                "statistics": results
            }

        except ET.ParseError as e:
            return {
                "status": "failed",
                "error": f"Failed to parse JUnit XML: {str(e)}"
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": f"Import failed: {str(e)}"
            }
