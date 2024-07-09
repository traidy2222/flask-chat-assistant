from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import time

app = Flask(__name__)

# Point to the local server
client = OpenAI(base_url="http://202.169.113.228:1234/v1", api_key="lm-studio")

history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
    {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    history.append({"role": "user", "content": user_message})

    # Simulate thinking time
    time.sleep(2)

    # Intermediate steps
    intermediate_thoughts = [
        "Hmm, let me think about that...",
        "Considering different aspects...",
        "Analyzing the question..."
    ]
    for thought in intermediate_thoughts:
        time.sleep(1)
        history.append({"role": "assistant", "content": thought})
        # Notify the UI about the thinking process
        yield jsonify({"role": "assistant", "content": thought})

    completion = client.chat.completions.create(
        model="QuantFactory/DeepSeek-Coder-V2-Lite-Instruct-GGUF",
        messages=history,
        temperature=0.7,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}

    for chunk in completion:
        if chunk.choices[0].delta.content:
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)
    yield jsonify(new_message)

if __name__ == '__main__':
    app.run(port=5000)

