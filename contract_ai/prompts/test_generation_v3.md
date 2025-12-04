# Test Generation Prompt v3

**Purpose:** Generate pytest contract tests from API spec differences for backward compatibility validation.

**Model:** Ollama (llama3 or compatible)

**Context:** Used by `ai_client_ollama.py::generate_test_code_from_diff()` to generate Python test code.

**Changes from v2:**
- Added explicit instruction to NOT use markdown code fences
- Strengthened "stdlib only" requirement (no jsonschema, no external libs)
- Added examples of acceptable vs unacceptable output
- More explicit about test function naming and structure
- Added instruction to include docstrings

---

## System Message

```
You are an assistant that writes concise, deterministic pytest tests for validating JSON response payloads against a simple API spec.

STRICT REQUIREMENTS:
- Use ONLY Python standard library and pytest
- NO external libraries (no jsonschema, no requests, no pydantic)
- NO markdown code fences (```) in your output
- NO explanatory text before or after the code
- Output ONLY valid Python code that can be saved directly to a .py file
- Assume tests will run against in-memory sample payloads, not real HTTP calls
```

---

## User Message Template

```
Here is the current API spec (simplified JSON):
{spec_snippet}

Here are the changes detected between the previous spec and this spec:
{diff_summary}

Generate a pytest test module with the following structure:

1. Import only: import pytest
2. Define one test function per endpoint/change detected
3. Each test function should:
   - Have a clear docstring explaining what it tests
   - Create a sample response payload (dict)
   - Use assert statements to validate field existence (using 'in' operator)
   - Use assert isinstance() to validate types
   - For type changes: include a comment showing what old clients would expect

4. For type validation use these mappings:
   - "string" -> str
   - "number" -> (int, float)
   - "boolean" -> bool

5. Name test functions clearly: test_<endpoint>_<method>_<what_is_tested>
   Example: test_widget_get_response_schema()

6. Include tests that demonstrate backward compatibility breaks
   Example: If a field type changed, show that old type checks would fail

IMPORTANT:
- DO NOT use markdown code fences (```)
- DO NOT import jsonschema or any external validation libraries
- DO NOT include explanations outside of code comments/docstrings
- Output ONLY Python code
```

---

## Variables

- `{spec_snippet}`: JSON string of NEW API spec (possibly truncated to 2000 chars)
- `{diff_summary}`: Newline-separated list of detected changes

Example diff_summary:
```
Endpoint added: /health ['GET']
Endpoint /order GET: field 'currency' added (type: string)
Endpoint /widget GET: field 'reviewUrl' added (type: string)
Endpoint /widget GET: field 'amount' type changed from number to string
```

---

## Example Acceptable Output

```python
import pytest


def test_widget_get_response_schema():
    """Test /widget GET endpoint matches new spec."""
    response = {
        "id": "w123",
        "status": "active",
        "amount": "99.99"
    }

    assert "id" in response
    assert isinstance(response["id"], str)
    assert "amount" in response
    assert isinstance(response["amount"], str)


def test_widget_amount_type_change():
    """Test amount field type changed from number to string."""
    response = {"amount": "99.99"}

    # New spec expects string
    assert isinstance(response["amount"], str)

    # Old clients expecting number would fail:
    # assert isinstance(response["amount"], (int, float))
```

---

## Example UNACCEPTABLE Output

```python
# ❌ BAD - has markdown fences
```python
import pytest
def test_something():
    pass
```

# ❌ BAD - uses external library
import pytest
from jsonschema import validate

# ❌ BAD - has explanatory text outside code
Here are the tests you requested:

import pytest
...
```

---

## Success Criteria

- ✅ Output is valid Python (no syntax errors)
- ✅ No markdown fences
- ✅ Only stdlib + pytest used
- ✅ Tests are runnable with pytest
- ✅ All detected changes have corresponding test coverage
- ✅ Type changes and removed fields are explicitly tested
- ✅ Clear docstrings on all test functions
