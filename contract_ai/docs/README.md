# AI Contract Testing & Backward Compatibility Platform

A proof-of-concept (POC) hackathon project that automatically generates pytest contract tests from API specification changes using a local LLM (Ollama).

## 🎯 Project Goals

- Automatically detect breaking changes between API spec versions
- Use AI to generate meaningful contract tests for backward compatibility
- Run entirely locally with no external dependencies
- Demonstrate AI-assisted test generation for API validation

## 🏗️ Architecture

```
contract_ai/
├── ai_client_ollama.py          # Ollama LLM client wrapper
├── diff_engine.py               # API spec comparison engine
├── cli.py                       # Command-line interface
├── specs/                       # API specification files
│   ├── spec_v1.json            # Original API spec
│   └── spec_v2.json            # Updated API spec (with breaking changes)
├── tests/                       # Generated and manual test files
│   ├── test_contract_generated.py   # AI-generated tests (manually fixed)
│   └── test_contract_v3.py         # Raw v3 prompt output
├── prompts/                     # Versioned LLM prompts
│   ├── test_generation_v1.md
│   ├── test_generation_v2.md
│   └── test_generation_v3.md
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Ollama installed and running locally
- `llama3` model pulled in Ollama

### Installation

```bash
# Install Python dependencies
pip3 install pytest requests --user

# Start Ollama (in separate terminal)
ollama serve

# Pull llama3 model (if not already done)
ollama pull llama3
```

### Basic Usage

**1. Compare two API specs:**
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

**2. Generate pytest tests from differences:**
```bash
python3 cli.py generate-tests \
  --old specs/spec_v1.json \
  --new specs/spec_v2.json \
  --output tests/test_contract_generated.py
```

**3. Run generated tests:**
```bash
python3 -m pytest tests/test_contract_generated.py -v
```

## 📊 What It Detects

The diff engine identifies:

- ✅ **Endpoint changes**: Added/removed API paths
- ✅ **Method changes**: Added/removed HTTP methods (GET, POST, etc.)
- ✅ **Field changes**: Added/removed fields in response schemas
- ✅ **Type changes**: Breaking type modifications (e.g., number → string)

## 🧪 Example Spec Structure

```json
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
            "amount": "number"
          }
        }
      }
    }
  }
}
```

## 🤖 How It Works

1. **Diff Engine** (`diff_engine.py`):
   - Loads two JSON spec files
   - Compares paths, methods, and response schemas
   - Outputs human-readable change descriptions

2. **LLM Integration** (`ai_client_ollama.py`):
   - Sends diff summary + new spec to local Ollama instance
   - Uses carefully crafted prompts (versioned in `/prompts`)
   - Receives generated Python test code

3. **Test Generation**:
   - Creates pytest tests with assertions for field existence
   - Validates types using `isinstance()`
   - Includes backward compatibility failure cases

## 📝 Prompt Versioning

All LLM prompts are versioned and documented in `/prompts/`:

- **v1**: Initial basic prompt
- **v2**: Added explicit structure requirements
- **v3**: Strict "no external libs" + "no markdown fences" enforcement

See `prompts/test_generation_v3.md` for current prompt details.

## 🎓 Key Learnings

### What Worked Well
- ✅ Diff engine is deterministic and accurate
- ✅ Ollama integration is straightforward
- ✅ Prompt versioning enables iteration
- ✅ Generated tests (after manual fixes) are comprehensive

### Challenges Encountered
- ⚠️ LLM output is non-deterministic (sometimes adds markdown fences)
- ⚠️ LLM occasionally uses external libraries despite instructions
- ⚠️ Prompt engineering requires multiple iterations

### Solutions Applied
- ✅ Explicit "NO markdown fences" in system message
- ✅ Listed forbidden libraries explicitly
- ✅ Added examples of acceptable/unacceptable output
- ✅ Post-generation manual review workflow

## 🔬 Test Results

**Manually fixed tests: 5/5 PASSED ✅**

```
tests/test_contract_generated.py::test_widget_get_response_schema PASSED
tests/test_contract_generated.py::test_widget_amount_type_change PASSED
tests/test_contract_generated.py::test_order_get_response_schema PASSED
tests/test_contract_generated.py::test_order_currency_field_added PASSED
tests/test_contract_generated.py::test_health_get_response_schema PASSED

5 passed in 0.01s
```

## 🛠️ Technology Stack

- **Python 3.11**: Core language
- **Ollama**: Local LLM runtime (llama3 model)
- **pytest**: Test framework
- **requests**: HTTP client for Ollama API
- **argparse**: CLI argument parsing (stdlib)
- **json**: Spec parsing (stdlib)

## 📦 Dependencies

```
requests>=2.31.0
pytest>=7.4.0
```

No external validation libraries (jsonschema, pydantic) required - tests use only Python stdlib.

## 🎯 Future Enhancements

**High Priority:**
- [ ] Add request body schema diffing
- [ ] Support more HTTP methods (POST, PUT, DELETE)
- [ ] Detect required vs optional field changes
- [ ] Output diff in machine-readable format (JSON)

**Medium Priority:**
- [ ] Add LLM output validation/sanitization layer
- [ ] Support multiple LLM models (claude, gpt-4, etc.)
- [ ] Generate test data fixtures automatically
- [ ] Add CI/CD integration examples

**Nice to Have:**
- [ ] Web UI for spec comparison
- [ ] Historical spec versioning tracking
- [ ] Auto-generate migration guides
- [ ] Integration with OpenAPI specs

## 🤝 Contributing

This is a hackathon POC. For production use:
1. Add robust error handling
2. Implement LLM output validation
3. Add comprehensive test suite for diff engine
4. Create Docker container for easy deployment
5. Add support for more spec formats (OpenAPI 3.0, GraphQL)

## 📄 License

MIT License - Hackathon POC Project

## 🙋 Authors

Built for the AI Contract Testing & Backward Compatibility Platform hackathon.

## 📚 Additional Documentation

- `prompts/test_generation_v3.md` - Current LLM prompt
- `tests/test_contract_generated.py` - Example generated tests
- CLI help: `python3 cli.py --help`
