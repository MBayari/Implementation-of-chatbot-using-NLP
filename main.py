# Author: Dhaval Patel. Codebasics YouTube Channel

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_helper
import generic_helper

app = FastAPI()

ongoing_conversations = {}  # Dictionary to store user session data


@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the Dialogflow request
    payload = await request.json()

    # Extract necessary information
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(output_contexts[0]["name"])

    # Map intents to appropriate handlers
    intent_handler_dict = {
        'query.ask': handle_user_query,
        'conversation.log': log_conversation,
        'conversation.status': get_conversation_status
    }

    if intent in intent_handler_dict:
        return intent_handler_dict[intent](parameters, session_id)
    else:
        return JSONResponse(content={"fulfillmentText": "I couldn't understand your request. Can you rephrase?"})


def log_query_to_db(session_id: str, query: str):
    """
    Save the user query to the database for logging purposes.
    """
    try:
        db_helper.log_user_query(session_id, query)
        return True
    except Exception as e:
        print(f"Error logging query: {e}")
        return False


def handle_user_query(parameters: dict, session_id: str):
    """
    Handle user's general queries by searching in the FAQ database or using AI-generated responses.
    """
    user_query = parameters.get("query")
    
    # Log the query
    log_query_to_db(session_id, user_query)

    # Search for a predefined response in the FAQ database
    response = db_helper.fetch_faq_response(user_query)

    if response:
        fulfillment_text = response
    else:
        # Fallback to a default response if no matching FAQ entry is found
        fulfillment_text = "I'm sorry, I couldn't find an answer to your question. Let me get back to you!"

    return JSONResponse(content={"fulfillmentText": fulfillment_text})


def log_conversation(parameters: dict, session_id: str):
    """
    Log conversation context or store intermediate data for ongoing conversation sessions.
    """
    user_message = parameters.get("message")
    if session_id in ongoing_conversations:
        ongoing_conversations[session_id].append(user_message)
    else:
        ongoing_conversations[session_id] = [user_message]

    return JSONResponse(content={
        "fulfillmentText": f"Your message has been logged: '{user_message}'. Anything else?"
    })


def get_conversation_status(parameters: dict, session_id: str):
    """
    Retrieve the status or history of a conversation for a given session.
    """
    if session_id in ongoing_conversations:
        conversation_history = ongoing_conversations[session_id]
        formatted_history = "\n".join(conversation_history)
        fulfillment_text = f"Here's the history of your conversation:\n{formatted_history}"
    else:
        fulfillment_text = "No conversation history found for your session."

    return JSONResponse(content={"fulfillmentText": fulfillment_text})
