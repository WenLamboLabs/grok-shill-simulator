"""Entry point for the Grok Shill Simulator Streamlit app."""

import sys
from pathlib import Path

# Add the project root to Python path for Streamlit Cloud
sys.path.insert(0, str(Path(__file__).parent))

from grok_shill.ui.streamlit_app import main

if __name__ == '__main__':
	main()