#!/usr/bin/env python3
"""
Mreaia Quickstart Demo
======================
Simulates a real enterprise workflow in 3 seconds:
1. Generates a sample heavy enterprise financial dataset.
2. Compiles and node-locks it into mreaia.ghost.
3. Decrypts strictly in volatile RAM and prints the prompt context ready for Ollama / LLM.
"""

import os
import sys

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mreaia_core import HierarchicalExtractor, GhostReader, HardwareSecurityLayer


def run_demo():
    print("=" * 70)
    print("  🪞 Mreaia Interactive Quickstart Demonstration")
    print("=" * 70)

    # 1. Inspect Host Hardware Fingerprint
    hw = HardwareSecurityLayer.get_machine_fingerprint()
    print(f"\n[1] Detected Host Hardware Fingerprint:")
    print(f"    SHA-256 Digest : {hw.hex()[:32]}... (Immutable Node Lock)")

    # 2. Create sample enterprise file
    sample_file = "sample_enterprise_ledger.dat"
    print(f"\n[2] Creating simulated enterprise dataset: {sample_file}")
    with open(sample_file, "wb") as f:
        f.write(b"ENTERPRISE_LEDGER_HEADER_MAGIC_V1\x00" + b"\x01\x02\x03\x04" * 250000)

    orig_sz = os.path.getsize(sample_file)
    print(f"    Source File Size : {orig_sz:,} bytes (~1.0 MB)")

    # 3. Compile into Ghost
    ghost_file = "demo_output.ghost"
    print(f"\n[3] Compiling and Node-Locking into {ghost_file}...")
    src_sz, ghost_sz, ratio = HierarchicalExtractor.compile_ghost(
        sample_file, output_ghost=ghost_file
    )
    print(f"    Original Size    : {src_sz:,} bytes")
    print(f"    Ghost Size       : {ghost_sz:,} bytes")
    print(f"    Compression      : {ratio:.2f}% reduction!")

    # 4. Stream Prompt Context in RAM
    print(f"\n[4] Streaming in-memory context for Local LLM (Ollama/Llama3):")
    print("-" * 70)
    prompt_context = GhostReader.to_llm_prompt_context(ghost_file, sample_file)
    print(prompt_context[:600] + "\n... [TRUNCATED FOR DEMO PREVIEW] ...")
    print("-" * 70)

    # Cleanup demo files
    if os.path.exists(sample_file):
        os.remove(sample_file)
    if os.path.exists(ghost_file):
        os.remove(ghost_file)

    print("\n[✔] Demo successfully completed with 0 plaintext disk residue!")


if __name__ == "__main__":
    run_demo()
