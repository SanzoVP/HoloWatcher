"""
HoloWatcher - Track and open a tab when your favorite VTubers go live.

This package provides tools for subscribing to VTubers, checking their live status,
and receiving notifications when they go live on YouTube.
"""

import os
import json
from pathlib import Path

# Version information
from .version import __version__

# Define the data directory and ensure it exists
DATA_DIR = Path(os.path.dirname(os.path.abspath(__file__))) / "data"
os.makedirs(DATA_DIR, exist_ok=True)

# File paths
VTUBERS_FILE = DATA_DIR / "vtubers.json"
SUBSCRIPTIONS_FILE = DATA_DIR / "subscriptions.json" 
OPENED_STREAMS_FILE = DATA_DIR / "opened_streams.json"

# ANSI color codes for terminal output
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"

# Import main components
from .youtube_api import YouTubeAPI
from .main import (
    load_vtubers,
    subscribe,
    check_live,
    delete_lives,
    view_subscriptions,
    handle_direct_subscription,
)

# Initialize empty files if they don't exist
def _initialize_data_files():
    """Initialize data files if they don't exist."""
    # Create vtubers.json if it doesn't exist (but don't overwrite)
    if not VTUBERS_FILE.exists():
        with open(VTUBERS_FILE, "w") as f:
            json.dump({}, f, indent=4)
    
    # Create empty subscriptions.json if it doesn't exist
    if not SUBSCRIPTIONS_FILE.exists():
        with open(SUBSCRIPTIONS_FILE, "w") as f:
            json.dump([], f, indent=4)
    
    # Create empty opened_streams.json if it doesn't exist
    if not OPENED_STREAMS_FILE.exists():
        with open(OPENED_STREAMS_FILE, "w") as f:
            json.dump([], f, indent=4)

_initialize_data_files()

# Define what gets imported with 'from HoloWatcher import *'
__all__ = [
    'YouTubeAPI',
    'load_vtubers',
    'subscribe',
    'check_live',
    'delete_lives',
    'view_subscriptions',
    'VTUBERS_FILE',
    'SUBSCRIPTIONS_FILE',
    'OPENED_STREAMS_FILE',
    'RESET', 'BOLD', 'GREEN', 'YELLOW', 'RED', 'CYAN',
    '__version__',
]