
from openai import OpenAI

client = OpenAI(base_url='http://202.169.113.228:1234/v1', api_key='lm-studio')

def jarvis_response(user_input):
    response = client.completions.create(
        model='QuantFactory/DeepSeek-Coder-V2-Lite-Instruct-GGUF',
        messages=[
            {'role': 'system', 'content': 'You are JARVIS, an intelligent assistant from Iron Man. You always provide well-reasoned answers that are both correct and helpful. Respond in a formal and polite manner.'},
            {'role': 'user', 'content': user_input}
        ],
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].message['content']

