"""
Pytest configuration file for inheritance distribution calculator tests.
"""

import os
import sys
import pytest

# Add the parent directory to PYTHONPATH so that we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 