# cli.py
"""
Simple CLI for the AI contract testing POC.

Commands:
- compare:
    Compare two spec JSON files and print detected changes.

- generate-tests:
    Compare two specs, summarize the changes, call the local LLM via Ollama
    to generate pytest tests, and write them to the specified output file.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Any, List

from diff_engine import load_spec, diff_specs
from ai_client_ollama import generate_test_code_from_diff, OllamaError


def json_snippet_for_model(spec: Dict[str, Any], max_chars: int = 2000) -> str:
    """
    Serialize the spec to JSON, truncated to a reasonable size for the model.
    """
    s = json.dumps(spec, indent=2)
    if len(s) > max_chars:
        return s[:max_chars] + "\n... (truncated)"
    return s


def cmd_compare(args: argparse.Namespace) -> None:
    old = load_spec(args.old)
    new = load_spec(args.new)
    changes = diff_specs(old, new)
    if not changes:
        print("No differences detected between the two specs.")
        return

    print("Differences detected:")
    for c in changes:
        print(f"- {c}")


def cmd_generate_tests(args: argparse.Namespace) -> None:
    old = load_spec(args.old)
    new = load_spec(args.new)
    changes: List[str] = diff_specs(old, new)

    if not changes:
        print("No differences detected. No tests to generate or update.")
        return

    diff_summary = "\n".join(changes)
    spec_snippet = json_snippet_for_model(new)

    print("Changes detected between specs:")
    for c in changes:
        print(f"- {c}")

    print("\nCalling local LLM via Ollama to generate pytest contract tests...")
    try:
        test_code = generate_test_code_from_diff(diff_summary, spec_snippet)
    except OllamaError as exc:
        print(f"Error calling Ollama: {exc}")
        return

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(test_code, encoding="utf-8")

    print(f"\nGenerated tests written to: {output_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AI contract testing tool using a local LLM via Ollama."
    )
    subparsers = parser.add_subparsers(dest="command")

    # compare
    p_compare = subparsers.add_parser(
        "compare", help="Compare two spec JSON files and print differences."
    )
    p_compare.add_argument("--old", required=True, help="Path to old spec (JSON).")
    p_compare.add_argument("--new", required=True, help="Path to new spec (JSON).")
    p_compare.set_defaults(func=cmd_compare)

    # generate-tests
    p_gen = subparsers.add_parser(
        "generate-tests",
        help="Generate pytest contract tests based on spec differences.",
    )
    p_gen.add_argument("--old", required=True, help="Path to old spec (JSON).")
    p_gen.add_argument("--new", required=True, help="Path to new spec (JSON).")
    p_gen.add_argument(
        "--output",
        required=True,
        help="Output path for generated pytest file, e.g. tests/test_contract_generated.py",
    )
    p_gen.set_defaults(func=cmd_generate_tests)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not getattr(args, "command", None):
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
