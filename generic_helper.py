from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import random

app = FastAPI()

# Hardcoded responses for simplicity
responses = {
    "greet": ["Hello! How can I help you today?", "Hi there! What can I do for you today?"],
    "goodbye": ["Goodbye! Have a great day!", "See you later! Take care!"],
    "ask_question": {
        "What is your name?": "I am your friendly chatbot.",
        "How are you?": "I'm doing great, thank you!",
    },
}

ongoing_conversations = {}  # To store ongoing conversations


@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()
    
    # Extract necessary information from the payload
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    session_id = parameters.get('session_id', 'default_session')
    
    # Map intents to appropriate handlers
    intent_handler_dict = {
        'greet': handle_greeting,
        'goodbye': handle_goodbye,
        'ask_question': handle_user_query,
        'conversation_status': get_conversation_status
    }

    if intent in intent_handler_dict:
        return intent_handler_dict[intent](parameters, session_id)
    else:
        return JSONResponse(content={"fulfillmentText": "I couldn't understand your request. Can you rephrase?"})


def handle_greeting(parameters: dict, session_id: str):
    """
    Handle greeting intents from the user.
    """
    greeting_response = random.choice(responses['greet'])
    return JSONResponse(content={"fulfillmentText": greeting_response})


def handle_goodbye(parameters: dict, session_id: str):
    """
    Handle goodbye intents from the user.
    """
    goodbye_response = random.choice(responses['goodbye'])
    return JSONResponse(content={"fulfillmentText": goodbye_response})


def handle_user_query(parameters: dict, session_id: str):
    """
    Handle user's general queries based on hardcoded responses.
    """
    user_query = parameters.get("query")
    query_response = responses['ask_question'].get(user_query, "I'm sorry, I don't have an answer to that.")

    # Log conversation history
    if session_id not in ongoing_conversations:
        ongoing_conversations[session_id] = []
    ongoing_conversations[session_id].append({"user": user_query, "bot": query_response})

    return JSONResponse(content={"fulfillmentText": query_response})


def get_conversation_status(parameters: dict, session_id: str):
    """
    Retrieve the status or history of a conversation for a given session.
    """
    if session_id in ongoing_conversations:
        conversation_history = ongoing_conversations[session_id]
        formatted_history = "\n".join([f"User: {item['user']}\nBot: {item['bot']}" for item in conversation_history])
        fulfillment_text = f"Here's the history of your conversation:\n{formatted_history}"
    else:
        fulfillment_text = "No conversation history found for your session."

    return JSONResponse(content={"fulfillmentText": fulfillment_text})
