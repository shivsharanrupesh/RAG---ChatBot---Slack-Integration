"""
Slack Bot for Internal IT Support Chatbot (RAG, Cohere, ChromaDB)

- Listens for messages/mentions in Slack
- Sends question & session_id to FastAPI backend
- Returns answer and sources directly in Slack

Requirements:
- SLACK_BOT_TOKEN (starts with xoxb-)
- SLACK_APP_TOKEN (starts with xapp-, for Socket Mode)
- FASTAPI backend running and accessible

Run: python slack_bot.py
"""

import os
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")  # Socket Mode token
FASTAPI_URL = os.environ.get("FASTAPI_URL", "http://localhost:8000/ask")

if not SLACK_BOT_TOKEN or not SLACK_APP_TOKEN:
    raise EnvironmentError("Both SLACK_BOT_TOKEN and SLACK_APP_TOKEN must be set in your environment.")

app = App(token=SLACK_BOT_TOKEN)

def ask_backend(question, session_id):
    """
    Send a question to FastAPI backend and get the answer and sources.
    """
    payload = {
        "question": question,
        "session_id": session_id,
    }
    try:
        response = requests.post(FASTAPI_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        answer = data.get("answer", "No answer found.")
        sources = data.get("sources", [])
        if sources:
            sources_text = "\n".join([f"- {src['source']} (page {src['page']})" for src in sources if src['source']])
            answer = f"{answer}\n\n*Sources:*\n{sources_text}"
        return answer
    except Exception as e:
        return f"Error contacting backend: {e}"

@app.event("app_mention")
def handle_app_mention_events(body, say):
    """
    Handle @bot mentions in channels.
    """
    event = body.get("event", {})
    user = event.get("user")
    text = event.get("text", "")
    channel = event.get("channel")
    thread_ts = event.get("ts")

    # Remove bot mention from text
    question = text.split('>', 1)[-1].strip() if '>' in text else text.strip()
    session_id = user  # Slack user ID as session_id

    # Call backend
    answer = ask_backend(question, session_id)
    say(text=answer, thread_ts=thread_ts)

@app.event("message")
def handle_direct_message_events(body, say, logger):
    """
    Handle DMs to the bot (direct message support).
    """
    event = body.get("event", {})
    channel_type = event.get("channel_type")
    user = event.get("user")
    text = event.get("text", "")
    thread_ts = event.get("ts")

    # Respond only in direct messages (IM)
    if channel_type == "im" and user:
        session_id = user
        answer = ask_backend(text.strip(), session_id)
        say(text=answer, thread_ts=thread_ts)

if __name__ == "__main__":
    print("Slack bot is running...")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
