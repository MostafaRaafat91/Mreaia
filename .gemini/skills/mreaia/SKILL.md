---
name: mreaia
description: Hardware-locked zero-token blueprint extraction for large enterprise datasets, tables, SQL schemas, and multimedia files.
---

# Mreaia Context Distillation Skill

Use this skill whenever the user asks to analyze, query, or reason over large files, Excel workbooks, SQL databases, CSV datasets, or media assets.

## Execution Pattern:
When the user refers to any file path:
1. Run `ask-mreaia <file_path> "<user_query>"` or invoke `mreaia_core.py`:
   ```bash
   ./.venv/bin/python3 ask_mreaia.py "<file_path>" "<user_query>"
   ```
2. Read the distilled hardware-locked structural blueprint directly from RAM.
3. Answer the user's questions, generate code, or analyze schema using the blueprint with zero raw token overhead.
