# ai_client_ollama.py
"""
Simple client for calling a local Ollama model via /api/chat.

- Exposes call_ollama() for flexible use.
- Exposes generate_test_code_from_diff() for our contract-testing POC.

Assumptions:
- Ollama is running on localhost:11434
- Model "llama3" is available (adjust MODEL_NAME if needed)
"""

from __future__ import annotations

from typing import List, Dict, Any
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3"  # change here if you prefer a different model


class OllamaError(RuntimeError):
    """Raised when the Ollama API call fails."""


def call_ollama(
    messages: List[Dict[str, str]],
    model: str = MODEL_NAME,
    timeout_seconds: int = 60,
) -> str:
    """
    Call the local Ollama /api/chat endpoint with a list of messages.

    messages = [
        {"role": "system" | "user" | "assistant", "content": "..."},
        ...
    ]

    Returns the assistant's full content string.
    """
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,  # easier to consume for our use case
    }

    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=timeout_seconds)
    except requests.RequestException as exc:
        raise OllamaError(f"Failed to reach Ollama at {OLLAMA_URL}: {exc}") from exc

    if resp.status_code != 200:
        raise OllamaError(
            f"Ollama returned HTTP {resp.status_code}: {resp.text[:500]}"
        )

    try:
        data = resp.json()
    except ValueError as exc:
        raise OllamaError(f"Invalid JSON from Ollama: {resp.text[:500]}") from exc

    message = data.get("message") or {}
    content = message.get("content")
    if not isinstance(content, str):
        raise OllamaError(f"Ollama response missing 'message.content': {data}")

    return content


def generate_test_code_from_diff(diff_summary: str, spec_snippet: str) -> str:
    """
    High-level helper: given a human-readable diff summary and a JSON spec snippet,
    ask the local model to generate pytest tests as pure Python code.

    The result is intended to be written directly to a .py file under tests/.
    """
    system_msg = {
        "role": "system",
        "content": (
            "You are an assistant that writes concise, deterministic pytest tests "
            "for validating JSON response payloads against a simple API spec.\n"
            "- Use only Python standard library and pytest.\n"
            "- Do not include explanations or comments, only Python code.\n"
            "- Assume tests will run against in-memory sample payloads, "
            "not real HTTP calls."
        ),
    }

    user_msg = {
        "role": "user",
        "content": (
            "Here is the current API spec (simplified JSON):\n"
            f"{spec_snippet}\n\n"
            "Here are the changes detected between the previous spec and this spec:\n"
            f"{diff_summary}\n\n"
            "Generate a pytest test module that:\n"
            "- Defines sample response payloads for the affected endpoints.\n"
            "- Asserts that required fields exist with the expected simple types "
            "(string, number, boolean).\n"
            "- Includes at least one test that would fail if a removed field is "
            "still expected by a client.\n"
            "- Includes at least one test that checks behavior for any added fields.\n"
            "Return ONLY valid Python code for a pytest test module.\n"
        ),
    }

    return call_ollama([system_msg, user_msg])
