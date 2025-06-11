"""
Utility functions for the detective game
"""

import json
import os
from datetime import datetime


def save_conversation(conversation_history, case_name):
    """Save conversation history to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/conversations/{case_name}_{timestamp}.json"

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w') as f:
        json.dump(conversation_history, f, indent=2)


def load_case_data(case_name):
    """Load case data from file"""
    filename = f"data/cases/{case_name}.json"

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None


def format_conversation_for_display(conversation_history):
    """Format conversation history for better display"""
    formatted = []
    for entry in conversation_history:
        if entry.startswith("Human:"):
            formatted.append(("user", entry[7:]))  # Remove "Human: " prefix
        elif entry.startswith("Detective"):
            formatted.append(("assistant", entry[15:]))  # Remove "Detective Sam: " prefix
    return formatted