import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from rag_chatbot import RAGChatbot

# Load environment variables
load_dotenv()

# Initialize the Slack app
app = App(token=os.environ["SLACK_BOT_TOKEN"])

# Jira wiki configuration
jira_config = {
    'base_url': os.environ["JIRA_BASE_URL"],
    'username': os.environ["JIRA_USERNAME"],
    'api_token': os.environ["JIRA_API_TOKEN"],
    'space_key': os.environ["JIRA_SPACE_KEY"]
}

# Initialize your RAG chatbot with the data directory and Jira config
chatbot = RAGChatbot('./data', jira_config=jira_config)

@app.event("app_mention")
def handle_mention(event, say):
    user = event['user']
    text = event['text']
    
    # Remove the bot mention from the text
    text = text.split('>')[-1].strip()
    
    # Get response from the RAG chatbot
    response = chatbot.get_response(text)
    
    say(f"<@{user}> {response}")

@app.event("message")
def handle_message(event, say):
    if event.get('channel_type') == 'im':
        user = event['user']
        text = event['text']
        
        # Get response from the RAG chatbot
        response = chatbot.get_response(text)
        
        say(f"<@{user}> {response}")

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()