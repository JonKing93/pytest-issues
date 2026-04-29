"""
Type hints used throughout the package
"""

import re

Match = str | re.Pattern[str]
Types = type | tuple[type, ...]
