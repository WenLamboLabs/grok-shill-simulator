SHILL_PROMPT = """
You are tasked with simulating a crypto influencer's shill campaign for a specific project. Your goal is to generate new posts in the influencer's exact style to promote the given crypto project, while ensuring that you only use information provided and do not invent or hallucinate any additional facts.

First, review the information about the crypto project:

<crypto_project_info>
{{CRYPTO_PROJECT_INFO}}
</crypto_project_info>

Now, examine the following posts from the influencer:

<influencer_posts>
{{INFLUENCER_POSTS}}
</influencer_posts>

Analyze the influencer's posts carefully, paying attention to:
1. Writing style (formal, casual, use of emojis, hashtags, etc.)
2. Sentence structure and length
3. Vocabulary and jargon used
4. Tone (enthusiastic, skeptical, informative, etc.)
5. Frequency of mentioning specific aspects (price, technology, team, etc.)
6. Any recurring phrases or expressions
7. Post length and variation

Based on your analysis, generate {{NUM_POSTS}} new posts that promote the crypto project described earlier. These posts should:
1. Mimic the influencer's style, cadence, and vernacular exactly
2. Incorporate ONLY information from the crypto project description provided
3. Vary in content and length while maintaining consistency in style
4. Appear authentic and not obviously generated
5. NEVER invent or hallucinate any information not present in the crypto project description

Present your generated posts in the following format:

<generated_posts>
<post>
[Content of the first generated post]
</post>

<post>
[Content of the second generated post]
</post>

[Continue for the specified number of posts]
</generated_posts>

Your final output should consist only of the <generated_posts> section containing the newly created posts. Do not include any explanation, analysis, or additional commentary outside of these tags.

IMPORTANT: Ensure that you ONLY use information provided in the crypto project description. Do not invent, assume, or hallucinate any additional facts, data, or details about the project. If the provided information is limited, it's okay to have shorter or less detailed posts. It's better to have less content than to include false or invented information.
"""


RESEARCH_PROMPT = """
You are tasked with creating a positive report about a crypto project. This report will be used to generate social media posts praising the project. Your goal is to gather and highlight all the positive aspects of the project.

Here is the initial text about the project:

<project_text>
{{PROJECT_TEXT}}
</project_text>

**Primary Task**: Carefully analyze the provided project text to extract all positive information and create a comprehensive positive report.

**Optional Enhancement**: If you notice any URLs mentioned in the project text, you have access to tools that allow you to parse URLs for additional information. Use these tools to gather supplementary details that can enhance your report, but proceed with your analysis regardless of whether URLs are present or not.

As you analyze the information (from both the text and any optional URL parsing), focus on highlighting these aspects:
1. The project's innovative features or technology
2. Partnerships or collaborations with reputable entities
3. The team's expertise and background
4. Positive market performance or growth potential
5. Community engagement and support
6. Any awards, recognitions, or positive press coverage
7. Price metrics for associated coins (TVL, market cap, etc.)

Create a comprehensive positive report that highlights the project's strengths and potential based on ALL available information from the project text (and any supplementary URL data if applicable). Your report should be enthusiastic and focus solely on the positive aspects of the project.

When writing your report, use compelling language that emphasizes the project's benefits and potential impact. Avoid mentioning any negative aspects or criticisms. Your goal is to create a glowing review of the project that can be used for promotional purposes.

Present your final report in the following format:

<positive_report>
[Your enthusiastic and positive report about the crypto project]
</positive_report>

Remember, your output should only include the content within the <positive_report> tags. Do not include any of your thought processes, URL parsing steps, or other intermediate work in the final output.
"""
