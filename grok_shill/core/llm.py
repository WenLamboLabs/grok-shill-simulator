import json
from typing import List

import litellm
from bs4 import BeautifulSoup
from litellm import completion

from grok_shill.integrations.firecrawl_tool import FIRECRAWL_TOOL
from grok_shill.integrations.firecrawl_tool import scrape_webpage
from grok_shill.core.prompt import RESEARCH_PROMPT
from grok_shill.core.prompt import SHILL_PROMPT

litellm.modify_params = True

CLAUDE_SONNET = 'anthropic/claude-sonnet-4-0'


def generate_shill_posts(
	crypto_project_info: str, influencer_posts: str, num_posts: int, model: str = CLAUDE_SONNET
) -> List[str]:
	"""Generate crypto shill posts in an influencer's style."""
	prompt_with_data = SHILL_PROMPT.replace('{{CRYPTO_PROJECT_INFO}}', crypto_project_info)
	prompt_with_data = prompt_with_data.replace('{{INFLUENCER_POSTS}}', influencer_posts)
	prompt_with_data = prompt_with_data.replace('{{NUM_POSTS}}', str(num_posts))

	llm_messages = [{'role': 'user', 'content': prompt_with_data}]

	response = completion(model=model, messages=llm_messages, temperature=1, reasoning_effort='low')

	response_content = response.choices[0].message.content
	soup = BeautifulSoup(response_content, 'html.parser')

	post_tags = soup.find_all('post')
	return [post.get_text().strip() for post in post_tags]


def research_crypto_project(project_text: str, model: str = CLAUDE_SONNET) -> str:
	"""Research a crypto project using web scraping to gather positive information."""
	prompt_with_data = RESEARCH_PROMPT.replace('{{PROJECT_TEXT}}', project_text)

	messages = [{'role': 'user', 'content': prompt_with_data}]

	while True:
		response = completion(model=model, messages=messages, tools=[FIRECRAWL_TOOL])
		message = response.choices[0].message

		if not message.tool_calls:
			# no more tool calls, this should be the final response
			soup = BeautifulSoup(message.content, 'html.parser')
			report_tag = soup.find('positive_report')

			if report_tag:
				return report_tag.get_text().strip()
			else:
				# if no positive_report tag found, return the raw content
				return message.content

		# add the assistant's message to the conversation
		messages.append(message.model_dump())

		# process all tool calls in this round
		for tool_call in message.tool_calls:
			if tool_call.function.name == 'scrape_webpage':
				args = json.loads(tool_call.function.arguments)
				result = scrape_webpage(args['url'])

				messages.append(
					{
						'role': 'tool',
						'tool_call_id': tool_call.id,
						'name': tool_call.function.name,
						'content': json.dumps(result),
					}
				)

		# continue the loop to get the next response
