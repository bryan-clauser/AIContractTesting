# Quick Start Guide

Get up and running with AI Contract Testing in 5 minutes.

## Prerequisites Check

```bash
# Check Python version (need 3.11+)
python3 --version

# Check if Ollama is installed
which ollama || echo "Ollama not installed"
```

## 1-Minute Setup

```bash
# Install Python dependencies
pip3 install pytest requests --user

# Start Ollama (in separate terminal)
ollama serve

# Pull llama3 model
ollama pull llama3
```

## First Run

```bash
# Navigate to project
cd /path/to/AIContractTesting/contract_ai

# Compare two specs
python3 cli.py compare --old specs/spec_v1.json --new specs/spec_v2.json

# Expected output:
# Differences detected:
# - Endpoint added: /health ['GET']
# - Endpoint /order GET: field 'currency' added (type: string)
# - Endpoint /widget GET: field 'reviewUrl' added (type: string)
# - Endpoint /widget GET: field 'amount' type changed from number to string
```

## Generate Your First Tests

```bash
# Generate tests
python3 cli.py generate-tests \
  --old specs/spec_v1.json \
  --new specs/spec_v2.json \
  --output tests/my_first_test.py

# Review generated tests
cat tests/my_first_test.py

# Run tests (after manual review/fixes)
python3 -m pytest tests/test_contract_generated.py -v
```

## Common Commands

```bash
# See all CLI options
python3 cli.py --help

# Get help for specific command
python3 cli.py compare --help
python3 cli.py generate-tests --help

# Run all existing tests
python3 -m pytest tests/ -v

# Check Ollama status
curl http://localhost:11434/api/tags
```

## What's Next?

- **Read full docs**: [README.md](README.md)
- **Setup details**: [SETUP.md](SETUP.md)
- **Usage examples**: [USAGE.md](USAGE.md)
- **Understand prompts**: [PROMPTS.md](PROMPTS.md)
- **See test results**: [TESTING.md](TESTING.md)

## Troubleshooting

**Can't connect to Ollama?**
```bash
# Check if it's running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve
```

**Tests fail?**
```bash
# Use the working baseline tests
python3 -m pytest tests/test_contract_generated.py -v
```

**Need help?**
```bash
# Check CLI help
python3 cli.py --help
```

## Project Structure

```
contract_ai/
├── cli.py                      # Main CLI entry point
├── ai_client_ollama.py         # LLM integration
├── diff_engine.py              # Spec comparison
├── specs/                      # API specifications
│   ├── spec_v1.json           # Original
│   └── spec_v2.json           # Updated
├── tests/                      # Generated tests
│   └── test_contract_generated.py
└── prompts/                    # LLM prompts
    └── test_generation_v3.md
```

## Key Files

- `README.md` - Project overview & documentation index
- `SETUP.md` - Detailed installation guide
- `USAGE.md` - Command reference & workflows
- `PROMPTS.md` - Prompt engineering documentation
- `TESTING.md` - Test results & analysis

---

**You're ready! Start by running the compare command above.** 🚀
