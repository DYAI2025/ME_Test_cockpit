import os
from typing import Dict

import openai


def gpt4_analysis(text: str) -> str:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return 'No API key provided.'
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[{'role': 'user', 'content': text}],
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f'Error calling OpenAI API: {e}'
