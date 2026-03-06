"""PyInstaller entry point — no relative imports."""
import sys
import os

# Make the cli/ directory importable as a package root
sys.path.insert(0, os.path.dirname(__file__))

from muapi.main import app

if __name__ == "__main__":
    app()
