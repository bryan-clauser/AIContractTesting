# Demo Guide

**AI Contract Testing & Backward Compatibility Platform**

Complete guide for presenting and demonstrating this hackathon project.

---

## 🎯 Demo Overview

**Duration:** 5-10 minutes
**Audience:** Technical judges, developers, hackathon attendees
**Goal:** Show AI-assisted contract test generation solving real API backward compatibility problems

---

## 🎬 Demo Script

### Opening (30 seconds)

**Say:**
> "We built an AI-powered tool that automatically detects breaking changes between API versions and generates contract tests to catch backward compatibility issues. It runs entirely locally using Ollama, no external APIs needed."

**Show:** Project structure on screen
```bash
ls -la contract_ai/
```

---

### Part 1: The Problem (1 minute)

**Say:**
> "When APIs evolve, backward compatibility breaks happen. Let's look at two versions of an API spec."

**Show spec_v1.json:**
```bash
cat specs/spec_v1.json
```

**Highlight:**
- `/widget` endpoint with `amount` as **number**
- `/order` endpoint with 2 fields

**Show spec_v2.json:**
```bash
cat specs/spec_v2.json
```

**Point out changes:**
- ⚠️ `amount` changed from **number** to **string** (BREAKING!)
- ✅ Added `currency` field
- ✅ Added new `/health` endpoint

**Say:**
> "That type change from number to string? That's a breaking change that will crash old clients. Let's see how our tool detects this."

---

### Part 2: Automated Diff Detection (1 minute)

**Say:**
> "Our diff engine automatically detects all changes between specs."

**Run:**
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

**Say:**
> "See that last line? It caught the breaking type change. Now let's use AI to generate tests for these changes."

---

### Part 3: AI Test Generation (2 minutes)

**Say:**
> "We use a local LLM via Ollama to generate pytest contract tests. Watch this..."

**Run:**
```bash
python3 cli.py generate-tests \
  --old specs/spec_v1.json \
  --new specs/spec_v2.json \
  --output tests/demo_generated.py
```

**Expected output:**
```
Changes detected between specs:
- Endpoint added: /health ['GET']
- Endpoint /order GET: field 'currency' added (type: string)
- Endpoint /widget GET: field 'reviewUrl' added (type: string)
- Endpoint /widget GET: field 'amount' type changed from number to string

Calling local LLM via Ollama to generate pytest contract tests...

Generated tests written to: tests/demo_generated.py
```

**Say:**
> "It took about 15 seconds. Let's look at what it generated."

**Show generated file:**
```bash
head -50 tests/test_contract_generated.py
```

**Highlight key parts:**
1. **Imports** - Only stdlib + pytest (no external deps)
2. **Docstrings** - Clear test intent
3. **Type validation** - Uses `isinstance()`
4. **Breaking change test** - Shows what old clients expected

**Say:**
> "Notice the test for the type change - it validates the new string type AND includes a comment showing what would break for old clients."

---

### Part 4: Running the Tests (1 minute)

**Say:**
> "These are real, runnable pytest tests. Let's run them."

**Run:**
```bash
python3 -m pytest tests/test_contract_generated.py -v
```

**Expected output:**
```
============================= test session starts ==============================
tests/test_contract_generated.py::test_widget_get_response_schema PASSED [ 20%]
tests/test_contract_generated.py::test_widget_amount_type_change PASSED  [ 40%]
tests/test_contract_generated.py::test_order_get_response_schema PASSED  [ 60%]
tests/test_contract_generated.py::test_order_currency_field_added PASSED [ 80%]
tests/test_contract_generated.py::test_health_get_response_schema PASSED [100%]

============================== 5 passed in 0.01s ===============================
```

**Say:**
> "All tests passing! We now have automated contract tests that validate the new API behavior and catch potential backward compatibility issues."

---

### Part 5: The Technology (1 minute)

**Show architecture:**

**Say:**
> "Here's how it works:"

**Point to:**
1. **diff_engine.py** - "Pure Python, compares JSON specs deterministically"
2. **ai_client_ollama.py** - "Connects to local Ollama running llama3"
3. **Prompts** - "We versioned our prompts - currently on v3 after iterating"

