#!/usr/bin/env python3
"""
Example: Create a Test Case with Steps
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from polarion_client import PolarionClient

# Initialize client
client = PolarionClient(
    url=os.getenv("POLARION_URL"),
    token=os.getenv("POLARION_TOKEN"),
    verify_ssl=False
)

# Create test case
result = client.create_test_case(
    title="Example: Verify certificate validation",
    description="Test that certificates are correctly read from controllerConfig",
    project_id=os.getenv("POLARION_PROJECT", "OSE"),
    severity="should_have",
    status="draft"
)

print(f"Created test case: {result}")

# Add test steps
if result.get("status") == "success":
    test_case_id = result.get("test_case_id", "").split("/")[-1]

    steps = [
        {
            "step": "Verify Windows nodes are ready: <code>oc get nodes -l kubernetes.io/os=windows</code>",
            "expectedResult": "All Windows nodes show STATUS 'Ready'"
        },
        {
            "step": "Query controllerConfig: <code>oc get controllerconfig machine-config-controller -o yaml</code>",
            "expectedResult": "controllerConfig contains certificate data"
        },
        {
            "step": "Verify certificates on nodes",
            "expectedResult": "All certificates match controllerConfig"
        }
    ]

    steps_result = client.add_test_steps(
        test_case_id=test_case_id,
        test_steps=steps,
        project_id=os.getenv("POLARION_PROJECT", "OSE")
    )

    print(f"Added test steps: {steps_result}")
