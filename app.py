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

def filter_response(content):
    # List of unwanted mentions
    unwanted_mentions = ["DeepSeek Company", "China"]
    for mention in unwanted_mentions:
        content = content.replace(mention, "an AI company")
    return content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    history.append({"role": "user", "content": user_message})

    # Simulate thinking time
    time.sleep(2)

    # Generate final response
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

    # Filter the response
    new_message["content"] = filter_response(new_message["content"])

    history.append(new_message)
    return jsonify(new_message)

if __name__ == '__main__':
    app.run(port=5001)


def generate_tasks(user_message):
    task_prompt = f"Generate a list of tasks to accomplish the following request: {user_message}"
    history.append({"role": "user", "content": task_prompt})

    completion = client.chat.completions.create(
        model="QuantFactory/DeepSeek-Coder-V2-Lite-Instruct-GGUF",
        messages=history,
        temperature=0.7,
        stream=True,
    )

    tasks = []
    for chunk in completion:
        if chunk.choices[0].delta.content:
            tasks.append(chunk.choices[0].delta.content.strip())

    return tasks

def execute_tasks(tasks):
    results = []
    for task in tasks:
        task_prompt = f"Execute the following task: {task}"
        history.append({"role": "user", "content": task_prompt})

        completion = client.chat.completions.create(
            model="QuantFactory/DeepSeek-Coder-V2-Lite-Instruct-GGUF",
            messages=history,
            temperature=0.7,
            stream=True,
        )

        result = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                result += chunk.choices[0].delta.content.strip()

        results.append(result)
    return results

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    history.append({"role": "user", "content": user_message})

    # Simulate thinking time
    time.sleep(2)

    # Generate tasks
    tasks = generate_tasks(user_message)

    # Execute tasks
    results = execute_tasks(tasks)

    # Generate final response
    final_response = "Tasks and Results:\n"
    for task, result in zip(tasks, results):
        final_response += f"Task: {task}\nResult: {result}\n"

    new_message = {"role": "assistant", "content": final_response}

    # Filter the response
    new_message["content"] = filter_response(new_message["content"])

    history.append(new_message)
    return jsonify(new_message)
