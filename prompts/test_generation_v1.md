# Test Generation Prompt v1

**Purpose:** Generate pytest contract tests from API spec differences for backward compatibility validation.

**Model:** Ollama (llama3 or compatible)

**Context:** Used by `ai_client_ollama.py` to generate Python test code that validates API responses against spec changes.

---

## Prompt Template

```
You are a Python test generation assistant. Generate pytest tests for API contract validation.

OLD SPEC:
{old_spec_json}

NEW SPEC:
{new_spec_json}

DETECTED CHANGES:
{change_list}

Generate pytest test functions that:
1. Validate response payloads match the NEW spec (correct keys and types)
2. Include test cases that would FAIL if old clients expect removed fields
3. Use pure Python validation (no HTTP calls, just dict/type validation)
4. Follow this pattern for each endpoint:

def test_endpoint_name_response_schema():
    # Simulated response payload
    response = {"field": "value"}

    # Validate required fields exist
    assert "field" in response

    # Validate types
    assert isinstance(response["field"], str)

IMPORTANT:
- Only output valid Python code
- No markdown code fences
- No explanations outside comments
- Include test functions for backward compatibility failures
- Name tests clearly: test_<endpoint>_<scenario>
```

---

## Variables

- `{old_spec_json}`: JSON string of original API spec
- `{new_spec_json}`: JSON string of updated API spec
- `{change_list}`: Newline-separated list of detected changes

---

## Expected Output

Pure Python code containing:
- Pytest test functions
- Inline comments explaining validation logic
- Tests covering both successful validation and backward-compatibility failures

---

## Success Criteria

- Output is valid Python (no syntax errors)
- Tests are runnable with pytest
- All detected changes have corresponding test coverage
- Backward compatibility issues are explicitly tested
