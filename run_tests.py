#!/usr/bin/env python
"""
Wrapper script to run tests from the project root.
Use it in PyCharm instead of running the tests directly.
"""

import os
import sys
from pathlib import Path
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parent
os.chdir(PROJECT_ROOT)

print(f"📁 Project Root: {PROJECT_ROOT}")
print(f"📁 Changed to: {Path.cwd()}\n")

pytest_args = sys.argv[1:] if len(sys.argv) > 1 else ['tests/']

# Execute pytest
cmd = [sys.executable, '-m', 'pytest'] + pytest_args
print(f"🚀 Executing: {' '.join(cmd)}\n")

subprocess.run(cmd)