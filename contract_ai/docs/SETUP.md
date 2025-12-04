# Setup Guide

Complete installation and setup instructions for the AI Contract Testing Platform.

## System Requirements

- **Operating System**: macOS, Linux, or Windows (WSL2)
- **Python**: 3.11 or higher
- **RAM**: 8GB minimum (16GB recommended for Ollama)
- **Disk Space**: ~5GB for Ollama + llama3 model

## Step 1: Install Python Dependencies

```bash
# Install pytest and requests
pip3 install pytest requests --user

# Verify installation
python3 -c "import pytest, requests; print('✓ Dependencies installed')"
```

### Alternative: Using a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install pytest requests

# Verify
python -c "import pytest, requests; print('✓ Dependencies installed')"
```

## Step 2: Install Ollama

### macOS

```bash
# Download and install from official site
curl -fsSL https://ollama.com/install.sh | sh

# OR use Homebrew
brew install ollama
```

### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows

Download installer from: https://ollama.com/download/windows

## Step 3: Start Ollama Service

```bash
# Start Ollama server (in a separate terminal)
ollama serve
```

The server should start on `http://localhost:11434`

### Verify Ollama is Running

```bash
# Check service status
curl http://localhost:11434/api/tags

# Expected output: JSON list of models (may be empty initially)
```

## Step 4: Pull the llama3 Model

```bash
# Download llama3 model (~4.7GB)
ollama pull llama3

# Verify model is available
ollama list
```

**Expected output:**
```
NAME            ID              SIZE      MODIFIED
llama3:latest   365c0bd3c000    4.7 GB    X minutes ago
```

## Step 5: Clone and Navigate to Project

```bash
# If you haven't already
cd /path/to/AIContractTesting/contract_ai

# Verify structure
ls -la
```

**Expected files:**
```
ai_client_ollama.py
cli.py
diff_engine.py
README.md
specs/
tests/
prompts/
```

## Step 6: Verify Installation

### Test 1: Python modules import correctly

```bash
python3 -c "
import ai_client_ollama
import diff_engine
import cli
print('✓ All modules import successfully')
"
```

### Test 2: Ollama API is accessible

```bash
curl -s http://localhost:11434/api/tags | grep -q llama3 && echo "✓ Ollama + llama3 ready" || echo "✗ Model not found"
```

### Test 3: Compare command works

```bash
python3 cli.py compare --old specs/spec_v1.json --new specs/spec_v2.json
```

**Expected output:**
```
Differences detected:
- Endpoint added: /health ['GET']
- Endpoint /order GET: field 'currency' added (type: string)
- Endpoint /widget GET: field 'reviewUrl' added (type: string)
- Endpoint /widget GET: field 'amount' type changed from number to string
```

### Test 4: Generate tests (full integration test)

```bash
python3 cli.py generate-tests \
  --old specs/spec_v1.json \
  --new specs/spec_v2.json \
  --output tests/test_verify_setup.py
```

**Expected output:**
```
Changes detected between specs:
...

Calling local LLM via Ollama to generate pytest contract tests...

Generated tests written to: tests/test_verify_setup.py
```

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'pytest'`

**Solution:**
```bash
pip3 install pytest --user
# OR if using venv:
pip install pytest
```

### Issue: `Failed to reach Ollama at http://localhost:11434`

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve

# In a new terminal, verify:
curl http://localhost:11434/api/tags
```

### Issue: `Ollama returned HTTP 404: model 'llama3' not found`

**Solution:**
```bash
# Pull the model
ollama pull llama3

# Verify
ollama list | grep llama3
```

### Issue: Tests take too long to generate (>2 minutes)

**Possible causes:**
- Limited system resources
- Large model inference time
- Network issues (if Ollama is downloading model data)

**Solutions:**
1. Increase timeout in `ai_client_ollama.py` (default: 60 seconds):
   ```python
   def call_ollama(
       messages: List[Dict[str, str]],
       model: str = MODEL_NAME,
       timeout_seconds: int = 120,  # Increase this
   )
   ```

2. Use a smaller/faster model:
   ```bash
   ollama pull llama3:8b-instruct-q4_0
   ```

   Update `MODEL_NAME` in `ai_client_ollama.py`:
   ```python
   MODEL_NAME = "llama3:8b-instruct-q4_0"
   ```

### Issue: Generated tests have syntax errors

**This is expected behavior.** LLM output can be non-deterministic.

**Solutions:**
1. Review and manually fix generated tests
2. Use the manually-fixed reference: `tests/test_contract_generated.py`
3. Iterate on prompt (see `prompts/test_generation_v3.md`)

## Configuration Options

### Change Ollama URL

Edit `ai_client_ollama.py`:
```python
OLLAMA_URL = "http://your-ollama-host:11434/api/chat"
```

### Change Model

Edit `ai_client_ollama.py`:
```python
MODEL_NAME = "codellama"  # or any other Ollama model
```

### Adjust Timeout

Edit `ai_client_ollama.py`:
```python
def call_ollama(
    messages: List[Dict[str, str]],
    model: str = MODEL_NAME,
    timeout_seconds: int = 180,  # 3 minutes
)
```

## Next Steps

Once setup is complete:

1. Read [USAGE.md](USAGE.md) for detailed command examples
2. Review [PROMPTS.md](PROMPTS.md) to understand prompt versioning
3. See [TESTING.md](TESTING.md) for test results and analysis
4. Try modifying `specs/spec_v2.json` to experiment with different changes

## Uninstall

```bash
# Remove Python packages
pip3 uninstall pytest requests

# Remove Ollama (macOS)
brew uninstall ollama
# OR manually delete: rm -rf /usr/local/bin/ollama

# Remove project
rm -rf /path/to/AIContractTesting
```

## Getting Help

- Check [README.md](README.md) for project overview
- Review CLI help: `python3 cli.py --help`
- Examine working test file: `tests/test_contract_generated.py`
- Review prompt documentation: `prompts/test_generation_v3.md`
