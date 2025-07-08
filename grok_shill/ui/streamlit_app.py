import streamlit as st

from grok_shill.core.llm import generate_shill_posts
from grok_shill.core.llm import research_crypto_project
from grok_shill.integrations.rapidapi import get_full_user_timeline

# Static examples data
PROJECT_EXAMPLES = {
	'$VIRTUAL': """$VIRTUAL - AI Agent Infrastructure
- https://www.virtuals.io/about
- https://virtuals.substack.com/p/virtuals-monthly-update-may-2025
- https://www.coingecko.com/en/coins/virtual-protocol
""",
	
	'$REI': """
- Up 41.88% over 7 days with $808.66K in net DEX inflows.
- $113.6M market cap, $3.19M liquidity.

REI is one of the OG research agent infrastructures . 
It's live on both Base and Hyperliquid; two ecosystems set to explode this cycle imo.
Smaller labs (like REI) are gaining attention for innovative architectures amid the 2025 push for AGI breakthroughs. 
Its "Bowtie" architecture's dual memory system reflects advances in cognitive science, inspired by human brain studies published in early 2025.
Smaller protocols aren't going to be able to compete with the warchests of the top research labs, so REI is taking a smart approach for AGI breakthrough. """,

	'$TAO': """Bittensor is an open-source protocol that utilizes blockchain technology to create a decentralized machine learning network.
	
https://bittensor.com/intro
https://bittensor.com/whitepaper
https://coinmarketcap.com/currencies/bittensor/
""",

	'$SOL': """
- ETF decision expected by October 10 with 90% approval probability, coinciding with Fire Dancer upgrade implementation as price catalysts.
- Former Solana Labs advisor Nikita Bier appointed as Product Head at X, signaling increased crypto-social media convergence and potential future integrations.
- Weekly DEX volume reaches $19B with Pump ($6.67B), Raydium ($4.67B), and Orca ($2.52B) leading trading activity, showing 7.5% week-over-week decline.
- New staking ETF implementation confirmed to operate through direct spot purchasing and staking of tokens for price exposure and yield generation, with no pre-purchasing conducted.
- Major exchanges split ecosystem integration: Robinhood and Coinbase choose ETH L2s (Optimism/Arbitrum), while Bybit and Kraken maintain Solana integration, establishing clear market segmentation in exchange partnerships.
"""
}

INFLUENCER_EXAMPLES = [
	'aixbt_agent',
	'S4mmyEth',
	'degentradingLSD', 
	'YashasEdu'
]

# Configure page title and icon
st.set_page_config(page_title='Grok Shill Simulator', page_icon='👀')

def main():
	st.title('Grok Shill Simulator')
	st.markdown('Cook alpha posts that actually move markets. Analyze any project + mimic top CT influencers. Built by [WenLambo Labs](https://wenl.ai/blog/grok-shill-simulator).')

	# Initialize session state for caching
	if 'researched_info' not in st.session_state:
		st.session_state.researched_info = None
	if 'cached_project_text' not in st.session_state:
		st.session_state.cached_project_text = None
	if 'influencer_posts' not in st.session_state:
		st.session_state.influencer_posts = None
	if 'cached_username' not in st.session_state:
		st.session_state.cached_username = None
	if 'generated_posts' not in st.session_state:
		st.session_state.generated_posts = None
	if 'project_text' not in st.session_state:
		st.session_state.project_text = ''
	if 'username' not in st.session_state:
		st.session_state.username = ''


	# Project text input
	project_text = st.text_area(
		'Project Alpha (links, descriptions):',
		value=st.session_state.project_text,
		height=150,
		placeholder='Drop your project intel, links, token info...'
	)
	
	# Quick fill buttons for project examples
	cols = st.columns(len(PROJECT_EXAMPLES))
	for i, (name, content) in enumerate(PROJECT_EXAMPLES.items()):
		with cols[i]:
			if st.button(f'{name}', use_container_width=True, type='secondary'):
				st.session_state.project_text = content.strip()
				st.rerun()
	
	st.divider()  # Subtle divider
	
	# Username input
	username = st.text_input(
		'CT Influencer to Clone:',
		value=st.session_state.username,
		placeholder='X handle (no @)'
	)
	
	# Quick fill buttons for username examples
	cols = st.columns(len(INFLUENCER_EXAMPLES))
	for i, username_example in enumerate(INFLUENCER_EXAMPLES):
		with cols[i]:
			if st.button(f'{username_example}', use_container_width=True, type='secondary'):
				st.session_state.username = username_example
				st.rerun()
	
	st.markdown('')  # Add some spacing
	
	# Update session state with current values
	st.session_state.project_text = project_text
	st.session_state.username = username
	
	# Main action button
	if st.button('🎯 Generate Posts', type='secondary', use_container_width=True):
		if project_text and username:
			run_full_workflow(project_text, username)
		else:
			st.warning('👀 Anon, need both project alpha and influencer to cook with')
	
	# Display results if available
	if st.session_state.generated_posts:
		display_results(st.session_state.generated_posts)


