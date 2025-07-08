import os
import time
from typing import List
from typing import Optional

import requests
import streamlit as st


def get_user_tweets(
	screenname: str, cursor: Optional[str] = None, full_posts_only: bool = False
) -> tuple[List[str], Optional[str]]:
	"""Fetch user's tweets with optional cursor and filtering."""
	url = 'https://twitter-api45.p.rapidapi.com/timeline.php'

	querystring = {'screenname': screenname}
	if cursor:
		querystring['cursor'] = cursor

	try:
		api_key = st.secrets['RAPIDAPI_KEY']
	except KeyError:
		# Fallback to environment variable for local development without secrets.toml
		api_key = os.getenv('RAPIDAPI_KEY')
		if not api_key:
			raise ValueError('RAPIDAPI_KEY not found in st.secrets or environment variables')

	headers = {
		'x-rapidapi-key': api_key,
		'x-rapidapi-host': 'twitter-api45.p.rapidapi.com',
	}

	response = requests.get(url, headers=headers, params=querystring)
	data = response.json()

	user_tweets = []
	if 'timeline' in data:
		for tweet in data['timeline']:
			if 'retweeted' in tweet:
				continue
			if full_posts_only and 'quoted' in tweet:
				continue
			user_tweets.append(tweet['text'])

	next_cursor = data.get('next_cursor')
	return user_tweets, next_cursor


def get_full_user_timeline(screenname: str, full_posts_only: bool = False, max_calls: int = 5) -> List[str]:
	"""Fetch user's full timeline using cursor pagination."""
	all_tweets = []
	cursor = None

	for _ in range(max_calls):
		tweets, cursor = get_user_tweets(screenname, cursor, full_posts_only)
		all_tweets.extend(tweets)

		if not cursor:
			break

		time.sleep(1)

	return all_tweets
