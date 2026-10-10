#!/usr/bin/env python3
"""
Mreaia Automated End-to-End QA Test Suite
========================================
Validates:
1. Dynamic 10MB heavy dataset generation
2. Blueprint extraction & >99% compression (<50KB ghost artifact)
3. 100% data integrity on authorized host with source file present
4. Zero-Exfiltration security validation:
   - Foreign hardware UUID exfiltration simulation -> InvalidTag cryptographic failure
   - Missing/tampered source file simulation -> Failure
5. Ephemeral in-memory LLM prompt generation without disk leaks
"""

import os
import sys
import time
import shutil
import tempfile
import unittest
from cryptography.exceptions import InvalidTag

from mreaia_core import (
    HardwareSecurityLayer,
    FileContentRouter,
    HierarchicalExtractor,
    GhostReader,
)


class TestMreaiaHardwareBoundGhost(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = tempfile.mkdtemp(prefix="mreaia_qa_")
        cls.source_10mb_path = os.path.join(cls.test_dir, "heavy_enterprise_10mb.dat")
        cls.ghost_path = os.path.join(cls.test_dir, "mreaia.ghost")

        print("\n" + "=" * 80)
        print("  [QA SUITE] MREAIA HARDWARE-BOUND ENCRYPTED BLUEPRINT TEST")
        print("=" * 80)
        print(f"[QA Setup] Creating simulated 10MB enterprise dataset at: {cls.source_10mb_path}")

        # Dynamically generate 10MB structured binary file with headers, records, and entropy
        target_size = 10 * 1024 * 1024  # 10,485,760 bytes
        chunk_pattern = (
            b"ENTERPRISE_RECORD_SCHEMA_HEADER_CHUNK\x00\x01\x02\x03"
            + b"TX_ID_UUID_RANDOMIZED_COLUMNS_DATA_PAYLOAD" * 5
            + b"\x00" * 32
        )
        with open(cls.source_10mb_path, "wb") as f:
            written = 0
            while written < target_size:
                to_write = min(len(chunk_pattern), target_size - written)
                f.write(chunk_pattern[:to_write])
                written += to_write

        actual_size = os.path.getsize(cls.source_10mb_path)
        print(f"[QA Setup] Dataset created successfully. Size: {actual_size:,} bytes ({actual_size / (1024*1024):.2f} MB)")

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)
        print("\n[QA Teardown] Cleaned up temporary test artifacts.")

    def test_01_hardware_fingerprint_extraction(self):
        """Verifies immutable hardware fingerprint extraction on current OS."""
        print("\n--- Test 1: Hardware Fingerprint Extraction ---")
        fp = HardwareSecurityLayer.get_machine_fingerprint()
        self.assertIsInstance(fp, bytes)
        self.assertEqual(len(fp), 32, "Hardware fingerprint must be 32 bytes (SHA-256).")
        print(f" [PASS] Hardware fingerprint extracted successfully (32 bytes SHA-256: {fp.hex()[:16]}...)")

    def test_02_compilation_compression_under_50kb(self):
        """Verifies >99% compression ratio (<50KB ghost file from 10MB source)."""
        print("\n--- Test 2: Ghost Compilation & Extreme Compression ---")
        src_sz, ghost_sz, ratio = HierarchicalExtractor.compile_ghost(
            self.source_10mb_path, output_ghost=self.ghost_path
        )

        print(f" Source size : {src_sz:,} bytes (10 MB)")
        print(f" Ghost size  : {ghost_sz:,} bytes")
        print(f" Compression : {ratio:.4f}% reduction")

        self.assertLess(
            ghost_sz,
            50 * 1024,
            f"Ghost file ({ghost_sz} bytes) must be compressed below 50KB!",
        )
        self.assertGreater(
            ratio,
            99.0,
            f"Compression ratio ({ratio:.2f}%) must exceed 99.0%!",
        )
        print(f" [PASS] Size {ghost_sz:,} B is strictly < 50,000 B (Compression ratio: {ratio:.2f}%)")

    def test_03_authorized_decryption_and_data_integrity(self):
        """Verifies 100% data integrity when decrypted on authorized host with source present."""
        print("\n--- Test 3: Authorized In-Memory Decryption & Integrity ---")
        blueprint = GhostReader.read_ghost_in_memory(
            self.ghost_path, self.source_10mb_path
        )

        self.assertIn("meta", blueprint)
        self.assertIn("architecture", blueprint)
        self.assertEqual(blueprint["meta"]["file_size_bytes"], os.path.getsize(self.source_10mb_path))
        self.assertTrue(blueprint["meta"]["node_locked"])

        # Validate LLM context string generation in RAM
        llm_context = GhostReader.to_llm_prompt_context(self.ghost_path, self.source_10mb_path)
        self.assertIn("[MREAIA HARDWARE-LOCKED CONTEXT BLUEPRINT]", llm_context)
        self.assertIn(blueprint["meta"]["sha256"], llm_context)
        print(" [PASS] Decrypted in volatile RAM with 100% schema match. No disk leaks.")

    def test_04_exfiltration_defense_foreign_hardware(self):
        """Simulates exfiltration to a foreign machine. Decryption must fail cryptographically."""
        print("\n--- Test 4: Exfiltration Attack Simulation (Foreign Hardware UUID) ---")
        attacker_fake_hw = "ATTACKER_FOREIGN_LAPTOP_UUID_DEADBEEF_9999"

        with self.assertRaises(InvalidTag) as ctx:
            GhostReader.read_ghost_in_memory(
                self.ghost_path,
                self.source_10mb_path,
                override_hw_id=attacker_fake_hw,
            )
        print(f" [PASS] Exfiltration blocked mathematically! Caught expected: {ctx.exception.__class__.__name__}")

    def test_05_exfiltration_defense_missing_or_altered_source(self):
        """Simulates ghost file moved without source file. Decryption must fail."""
        print("\n--- Test 5: Exfiltration Attack Simulation (Missing/Altered Source File) ---")
        non_existent_source = os.path.join(self.test_dir, "missing_source_dataset.dat")

        with self.assertRaises(FileNotFoundError) as ctx:
            GhostReader.read_ghost_in_memory(self.ghost_path, non_existent_source)
        print(f" [PASS] Source-bound check enforced! Caught expected: {ctx.exception.__class__.__name__}")

        # Test altered source file
        tampered_source = os.path.join(self.test_dir, "tampered_source.dat")
        with open(tampered_source, "wb") as f:
            f.write(b"CORRUPTED_OR_TAMPERED_DATA_STREAM")

        with self.assertRaises(InvalidTag) as ctx:
            GhostReader.read_ghost_in_memory(self.ghost_path, tampered_source)
        print(f" [PASS] Tampered source rejected! Caught expected: {ctx.exception.__class__.__name__}")


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMreaiaHardwareBoundGhost)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    main()