def run_full_workflow(project_text: str, username: str):
	"""Run the complete workflow: research → fetch posts → generate shill posts."""
	with st.status('Running shill post generation...', expanded=True) as status:
		# Step 1: Research project (with caching)
		if st.session_state.cached_project_text == project_text and st.session_state.researched_info:
			st.write('🤿 Using cached project research...')
			researched_info = st.session_state.researched_info
			st.write('✅ Cached project research loaded!')
		else:
			st.write('🤿 Deep diving the project...')
			try:
				researched_info = research_crypto_project(project_text)
				st.session_state.researched_info = researched_info
				st.session_state.cached_project_text = project_text
				st.write('✅ Alpha extracted!')
			except Exception as e:
				st.error(f'❌ Research failed: {str(e)}')
				st.stop()

		# Step 2: Fetch influencer posts (with caching)
		if st.session_state.cached_username == username and st.session_state.influencer_posts:
			st.write('👀 Using cached influencer posts...')
			influencer_posts = st.session_state.influencer_posts
			st.write('✅ Cached influencer posts loaded!')
		else:
			st.write("👀 Studying the influencer's flow...")
			try:
				tweets = get_full_user_timeline(username)
				influencer_posts = '\n\n'.join(tweets)
				st.session_state.influencer_posts = influencer_posts
				st.session_state.cached_username = username
				st.write(f'✅ Retrieved {len(tweets)} posts from @{username}')
			except Exception as e:
				st.error(f'❌ Failed to fetch posts: {str(e)}')
				st.stop()

		# Step 3: Generate shill posts
		st.write('🧠 Generating shill posts...')
		try:
			shill_posts = generate_shill_posts(researched_info, influencer_posts, 3)
			st.session_state.generated_posts = shill_posts
			st.write('✅ Shill posts generated!')
		except Exception as e:
			st.error(f'❌ Generation failed: {str(e)}')
			st.stop()

		status.update(label='Shill post generation complete! ⚡', state='complete', expanded=False)


def display_results(posts: list[str]):
	"""Display the generated shill posts."""
	st.subheader('💎 Your Alpha Posts')

	# Display research report if available
	if st.session_state.researched_info:
		with st.expander("📄 View Research Report", expanded=False):
			st.markdown("**Project Research Summary:**")
			# Use text_area in read-only mode for better handling of long text
			st.text_area(
				label="Research findings",
				value=st.session_state.researched_info,
				height=400,
				disabled=True,
				label_visibility="collapsed"
			)
	
	for i, post in enumerate(posts, 1):
		with st.expander(f'📝 Post {i}', expanded=True):
			st.text(post)
			
			# Copy button for each post
			col1, col2 = st.columns([3, 1])
			with col2:
				if st.button(f'💰 Copy', key=f'copy_{i}', use_container_width=True):
					st.write('✅ Alpha copied ser!')
	
	# Clear cache button
	st.markdown('---')
	if st.button('🗑️ Clear Cache & Start Fresh', type='secondary'):
		st.session_state.researched_info = None
		st.session_state.cached_project_text = None
		st.session_state.influencer_posts = None
		st.session_state.cached_username = None
		st.session_state.generated_posts = None
		st.rerun()

if __name__ == '__main__':
	main()
