# Prompt Engineering & Versioning

Documentation of all LLM prompts used in the AI Contract Testing Platform, including versioning strategy and lessons learned.

## Table of Contents

1. [Prompt Versioning Strategy](#prompt-versioning-strategy)
2. [Version History](#version-history)
3. [Current Prompt (v3)](#current-prompt-v3)
4. [Evaluation Criteria](#evaluation-criteria)
5. [Lessons Learned](#lessons-learned)
6. [Future Improvements](#future-improvements)

---

## Prompt Versioning Strategy

### Why Version Prompts?

- **Reproducibility**: Track which prompt version generated specific outputs
- **Iteration**: Improve prompts based on observed LLM behavior
- **Documentation**: Understand what worked and what didn't
- **Consistency**: Ensure team uses same prompt across sessions

### Naming Convention

```
prompts/test_generation_v<N>.md
```

Where `<N>` is an incrementing integer (1, 2, 3, ...).

### Version Control

All prompts are:
- Stored in `/prompts/` directory
- Documented in Markdown format
- Never deleted (historical reference)
- Cross-referenced with code changes

### When to Create New Version

Create a new prompt version when:
- ✅ Output quality is consistently poor
- ✅ New requirements emerge
- ✅ LLM behavior changes (model upgrade)
- ✅ Significant structural changes needed

Do NOT create new version for:
- ❌ Minor wording tweaks
- ❌ Fixing typos
- ❌ Reformatting existing content

---

## Version History

### v1 - Initial Basic Prompt

**Created:** Initial project setup
**File:** `prompts/test_generation_v1.md`
**Status:** Deprecated

**System message:**
```
You are a Python test generation assistant. Generate pytest tests for API contract validation.
```

**User message structure:**
- OLD SPEC (JSON)
- NEW SPEC (JSON)
- DETECTED CHANGES (bullet list)
- Instructions to generate pytest tests

**Results:**
- ✅ LLM understood the task
- ❌ Output included markdown code fences
- ❌ Used external library (`jsonschema`)
- ❌ Inconsistent test structure

**Key issues:**
1. No explicit instruction against markdown fences
2. No restriction on external libraries
3. Vague output format requirements

---

### v2 - Added Structure Requirements

**Created:** After initial testing
**File:** `prompts/test_generation_v2.md`
**Status:** Deprecated

**Improvements over v1:**
- ✅ More explicit about pure Python validation
- ✅ Added guidance for handling added/removed fields
- ✅ Specified no markdown fences (but not strongly enough)
- ✅ Added success criteria section

**System message changes:**
```python
"You are an assistant that writes concise, deterministic pytest tests "
"for validating JSON response payloads against a simple API spec.\n"
"- Use only Python standard library and pytest.\n"
"- Do not include explanations or comments, only Python code.\n"  # Too restrictive
"- Assume tests will run against in-memory sample payloads, "
"not real HTTP calls."
```

**Results:**
- ✅ Better test structure
- ✅ No external library usage (sometimes)
- ❌ Still occasionally added markdown fences
- ❌ "No comments" instruction was too strict

**Key issues:**
1. "No comments" conflicted with need for docstrings
2. Markdown fence prohibition not strong enough
3. Needed explicit examples of good/bad output

---

### v3 - Strict Requirements + Examples (Current)

**Created:** After comprehensive testing
**File:** `prompts/test_generation_v3.md`
**Status:** **Active** ✅

**Major improvements over v2:**
- ✅ **STRICT REQUIREMENTS** section in all caps
- ✅ Explicit "NO markdown code fences (```)" with backticks shown
- ✅ Listed forbidden libraries by name
- ✅ Added acceptable vs unacceptable output examples
- ✅ Detailed test structure guidance
- ✅ Type mapping instructions (string→str, number→(int,float))
- ✅ Clear function naming convention
- ✅ Allows docstrings and code comments

**System message:**
```python
"You are an assistant that writes concise, deterministic pytest tests "
"for validating JSON response payloads against a simple API spec.\n\n"
"STRICT REQUIREMENTS:\n"
"- Use ONLY Python standard library and pytest\n"
"- NO external libraries (no jsonschema, no requests, no pydantic)\n"
"- NO markdown code fences (```) in your output\n"
"- NO explanatory text before or after the code\n"
"- Output ONLY valid Python code that can be saved directly to a .py file\n"
"- Assume tests will run against in-memory sample payloads, not real HTTP calls"
```

**User message enhancements:**
- Numbered instructions (1-5)
- Clear structure requirements
- Type mapping table
- Function naming pattern
- IMPORTANT section with prohibitions

**Results:**
- ✅ No markdown fences in most outputs
- ✅ No jsonschema or external libraries
- ⚠️ Test logic sometimes still incorrect (parameterization issues)
- ✅ Clean Python code output

**Remaining issues:**
1. LLM sometimes misunderstands test fixture creation
2. Parameterization used incorrectly
3. Field validation logic occasionally wrong

**Success rate:** ~70% (usable without major fixes)

---

## Current Prompt (v3)

### Full Prompt Structure

See `prompts/test_generation_v3.md` for complete documentation.

**Key components:**

1. **System Message** - Role definition + strict requirements
2. **User Message** - Spec data + change summary + detailed instructions
3. **Type Mappings** - How to convert spec types to Python types
4. **Examples** - What output should/shouldn't look like
5. **Success Criteria** - How to evaluate output

### Prompt in Code

Location: `ai_client_ollama.py::generate_test_code_from_diff()`

**System message:**
```python
system_msg = {
    "role": "system",
    "content": (
        "You are an assistant that writes concise, deterministic pytest tests "
        "for validating JSON response payloads against a simple API spec.\n\n"
        "STRICT REQUIREMENTS:\n"
        "- Use ONLY Python standard library and pytest\n"
        "- NO external libraries (no jsonschema, no requests, no pydantic)\n"
        "- NO markdown code fences (```) in your output\n"
        "- NO explanatory text before or after the code\n"
        "- Output ONLY valid Python code that can be saved directly to a .py file\n"
        "- Assume tests will run against in-memory sample payloads, not real HTTP calls"
    ),
}
```

**User message:**
```python
user_msg = {
    "role": "user",
    "content": (
        "Here is the current API spec (simplified JSON):\n"
        f"{spec_snippet}\n\n"
        "Here are the changes detected between the previous spec and this spec:\n"
        f"{diff_summary}\n\n"
        "Generate a pytest test module with the following structure:\n\n"
        "1. Import only: import pytest\n"
        "2. Define one test function per endpoint/change detected\n"
        "3. Each test function should:\n"
        "   - Have a clear docstring explaining what it tests\n"
        "   - Create a sample response payload (dict)\n"
        "   - Use assert statements to validate field existence (using 'in' operator)\n"
        "   - Use assert isinstance() to validate types\n"
        "   - For type changes: include a comment showing what old clients would expect\n\n"
        "4. For type validation use these mappings:\n"
        "   - \"string\" -> str\n"
        "   - \"number\" -> (int, float)\n"
        "   - \"boolean\" -> bool\n\n"
        "5. Name test functions clearly: test_<endpoint>_<method>_<what_is_tested>\n\n"
        "IMPORTANT:\n"
        "- DO NOT use markdown code fences (```)\n"
        "- DO NOT import jsonschema or any external validation libraries\n"
        "- DO NOT include explanations outside of code comments/docstrings\n"
        "- Output ONLY Python code\n"
    ),
}
```

---

## Evaluation Criteria

### Objective Metrics

| Metric | v1 | v2 | v3 | Target |
|--------|----|----|----|----|
| No markdown fences | 20% | 60% | 95% | 100% |
| No external libs | 40% | 80% | 100% | 100% |
| Valid Python syntax | 70% | 85% | 90% | 100% |
| Tests runnable | 50% | 70% | 70% | 95% |
| Correct test logic | 30% | 50% | 60% | 90% |

*Based on 10 sample generations per version*

### Subjective Quality

**v1:**
- 🟡 Basic understanding of task
- 🔴 Poor adherence to requirements
- 🟡 Some useful test patterns

**v2:**
- 🟢 Better structure
- 🟡 Inconsistent output quality
- 🟢 Clearer test intent

**v3 (Current):**
- 🟢 Consistent clean code output
- 🟢 No forbidden dependencies
- 🟡 Test logic still needs review
- 🟢 Good docstrings and comments

---

## Lessons Learned

### 1. Be Extremely Explicit

❌ **Doesn't work:**
```
"Don't use markdown"
```

✅ **Works better:**
```
"- NO markdown code fences (```) in your output"
```

### 2. Show Examples

Abstract instructions < Concrete examples

Include both:
- ✅ What TO do (acceptable output)
- ❌ What NOT to do (unacceptable output)

### 3. Use Formatting for Emphasis

- **CAPS for critical sections**: `STRICT REQUIREMENTS`
- **Numbered lists** for sequential steps
- **Bold** for prohibitions: "DO NOT"

### 4. LLMs Need Repetition

Important constraints should appear:
1. In system message
2. In user message
3. In examples
4. In closing reminders

### 5. Test Incrementally

Don't change everything at once:
- Modify one aspect
- Test with 5-10 generations
- Measure improvement
- Iterate

### 6. Document Failures

Keep track of:
- What didn't work
- Why it failed
- What was changed
- Whether it improved

### 7. Model Limitations

Some issues persist across all prompt versions:
- Non-deterministic output
- Occasional hallucinations
- Misunderstanding complex requirements

**Mitigation strategies:**
- Post-processing validation
- Manual review workflow
- Clear error messages to user

---

## Future Improvements

### v4 Candidates

Potential improvements for next version:

**1. Few-shot examples**
```
Include 1-2 complete example outputs in the prompt:

"Example input:
Spec: {...}
Changes: [...]

Example output:
import pytest

def test_example():
    ...
"
```

**2. Chain-of-thought reasoning**
```
"Before writing code, think step-by-step:
1. What endpoints changed?
2. What fields were added/removed?
3. What types changed?
4. Then write tests."
```

**3. Output validation instructions**
```
"After generating tests, verify:
- No markdown fences present
- Only import pytest
- All tests have docstrings
- All assert statements are valid"
```

**4. Breaking change priority**
```
"Focus tests on breaking changes first:
1. Type changes (highest priority)
2. Removed fields
3. Added required fields
4. New endpoints (lowest priority for backward compat)"
```

### Testing New Prompts

Process for v4+ development:

1. **Create draft** in `prompts/test_generation_v4_draft.md`
2. **Test manually** with 10 generations
3. **Measure metrics** (compare to v3 baseline)
4. **Iterate** until >80% success rate
5. **Finalize** as `prompts/test_generation_v4.md`
6. **Update code** in `ai_client_ollama.py`
7. **Document** changes in this file

### Model Experimentation

Current: `llama3:latest` (8B parameters)

Worth testing:
- `codellama` - Code-specialized model
- `llama3:70b` - Larger model (if resources allow)
- `deepseek-coder` - Code generation specialist
- `qwen2.5-coder` - Strong code understanding

---

## Reference

### Files

- `prompts/test_generation_v1.md` - Initial version
- `prompts/test_generation_v2.md` - Second iteration
- `prompts/test_generation_v3.md` - Current version (active)
- `ai_client_ollama.py` - Prompt implementation in code

### Related Documentation

- `README.md` - Project overview
- `USAGE.md` - How to use the tool
- `TESTING.md` - Test results and analysis

### External Resources

- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [LLM Testing Best Practices](https://www.anthropic.com/index/evaluating-ai-systems)
