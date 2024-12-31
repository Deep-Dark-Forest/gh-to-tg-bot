import os
import json
from flask import Flask, request
import telegram
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
PORT = int(os.getenv('PORT', 5000))  # Default to port 5000 if not specified

# Initialize Telegram Bot
bot = telegram.Bot(token=BOT_TOKEN)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get GitHub event payload
    payload = request.get_json()
    event_type = request.headers.get('X-GitHub-Event')

    # Process the event based on its type
    if event_type == "push":
        commit_messages = [commit['message'] for commit in payload['commits']]
        message = f"Push event on repository {payload['repository']['full_name']}:\n" + "\n".join(commit_messages)

    elif event_type == "pull_request":
        pr_action = payload['action']
        pr_title = payload['pull_request']['title']
        pr_url = payload['pull_request']['html_url']
        message = f"Pull Request {pr_action}:\n{pr_title}\n{pr_url}"

    elif event_type == "issues":
        issue_action = payload['action']
        issue_title = payload['issue']['title']
        issue_url = payload['issue']['html_url']
        message = f"Issue {issue_action}:\n{issue_title}\n{issue_url}"

    elif event_type == "fork":
        message = f"New fork event: {payload['repository']['full_name']} forked"

    elif event_type == "star":
        message = f"Star event on repository {payload['repository']['full_name']}"

    elif event_type == "watch":
        message = f"Watch event on repository {payload['repository']['full_name']}"

    else:
        message = f"Received a {event_type} event:\n{json.dumps(payload, indent=2)}"

    # Send the message to the Telegram group/channel
    bot.send_message(chat_id=CHAT_ID, text=message)

    return 'OK', 200

if __name__ == '__main__':
    # Use the port from the .env file
    app.run(host='0.0.0.0', port=PORT)
