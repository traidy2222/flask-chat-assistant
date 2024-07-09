
def jarvis_response(user_input):
    responses = {
        "introduce yourself": "I am JARVIS, your personal assistant. How may I assist you today?",
        "default": "I'm here to assist you with any tasks you need. Please provide your instructions."
    }
    return responses.get(user_input.lower(), responses["default"])

