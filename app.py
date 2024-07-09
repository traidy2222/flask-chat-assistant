# This is a test comment to verify commit and push
from flask import Flask, request, jsonify, render_template
from personality import jarvis_response
from openai import OpenAI
import time
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Point to the local server
client = OpenAI(base_url="http://202.169.113.228:1234/v1", api_key="lm-studio")

history = [
    {"role": "system", "content": "You are JARVIS, an intelligent assistant from Iron Man. You always provide well-reasoned answers that are both correct and helpful. Respond in a formal and polite manner."},
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

@app.route('/start', methods=['GET'])
def start():
    initial_message = {"role": "assistant", "content": "I am JARVIS, your personal assistant. How may I assist you today?"}
    history.append(initial_message)
    return jsonify(initial_message)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    history.append({"role": "user", "content": user_message})

    # Simulate thinking time
    time.sleep(2)

    # Generate response using jarvis_response function
    response_message = jarvis_response(user_message)
    new_message = {"role": "assistant", "content": response_message}

    # Filter the response
    new_message["content"] = filter_response(new_message["content"])

    history.append(new_message)
    return jsonify(new_message)

if __name__ == '__main__':
    app.run(port=5001)