**Show prompt evolution:**
```bash
ls -la prompts/
```

**Say:**
> "We learned that prompt engineering is hard. It took 3 iterations to get good results. All documented in PROMPTS.md"

---

### Part 6: Key Learnings (1 minute)

**Say:**
> "What we learned building this:"

**Show TESTING.md metrics (open in editor):**
- ✅ Diff engine: 100% accuracy
- ✅ No external dependencies
- ✅ Prompt v3: 70% of tests usable without fixes
- ⚠️ LLM output still needs human review

**Say:**
> "The diff detection is perfect. The AI-generated tests are good but not perfect - about 70% are usable as-is. We see this as an AI-assisted workflow, not fully automated."

---

### Closing (30 seconds)

**Say:**
> "This solves a real problem: catching breaking API changes early. It's production-ready for the diff detection, and very useful for AI-assisted test generation. All running locally, no external APIs."

**Show documentation:**
```bash
ls -la *.md
```

**Say:**
> "And it's fully documented - 8 comprehensive guides covering setup, usage, prompt engineering, and test results."

---

## 🎤 Key Talking Points

### Strengths to Emphasize

1. **Solves Real Problem**
   - Breaking API changes are common
   - Manual test writing is time-consuming
   - Backward compatibility issues are expensive

2. **Technical Excellence**
   - 100% accurate diff detection
   - Local-first (Ollama, no cloud APIs)
   - Versioned prompts (engineering discipline)
   - Comprehensive documentation

3. **Practical Value**
   - Real, runnable pytest tests
   - Works with existing tools
   - CI/CD integration ready
   - No external dependencies

4. **Honest Assessment**
   - We document limitations
   - 70% success rate is transparent
   - We say "AI-assisted" not "fully automated"

### Questions You Might Get

**Q: Why not use GPT-4 or Claude?**
> "We wanted everything local - no API keys, no external dependencies, no rate limits. Ollama lets us run this entirely offline."

**Q: What about the 30% that need fixes?**
> "That's the reality of LLM output quality. We documented all failure modes in TESTING.md and see this as AI-assisted, not fully automated. The tool still saves significant time."

**Q: Can it handle OpenAPI specs?**
> "Not yet - we built a simplified JSON format for the hackathon POC. OpenAPI support is on the roadmap. The diff engine is modular and could be extended."

**Q: How do you version prompts?**
> "Every prompt iteration is saved as a versioned markdown file in /prompts/. We track what changed, why, and the impact on output quality. This makes prompt engineering reproducible."

**Q: What's the performance?**
> "Diff detection is instant (<1ms). Test generation takes 10-20 seconds depending on the model. The bottleneck is LLM inference, not our code."

---

## 🖥️ Demo Setup Checklist

### Before the Demo

- [ ] Ollama is running (`ollama serve` in background)
- [ ] llama3 model is pulled (`ollama list`)
- [ ] Terminal font size increased (for visibility)
- [ ] Terminal window is clean (clear history)
- [ ] Project directory open (`cd contract_ai`)
- [ ] Browser tab ready with one of the docs (optional)
- [ ] Backup: Have screenshots ready in case of issues

### Terminal Setup

```bash
# Start fresh
cd /path/to/AIContractTesting/contract_ai
clear

# Verify Ollama
curl -s http://localhost:11434/api/tags | grep llama3

# Test imports
python3 -c "import ai_client_ollama, diff_engine, cli; print('✓ Ready')"

# Remove old demo output if exists
rm -f tests/demo_generated.py
```

### Font Size
```bash
# Make terminal readable from distance
# Recommended: 18-20pt font
# Use Command + Plus to increase
```

---

## 🎯 Different Audience Variations

### For Technical Judges (10 minutes)

**Add:**
- Show actual code: `cat diff_engine.py | head -50`
- Explain set-based diffing algorithm
- Show prompt engineering iteration (v1 vs v3)
- Discuss test quality metrics from TESTING.md
- Talk about production readiness

### For Business Audience (5 minutes)

