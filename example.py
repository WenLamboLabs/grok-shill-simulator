from grok_shill.core.llm import generate_shill_posts
from grok_shill.core.llm import research_crypto_project
from grok_shill.integrations.rapidapi import get_full_user_timeline

PROJECT = """
$GAME 
- @GAME_Virtuals
- https://docs.game.virtuals.io/
- https://www.coingecko.com/en/coins/game-by-virtuals
"""


def fetch_influencer_posts(username: str) -> str:
	tweets = get_full_user_timeline(username)
	return '\n\n'.join(tweets)


def print_shill_posts(posts: list[str]) -> None:
	print('Generated shill posts:')
	for i, post in enumerate(posts, 1):
		print(f'\nPost {i}:')
		print(post)


def main() -> None:
	"""Generate crypto shill posts by researching project and mimicking influencer style."""
	print('Researching crypto project...')
	researched_info = research_crypto_project(PROJECT)
	print('Research complete.\n')
	print(researched_info)

	influencer_posts = fetch_influencer_posts('aixbt_agent')
	shill_posts = generate_shill_posts(researched_info, influencer_posts, 3)

	print_shill_posts(shill_posts)


if __name__ == '__main__':
	main()
