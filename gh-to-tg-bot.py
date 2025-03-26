import os
import json
import logging
import hmac
import hashlib
from flask import Flask, request, abort
import telegram
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
SECRET_TOKEN = os.getenv('SECRET_TOKEN')
PORT = int(os.getenv('PORT', 5000))

if not BOT_TOKEN or not CHAT_ID or not SECRET_TOKEN:
    raise ValueError("Environment variables BOT_TOKEN, CHAT_ID, and SECRET_TOKEN must be set.")

try:
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.get_me()
    logging.info("Telegram Bot initialized successfully.")
except telegram.error.InvalidToken:
    raise ValueError("Invalid Telegram Bot Token.")

app = Flask(__name__)

def verify_signature(request, secret):
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        logging.warning("Missing X-Hub-Signature-256 header.")
        return False
    hash_object = hmac.new(secret.encode(), request.data, hashlib.sha256)
    expected_signature = f"sha256={hash_object.hexdigest()}"
    return hmac.compare_digest(expected_signature, signature)

def handle_push_event(payload):
    commit_messages = [commit.get('message', 'No message') for commit in payload.get('commits', [])]
    return f"Push event on repository {payload['repository']['full_name']}:\n" + "\n".join(commit_messages)

def handle_pull_request_event(payload):
    pr_action = payload.get('action', 'unknown action')
    pr_title = payload['pull_request'].get('title', 'No title')
    pr_url = payload['pull_request'].get('html_url', 'No URL')
    return f"Pull Request {pr_action}:\n{pr_title}\n{pr_url}"

def handle_issues_event(payload):
    issue_action = payload.get('action', 'unknown action')
    issue_title = payload['issue'].get('title', 'No title')
    issue_url = payload['issue'].get('html_url', 'No URL')
    return f"Issue {issue_action}:\n{issue_title}\n{issue_url}"

def handle_fork_event(payload):
    return f"New fork event: {payload['repository']['full_name']} forked."

def handle_star_event(payload):
    return f"Star event on repository {payload['repository']['full_name']}."

@app.route('/webhook', methods=['POST'])
def webhook():
    if not verify_signature(request, SECRET_TOKEN):
        logging.warning("Invalid signature. Aborting request.")
        abort(403)
    payload = request.get_json()
    if not payload:
        logging.error("Invalid payload received.")
        return 'Invalid payload.', 400
    event_type = request.headers.get('X-GitHub-Event')
    logging.info(f"Received GitHub event: {event_type}")
    try:
        if event_type == "push":
            message = handle_push_event(payload)
        elif event_type == "pull_request":
            message = handle_pull_request_event(payload)
        elif event_type == "issues":
            message = handle_issues_event(payload)
        elif event_type == "fork":
            message = handle_fork_event(payload)
        elif event_type == "star":
            message = handle_star_event(payload)
        else:
            message = f"Received a {event_type} event:\n{json.dumps(payload, indent=2)}"
        bot.send_message(chat_id=CHAT_ID, text=message)
        logging.info("Message sent to Telegram successfully.")
    except Exception as e:
        logging.error(f"Error processing event: {e}")
        return 'Error processing event.', 500
    return 'OK', 200

if __name__ == '__main__':
    from waitress import serve
    logging.info(f"Starting Flask app on port {PORT}...")
    serve(app, host='0.0.0.0', port=PORT)