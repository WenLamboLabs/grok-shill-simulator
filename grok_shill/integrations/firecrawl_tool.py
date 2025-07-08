import os
from typing import Any
from typing import Dict

import requests
import streamlit as st


def scrape_webpage(url: str) -> Dict[str, Any]:
	"""Scrape webpage content using Firecrawl API."""
	try:
		api_key = st.secrets['FIRECRAWL_API_KEY']
	except KeyError:
		# Fallback to environment variable for local development without secrets.toml
		api_key = os.getenv('FIRECRAWL_API_KEY')
		if not api_key:
			return {'error': 'FIRECRAWL_API_KEY not found in st.secrets or environment variables', 'success': False}

	headers = {'Authorization': f'Bearer {api_key}'}

	try:
		response = requests.post(
			'https://api.firecrawl.dev/v1/scrape',
			headers=headers,
			json={'url': url, 'formats': ['markdown']},
		)
		response.raise_for_status()
		data = response.json()

		if data.get('success'):
			return {
				'content': data.get('data', {}).get('markdown', ''),
				'url': url,
				'success': True,
			}
		return {'error': data.get('error', 'Unknown error'), 'success': False}

	except requests.exceptions.RequestException as e:
		return {'error': str(e), 'success': False}


FIRECRAWL_TOOL = {
	'type': 'function',
	'function': {
		'name': 'scrape_webpage',
		'description': 'Scrape and parse the contents of a webpage',
		'parameters': {
			'type': 'object',
			'properties': {
				'url': {
					'type': 'string',
					'description': 'The URL of the webpage to scrape',
				}
			},
			'required': ['url'],
		},
	},
}
