# Usage Guide

Comprehensive guide to using the AI Contract Testing Platform.

## Table of Contents

1. [Basic Workflows](#basic-workflows)
2. [Command Reference](#command-reference)
3. [Spec File Format](#spec-file-format)
4. [Working with Generated Tests](#working-with-generated-tests)
5. [Advanced Usage](#advanced-usage)
6. [Best Practices](#best-practices)

---

## Basic Workflows

### Workflow 1: Compare Two Specs

```bash
python3 cli.py compare --old specs/spec_v1.json --new specs/spec_v2.json
```

**Output:**
```
Differences detected:
- Endpoint added: /health ['GET']
- Endpoint /order GET: field 'currency' added (type: string)
- Endpoint /widget GET: field 'reviewUrl' added (type: string)
- Endpoint /widget GET: field 'amount' type changed from number to string
```

**Use cases:**
- Quick diff check before deploying API changes
- Documentation of breaking changes
- Input for release notes

### Workflow 2: Generate Contract Tests

```bash
python3 cli.py generate-tests \
  --old specs/spec_v1.json \
  --new specs/spec_v2.json \
  --output tests/test_my_contract.py
```

**Output:**
```
Changes detected between specs:
- Endpoint added: /health ['GET']
- Endpoint /order GET: field 'currency' added (type: string)
- Endpoint /widget GET: field 'reviewUrl' added (type: string)
- Endpoint /widget GET: field 'amount' type changed from number to string

Calling local LLM via Ollama to generate pytest contract tests...

Generated tests written to: tests/test_my_contract.py
```

**Use cases:**
- Bootstrap test suite for new API version
- Generate backward compatibility tests
- Automated test creation in CI/CD

### Workflow 3: Run Generated Tests

```bash
# Run all tests
python3 -m pytest tests/test_my_contract.py

# Run with verbose output
python3 -m pytest tests/test_my_contract.py -v

# Run specific test
python3 -m pytest tests/test_my_contract.py::test_widget_get_response_schema
```

**Expected output:**
```
============================= test session starts ==============================
tests/test_my_contract.py::test_widget_get_response_schema PASSED
tests/test_my_contract.py::test_order_get_response_schema PASSED
...
============================== 5 passed in 0.01s ================================
```

### Workflow 4: Iterative Development

```bash
# 1. Create or modify spec_v2.json
vim specs/spec_v2.json

# 2. Check what changed
python3 cli.py compare --old specs/spec_v1.json --new specs/spec_v2.json

# 3. Generate tests
python3 cli.py generate-tests \
  --old specs/spec_v1.json \
  --new specs/spec_v2.json \
  --output tests/test_contract_generated.py

# 4. Review and fix generated tests
vim tests/test_contract_generated.py

# 5. Run tests
python3 -m pytest tests/test_contract_generated.py -v
```

---

## Command Reference

### `compare` Command

Compare two API specs and show human-readable differences.

**Syntax:**
```bash
python3 cli.py compare --old <old_spec> --new <new_spec>
```

**Arguments:**
- `--old`: Path to old/original spec (JSON file)
- `--new`: Path to new/updated spec (JSON file)

**Example:**
```bash
python3 cli.py compare --old specs/spec_v1.json --new specs/spec_v2.json
```

**Output format:**
```
Differences detected:
- <change_type>: <details>
- <change_type>: <details>
...
```

**Change types:**
- `Endpoint added: <path> [<methods>]`
- `Endpoint removed: <path> [<methods>]`
- `Endpoint <path>: method <HTTP_METHOD> added`
- `Endpoint <path>: method <HTTP_METHOD> removed`
- `Endpoint <path> <METHOD>: field '<name>' added (type: <type>)`
- `Endpoint <path> <METHOD>: field '<name>' removed (type: <type>)`
- `Endpoint <path> <METHOD>: field '<name>' type changed from <old_type> to <new_type>`

**Exit codes:**
- `0`: Success (changes detected or no changes)
- `1`: Error (file not found, invalid JSON, etc.)

---

### `generate-tests` Command

Generate pytest test file from spec differences using local LLM.

**Syntax:**
```bash
python3 cli.py generate-tests --old <old_spec> --new <new_spec> --output <test_file>
```

**Arguments:**
- `--old`: Path to old/original spec (JSON file)
- `--new`: Path to new/updated spec (JSON file)
- `--output`: Path for generated pytest file (e.g., `tests/test_contract.py`)

**Example:**
```bash
python3 cli.py generate-tests \
  --old specs/spec_v1.json \
  --new specs/spec_v2.json \
  --output tests/test_contract_generated.py
```

**Output:**
1. Prints detected changes
2. Calls Ollama LLM to generate tests
3. Writes Python test code to specified file
4. Displays success message with pytest run command

**Exit codes:**
- `0`: Success (tests generated)
- `1`: Error (Ollama unreachable, file write failed, etc.)

**Notes:**
- Requires Ollama to be running (`ollama serve`)
- Generation time: 10-60 seconds depending on model and system
- Output may require manual review/fixes

---

## Spec File Format

### Structure

```json
{
  "version": "1.0.0",
  "paths": {
    "<endpoint_path>": {
      "<HTTP_METHOD>": {
        "response": {
          "status": <status_code>,
          "schema": {
            "<field_name>": "<field_type>",
            ...
          }
        }
      }
    }
  }
}
```

### Example

```json
{
  "version": "1.0.0",
  "paths": {
    "/users": {
      "GET": {
        "response": {
          "status": 200,
          "schema": {
            "id": "string",
            "username": "string",
            "email": "string",
            "created_at": "string"
          }
        }
      },
      "POST": {
        "response": {
          "status": 201,
          "schema": {
            "id": "string",
            "username": "string"
          }
        }
      }
    }
  }
}
```

### Supported Field Types

- `"string"` - String values
- `"number"` - Numeric values (int or float)
- `"boolean"` - Boolean values (true/false)

**Note:** Currently only response schemas are compared. Request bodies and parameters are not yet supported.

---

## Working with Generated Tests

### Review Generated Tests

Generated tests may need manual fixes. Common issues:

1. **Markdown code fences** - Remove ` ``` ` if present
2. **External libraries** - Replace `jsonschema` with stdlib assertions
3. **Invalid syntax** - Fix any Python syntax errors
4. **Incomplete coverage** - Add missing test cases

### Example: Manually Fixing Generated Test

**Before (LLM output):**
```python
```
import pytest
from jsonschema import validate

def test_example():
    validate({"id": "123"}, {"type": "object"})
```
```

**After (fixed):**
```python
import pytest

def test_example():
    """Test example endpoint response."""
    response = {"id": "123"}
    assert "id" in response
    assert isinstance(response["id"], str)
```

### Running Tests

```bash
# Run all generated tests
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_contract_generated.py -v

# Run specific test function
python3 -m pytest tests/test_contract_generated.py::test_widget_get_response_schema -v

# Run with coverage (if pytest-cov installed)
python3 -m pytest tests/ --cov=. --cov-report=html
```

---

## Advanced Usage

### Custom Spec Paths

```bash
# Compare specs from different directories
python3 cli.py compare \
  --old /path/to/production/spec.json \
  --new /path/to/staging/spec.json

# Generate tests for custom locations
python3 cli.py generate-tests \
  --old ~/api/v1/spec.json \
  --new ~/api/v2/spec.json \
  --output ~/tests/test_v1_to_v2.py
```

### Scripting and Automation

```bash
#!/bin/bash
# auto_test_generation.sh

OLD_SPEC="specs/spec_v1.json"
NEW_SPEC="specs/spec_v2.json"
OUTPUT_DIR="tests/generated"

mkdir -p "$OUTPUT_DIR"

echo "Comparing specs..."
python3 cli.py compare --old "$OLD_SPEC" --new "$NEW_SPEC"

if [ $? -eq 0 ]; then
    echo "Generating tests..."
    python3 cli.py generate-tests \
        --old "$OLD_SPEC" \
        --new "$NEW_SPEC" \
        --output "$OUTPUT_DIR/test_contract_$(date +%Y%m%d).py"

    echo "Running tests..."
    python3 -m pytest "$OUTPUT_DIR/" -v
fi
```

### CI/CD Integration

**GitHub Actions example:**

```yaml
name: Contract Test Generation

on:
  pull_request:
    paths:
      - 'specs/**'

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pytest requests

      - name: Install Ollama
        run: |
          curl -fsSL https://ollama.com/install.sh | sh
          ollama serve &
          sleep 5
          ollama pull llama3

      - name: Compare specs
        run: |
          python3 cli.py compare \
            --old specs/spec_v1.json \
            --new specs/spec_v2.json

      - name: Generate contract tests
        run: |
          python3 cli.py generate-tests \
            --old specs/spec_v1.json \
            --new specs/spec_v2.json \
            --output tests/test_contract_generated.py

      - name: Run tests
        run: |
          python3 -m pytest tests/ -v
```

---

## Best Practices

### 1. Version Your Specs

```
specs/
├── v1.0.0_spec.json
├── v1.1.0_spec.json
└── v2.0.0_spec.json
```

### 2. Review Before Committing

Always manually review generated tests before committing to version control.

### 3. Keep Tests Alongside Specs

```
project/
├── specs/
│   ├── spec_v1.json
│   └── spec_v2.json
└── tests/
    ├── test_contract_v1_to_v2.py
    └── test_manual_cases.py
```

### 4. Document Breaking Changes

Use the `compare` output in your CHANGELOG:

```markdown
## [2.0.0] - 2025-12-04

### Breaking Changes
- `/widget` GET: field 'amount' type changed from number to string
- Required field 'currency' added to `/order` GET response

### Added
- New endpoint: `/health` GET
```

### 5. Iterate on Prompts

If generated tests are consistently poor:
1. Review `prompts/test_generation_v3.md`
2. Identify issues
3. Create `prompts/test_generation_v4.md` with improvements
4. Update `ai_client_ollama.py` to use new prompt

### 6. Use Spec as Source of Truth

Keep spec files updated whenever API changes. Then:
```bash
python3 cli.py compare --old specs/prod.json --new specs/staging.json
```

---

## Troubleshooting Common Issues

### Issue: No differences detected

**Check:**
- Files are different (use `diff` or JSON diff tool)
- Spec structure matches expected format
- Field names are exact matches (case-sensitive)

### Issue: Generated tests fail to run

**Solutions:**
1. Check for syntax errors: `python3 -m py_compile tests/test_generated.py`
2. Look for markdown fences or invalid imports
3. Review manually-fixed example: `tests/test_contract_generated.py`

### Issue: Tests pass but don't validate correctly

**Review:**
- Test payload data matches spec types
- All required fields are checked
- Type assertions use correct Python types

---

## Examples

See these files for working examples:
- `specs/spec_v1.json` - Original spec
- `specs/spec_v2.json` - Updated spec with changes
- `tests/test_contract_generated.py` - Manually-fixed working tests
- `prompts/test_generation_v3.md` - Current prompt used for generation
