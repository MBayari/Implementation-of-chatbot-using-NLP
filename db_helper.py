import re

# Sample FAQ dataset (in place of a database)
faq_data = {
    "What are your hours of operation?": "Our operation hours are from 9 AM to 9 PM every day.",
    "What is your location?": "We are located at 123 Main Street, City XYZ.",
    "How can I contact support?": "You can contact support by email at support@example.com.",
    "What services do you offer?": "We offer a variety of services including product sales, customer support, and more.",
}

# In-memory conversation log (to replace MySQL logging)
conversation_history = []

# In-memory session tracker (to simulate session ID management)
session_tracker = {}

# Function to simulate logging user query (in-memory storage)
def log_user_query(user_id, query_text):
    conversation_history.append({"user_id": user_id, "query": query_text})
    print(f"Logged query from user {user_id}: {query_text}")
    return 1

# Function to fetch a predefined FAQ response
def fetch_faq_response(query_text):
    # Search for a matching query in the FAQ dataset
    response = faq_data.get(query_text, "Sorry, I couldn't find an answer to your question.")
    return response

# Function to handle conversation session (using simple in-memory session tracker)
def start_new_session(user_id):
    session_id = len(session_tracker) + 1  # Generating a simple session ID
    session_tracker[session_id] = {"user_id": user_id, "status": "active"}
    print(f"New session started for user {user_id} with session ID {session_id}")
    return session_id

# Function to update conversation status (in-memory tracking)
def update_conversation_status(session_id, status):
    if session_id in session_tracker:
        session_tracker[session_id]["status"] = status
        print(f"Session {session_id} status updated to {status}")
        return 1
    else:
        return -1

# Function to fetch the next available session ID (using simple count)
def get_next_session_id():
    return len(session_tracker) + 1

# Function to fetch the conversation history for a user (using in-memory storage)
def get_conversation_history(user_id):
    history = [entry for entry in conversation_history if entry['user_id'] == user_id]
    return history

# Main function to simulate chatbot interaction
def chatbot_main():
    user_id = 1  # Example user_id
    session_id = start_new_session(user_id)
    
    while True:
        # Simulate user query input
        user_query = input("You: ")

        # Log the user query
        log_user_query(user_id, user_query)

        # Fetch the response from the FAQ (simple NLP approach using matching)
        bot_response = fetch_faq_response(user_query)

        # Display the bot response
        print(f"Bot: {bot_response}")

        # Ask if the user wants to continue
        continue_chat = input("Would you like to ask something else? (yes/no): ").strip().lower()
        if continue_chat != "yes":
            # Update session status and end conversation
            update_conversation_status(session_id, "completed")
            break

    # Optionally print conversation history for the session
    history = get_conversation_history(user_id)
    print("\nConversation History:")
    for entry in history:
        print(f"User: {entry['query']} - Bot: {fetch_faq_response(entry['query'])}")

# Run the chatbot simulation
if __name__ == "__main__":
    chatbot_main()