**Focus on:**
- The problem (API breaking changes cost money)
- The solution (automated detection + test generation)
- Time savings (manual test writing vs automated)
- Skip technical details
- Show only the CLI, not the code

### For AI/ML Audience (8 minutes)

**Emphasize:**
- Prompt engineering challenges (show PROMPTS.md)
- v1→v2→v3 evolution with metrics
- LLM output quality analysis
- Evaluation criteria
- Why local LLM vs cloud
- Future: Few-shot examples, chain-of-thought

---

## 🎬 Alternative Demo Flow (Quick Version)

If you have **<5 minutes:**

1. **Show the problem** (30s)
   - "APIs change, backward compatibility breaks"

2. **Run compare** (30s)
   ```bash
   python3 cli.py compare --old specs/spec_v1.json --new specs/spec_v2.json
   ```

3. **Show pre-generated tests** (1 min)
   ```bash
   cat tests/test_contract_generated.py
   ```

4. **Run tests** (30s)
   ```bash
   python3 -m pytest tests/test_contract_generated.py -v
   ```

5. **Show docs** (30s)
   ```bash
   ls -la *.md
   ```
   "Fully documented, versioned prompts, test metrics"

6. **Wrap up** (1 min)
   - "Solves real problem, local LLM, production-ready diff, AI-assisted test gen"

---

## 💡 Pro Tips

### Make It Visual

1. **Split terminal** - Show code on left, output on right
2. **Color output** - pytest's colors help show passing tests
3. **Use cat with syntax highlighting** if available
4. **Keep terminal clean** - Clear between major steps

### Handle Issues

**If Ollama is slow:**
> "LLM inference takes time - this is expected. The diff detection was instant though."

**If generation fails:**
> "We have pre-generated tests here - let me show those instead."
```bash
cat tests/test_contract_generated.py
```

**If tests fail:**
> "This demonstrates why we say AI-assisted, not fully automated. Let me show our baseline tests."
```bash
python3 -m pytest tests/test_contract_generated.py -v
```

### Practice Runs

Do 3 practice runs before the real demo:
1. **Full run** - All commands, all explanations
2. **Quick run** - Time-limited version
3. **Recovery run** - Practice handling failures

---

## 📸 Screenshot Backup Plan

If live demo fails, have screenshots of:

1. ✅ Diff output showing 4 changes detected
2. ✅ Generated test code (formatted nicely)
3. ✅ Pytest output showing 5/5 tests passing
4. ✅ Documentation directory listing
5. ✅ TESTING.md metrics page

**Say if needed:**
> "Let me show you screenshots of a successful run..."

---

## 🎓 Post-Demo Resources

**If someone wants to try it:**
> "Clone the repo and run `python3 cli.py --help` to get started. QUICKSTART.md has 5-minute setup instructions."

**If someone wants to understand it:**
> "Read PROJECT_SUMMARY.md - it's a complete documentation index with reading paths for different audiences."

**If someone wants to improve it:**
> "Check PROMPTS.md for prompt engineering insights and TESTING.md for quality metrics. PRs welcome!"

---

## ✅ Final Checklist

**Before presenting:**
- [ ] Ollama running and tested
- [ ] All commands tested in sequence
- [ ] Terminal font size readable
- [ ] Backup screenshots ready
- [ ] Timing practiced (<10 minutes)
- [ ] Questions rehearsed

**During demo:**
- [ ] Speak clearly and not too fast
- [ ] Show, don't just tell
- [ ] Highlight breaking change problem
- [ ] Emphasize local/no external deps
- [ ] Show real passing tests
- [ ] Be honest about limitations

**After demo:**
- [ ] Mention documentation
- [ ] Offer to answer questions
- [ ] Share repo link if allowed

---

## 🚀 You're Ready!

This demo shows:
✅ Real problem solved
✅ Working code
✅ AI integration done right
✅ Honest about limitations
✅ Production considerations
✅ Comprehensive documentation

**Break a leg!** 🎉

---

*Pro tip: The judges will appreciate that you document BOTH what works perfectly (diff detection) AND what needs improvement (LLM output consistency). Honesty about limitations shows maturity.*
