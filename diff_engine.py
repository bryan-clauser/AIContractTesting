"""
API specification diff engine.
Compares two simplified API specs and detects changes.
"""
import json
from typing import Dict, List, Any, Set


def load_spec(path: str) -> Dict[str, Any]:
    """Load API spec from JSON file."""
    with open(path, 'r') as f:
        return json.load(f)


def diff_specs(old_spec: Dict[str, Any], new_spec: Dict[str, Any]) -> List[str]:
    """
    Compare two API specs and return list of human-readable changes.

    Expected spec structure:
    {
        "version": "1.0.0",
        "paths": {
            "/widget": {
                "GET": {
                    "response": {
                        "status": 200,
                        "schema": {
                            "id": "string",
                            "status": "string",
                            ...
                        }
                    }
                }
            }
        }
    }

    Returns:
        List of change descriptions (e.g., "Endpoint /users GET: field 'email' removed")
    """
    changes = []

    old_endpoints = old_spec.get("paths", {})
    new_endpoints = new_spec.get("paths", {})

    # Detect endpoint-level changes
    old_paths = set(old_endpoints.keys())
    new_paths = set(new_endpoints.keys())

    added_paths = new_paths - old_paths
    removed_paths = old_paths - new_paths
    common_paths = old_paths & new_paths

    for path in sorted(added_paths):
        methods = list(new_endpoints[path].keys())
        changes.append(f"Endpoint added: {path} {methods}")

    for path in sorted(removed_paths):
        methods = list(old_endpoints[path].keys())
        changes.append(f"Endpoint removed: {path} {methods}")

    # Detect method and field-level changes for common paths
    for path in sorted(common_paths):
        old_methods = old_endpoints[path]
        new_methods = new_endpoints[path]

        old_method_names = set(old_methods.keys())
        new_method_names = set(new_methods.keys())

        added_methods = new_method_names - old_method_names
        removed_methods = old_method_names - new_method_names
        common_methods = old_method_names & new_method_names

        for method in sorted(added_methods):
            changes.append(f"Endpoint {path}: method {method} added")

        for method in sorted(removed_methods):
            changes.append(f"Endpoint {path}: method {method} removed")

        # Compare response schemas for common methods
        for method in sorted(common_methods):
            old_response = old_methods[method].get("response", {}).get("schema", {})
            new_response = new_methods[method].get("response", {}).get("schema", {})

            field_changes = _diff_fields(path, method, old_response, new_response)
            changes.extend(field_changes)

    return changes


def _diff_fields(
    path: str,
    method: str,
    old_fields: Dict[str, str],
    new_fields: Dict[str, str]
) -> List[str]:
    """Compare response field schemas between old and new specs."""
    changes = []

    old_field_names = set(old_fields.keys())
    new_field_names = set(new_fields.keys())

    added_fields = new_field_names - old_field_names
    removed_fields = old_field_names - new_field_names
    common_fields = old_field_names & new_field_names

    for field in sorted(added_fields):
        field_type = new_fields[field]
        changes.append(f"Endpoint {path} {method}: field '{field}' added (type: {field_type})")

    for field in sorted(removed_fields):
        field_type = old_fields[field]
        changes.append(f"Endpoint {path} {method}: field '{field}' removed (type: {field_type})")

    # Detect type changes
    for field in sorted(common_fields):
        old_type = old_fields[field]
        new_type = new_fields[field]

        if old_type != new_type:
            changes.append(
                f"Endpoint {path} {method}: field '{field}' type changed from {old_type} to {new_type}"
            )

    return changes
