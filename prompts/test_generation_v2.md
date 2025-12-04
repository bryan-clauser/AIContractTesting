# Test Generation Prompt v2

**Purpose:** Generate pytest contract tests from API spec differences for backward compatibility validation.

**Model:** Ollama (llama3 or compatible)

**Context:** Used by `ai_client_ollama.py::generate_test_code_from_diff()` to generate Python test code.

**Changes from v1:**
- Simplified message structure (system + user)
- More explicit instructions for pure Python validation
- Added guidance for handling added/removed fields in tests
- Removed markdown fence handling (model should output pure Python)

---

## System Message

```
You are an assistant that writes concise, deterministic pytest tests for validating JSON response payloads against a simple API spec.
- Use only Python standard library and pytest.
- Do not include explanations or comments, only Python code.
- Assume tests will run against in-memory sample payloads, not real HTTP calls.
```

---

## User Message Template

```
Here is the current API spec (simplified JSON):
{spec_snippet}

Here are the changes detected between the previous spec and this spec:
{diff_summary}

Generate a pytest test module that:
- Defines sample response payloads for the affected endpoints.
- Asserts that required fields exist with the expected simple types (string, number, boolean).
- Includes at least one test that would fail if a removed field is still expected by a client.
- Includes at least one test that checks behavior for any added fields.
Return ONLY valid Python code for a pytest test module.
```

---

## Variables

- `{spec_snippet}`: JSON string of NEW API spec (possibly truncated to 2000 chars)
- `{diff_summary}`: Newline-separated list of detected changes (e.g., "Endpoint /widget GET: field 'amount' type changed from number to string")

---

## Expected Output

Pure Python code containing:
- Pytest test functions
- Sample payloads (dicts) for each affected endpoint
- Type assertions using `isinstance()`
- Field existence checks using `in` operator
- Tests covering backward-compatibility failures

---

## Example Output Structure

```python
def test_widget_get_response_schema():
    response = {
        "id": "abc123",
        "status": "active",
        "amount": "99.99",
        "reviewUrl": "https://example.com/review"
    }

    assert "id" in response
    assert isinstance(response["id"], str)
    assert "amount" in response
    assert isinstance(response["amount"], str)

def test_widget_backward_compat_amount_type():
    # This would fail for old clients expecting number
    response = {"amount": "99.99"}
    # Old code: assert isinstance(response["amount"], (int, float))
    # New code accepts string
    assert isinstance(response["amount"], str)
```

---

## Success Criteria

- Output is valid Python (no syntax errors)
- Tests are runnable with pytest
- All detected changes have corresponding test coverage
- Type changes and removed fields are explicitly tested
