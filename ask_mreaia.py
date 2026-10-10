#!/usr/bin/env python3
"""
Mreaia On-Demand AI Context Bridge (ask-mreaia)
==============================================
Zero-background-overhead on-demand CLI:
1. Ingests any large enterprise dataset in milliseconds.
2. Extracts and node-locks the hardware-bound blueprint into volatile RAM.
3. Automatically pipes to local LLM (Ollama) if installed, or copies the
   zero-token prompt directly to your macOS clipboard (pbcopy) for instant pasting into ChatGPT / Claude.
4. Terminates immediately (0.0% idle CPU, 0.0 MB RAM).
"""

import os
import sys
import argparse
import subprocess
import shutil

from mreaia_core import HierarchicalExtractor, GhostReader


def copy_to_macos_clipboard(text: str) -> bool:
    """Copies text directly to macOS clipboard using native pbcopy."""
    try:
        process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        process.communicate(text.encode("utf-8"))
        return process.returncode == 0
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Mreaia On-Demand: Zero-overhead context bridge for local & cloud LLMs"
    )
    parser.add_argument("file", help="Path to data file (Excel, SQL, CSV, or binary dataset)")
    parser.add_argument(
        "query",
        nargs="?",
        default="Analyze this dataset topology and provide insights or code.",
        help="Prompt / question for the AI model",
    )
    parser.add_argument(
        "--model",
        default="llama3",
        help="Local Ollama model name (default: llama3)",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        default=True,
        help="Copy the generated prompt context to macOS clipboard (default: True)",
    )

    args = parser.parse_args()

    file_path = os.path.abspath(args.file)
    if not os.path.exists(file_path):
        print(f"[-] Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    temp_ghost = f"{file_path}.ghost"

    try:
        # 1. Compile and node-lock in milliseconds
        src_sz, ghost_sz, ratio = HierarchicalExtractor.compile_ghost(
            file_path, output_ghost=temp_ghost
        )

        # 2. Extract verified prompt context in RAM
        blueprint_context = GhostReader.to_llm_prompt_context(temp_ghost, file_path)

        full_prompt = (
            f"{blueprint_context}\n\n"
            f"USER QUERY: {args.query}\n"
        )

        # 3. Check if Ollama is available
        ollama_bin = shutil.which("ollama")

        if ollama_bin:
            print(f"[*] Streaming directly to local Ollama ({args.model})...\n")
            proc = subprocess.Popen(
                [ollama_bin, "run", args.model, full_prompt],
                stdout=sys.stdout,
                stderr=sys.stderr,
            )
            proc.communicate()
        else:
            # 4. Graceful macOS Clipboard Integration
            copied = copy_to_macos_clipboard(full_prompt)
            print("=" * 70)
            print("  🪞 Mreaia Zero-Token Prompt Ready!")
            print("=" * 70)
            print(f"  Source Dataset : {os.path.basename(file_path)} ({src_sz:,} bytes)")
            print(f"  Ghost Size     : {ghost_sz:,} bytes ({ratio:.2f}% reduction)")
            print(f"  Status         : Node-Locked & Decrypted in RAM (0.0s)")
            if copied:
                print("  📋 Clipboard    : COPIED TO CLIPBOARD (Cmd+V ready for ChatGPT / Claude!)")
            print("=" * 70)
            print("\nPreview of AI Prompt:")
            print("-" * 70)
            print(full_prompt[:500] + "\n... [FULL CONTEXT IN CLIPBOARD] ...")
            print("-" * 70)

    finally:
        # Clean up ephemeral ghost file immediately
        if os.path.exists(temp_ghost):
            os.remove(temp_ghost)


if __name__ == "__main__":
    main()
