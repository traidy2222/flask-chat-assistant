
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import time
import requests

app = Flask(__name__)

# Point to the local server
client = OpenAI(base_url="http://202.169.113.228:1234/v1", api_key="lm-studio")

history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
    {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
]

def filter_response(content):
    # List of unwanted mentions
    unwanted_mentions = ["DeepSeek Company", "China"]
    for mention in unwanted_mentions:
        content = content.replace(mention, "an AI company")
    return content

def get_response_time(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    return end_time - start_time

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    history.append({"role": "user", "content": user_message})

    # Simulate thinking time
    time.sleep(2)

    # Check if the message is an action request
    if "response time" in user_message.lower():
        # Generate Thought
        thought_prompt = f"Thought: I should check the response time for the web page first."
        history.append({"role": "assistant", "content": thought_prompt})

        # Generate Action
        action_prompt = {
            "function_name": "get_response_time",
            "function_params": {
                "url": "https://learnwithhasan.com"
            }
        }
        history.append({"role": "assistant", "content": f"Action: {action_prompt}"})

        # Simulate PAUSE
        time.sleep(2)

        # Execute Action
        response_time = get_response_time(action_prompt["function_params"]["url"])

        # Generate Action_Response
        action_response_prompt = f"Action_Response: {response_time}"
        history.append({"role": "assistant", "content": action_response_prompt})

        # Generate final Answer
        final_response = f"Answer: The response time for learnwithhasan.com is {response_time} seconds."
        new_message = {"role": "assistant", "content": final_response}
    else:
        # Generate a regular chat response
        response = client.completions.create(
            model="QuantFactory/DeepSeek-Coder-V2-Lite-Instruct-GGUF",
            prompt=history,
            temperature=0.7,
            max_tokens=150
        )
        new_message = {"role": "assistant", "content": response.choices[0].text}

    # Filter the response
    new_message["content"] = filter_response(new_message["content"])

    history.append(new_message)
    return jsonify(new_message)

if __name__ == '__main__':
    app.run(port=5001)

