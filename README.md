# gh-to-tg-bot

**gh-to-tg-bot** is a Telegram bot that automatically sends all GitHub events (such as pushes, pull requests, issues, forks, stars, and more) from a GitHub organization or repository to a specified Telegram group or channel using webhooks.

You can run the bot either using a precompiled `.exe` file (for **Windows**) or from source code (for **Linux**).

## Features

- **Real-time Notifications**: Get notified instantly about any GitHub activity in your organization (pushes, PRs, issues, forks, stars, etc.).
- **Supports All GitHub Events**: Not limited to just issues or PRs — all GitHub events are supported.
- **Telegram Integration**: Sends GitHub events directly to your Telegram group or channel.
- **Windows and Linux Support**: Easy to run with an `.exe` file on Windows or via source code on Linux.

---

## Requirements

- **Python 3.9+** (for Linux installation)
- **A GitHub Organization or Repository** with webhook configuration.
- **A Telegram Bot Token** created via [BotFather](https://core.telegram.org/bots#botfather).
- **A Telegram Group/Channel** to receive the updates.

---

## Installation

### First-Time Setup

Before running the bot for the first time, make sure you install the required dependencies:

1. If you are using the source code, install Python dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

2. Dependencies included in `requirements.txt` are:
   - `Flask`: For handling webhook requests.
   - `python-telegram-bot`: For sending messages to Telegram.
   - `python-dotenv`: For managing environment variables.

   If you don’t have the `requirements.txt` file, you can install the libraries manually:

   ```bash
   pip install Flask python-telegram-bot python-dotenv
   ```

3. For Windows users running the `.exe` file, these libraries are already bundled into the executable and no additional installation is required.

---

### For Windows: Using Precompiled `.exe` File

1. **Download the `.exe` File**  
   Download the precompiled `.exe` file from the [releases section](https://github.com/Deep-Dark-Forest/gh-to-tg-bot/releases).

2. **Set Up the Environment Variables**

   After downloading and extracting the `.exe` file, create a `.env` file in the same directory and add the following variables:

   ```bash
   BOT_TOKEN=your-telegram-bot-token
   CHAT_ID=your-telegram-chat-id
   PORT=5000
   ```

   - **BOT_TOKEN**: The Telegram Bot token you received from [BotFather](https://core.telegram.org/bots#botfather).
   - **CHAT_ID**: The chat ID of your Telegram group or channel where the messages will be sent.
   - **PORT**: The port the bot will listen on (default is `5000`).

3. **Run the `.exe` File**  
   Simply run the `.exe` file by double-clicking it. The bot will start listening for GitHub events and will send updates to the specified Telegram group/channel.

---

### For Linux: Using Source Code

If you're using Linux, follow the instructions below to run the bot from source code.

1. **Clone the repository**

   ```bash
   git clone https://github.com/Deep-Dark-Forest/gh-to-tg-bot.git
   cd gh-to-tg-bot
   ```

2. **Install dependencies**

   Install the required dependencies using:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the environment variables**

   Create a `.env` file in the root directory and add the following:

   ```bash
   BOT_TOKEN=your-telegram-bot-token
   CHAT_ID=your-telegram-chat-id
   PORT=5000
   ```

4. **Run the bot**

   Start the bot using the following command:

   ```bash
   python gh-to-tg-bot.py
   ```

---

### Configure GitHub Webhook

Configuring the webhook is the same for both **Windows** and **Linux** setups:

1. Go to your GitHub repository or organization settings.
2. Under **Settings**, navigate to **Webhooks** and click **Add webhook**.
3. Configure the following options:
   - **Payload URL**: Set this to the public URL of your server, followed by `/webhook`. For example:
     - For a deployed server: `http://your-server-url/webhook`
     - For local testing with a tool like [ngrok](https://ngrok.com/): `http://your-ngrok-url/webhook`
   - **Content type**: Choose `application/json`.
   - **Secret**: Leave empty unless you want additional security (you'll need to update the bot to verify this secret if used).
   - **Which events would you like to trigger this webhook?**: Select **Send me everything** to receive all GitHub events.
4. Click **Add webhook** to save the configuration.

---

## How It Works

### GitHub Events

The bot listens for the following GitHub events (and any future events you choose to subscribe to):

- **Push**: Triggered when commits are pushed to a repository.
- **Pull Request**: Triggered when a pull request is created, closed, or synchronized.
- **Issues**: Triggered when an issue is opened, closed, or commented on.
- **Fork**: Triggered when a repository is forked.
- **Star**: Triggered when a repository is starred.
- **Watch**: Triggered when a repository is watched.
- And many more...

### Example Notifications

#### Push Event:
```
Push event on repository my-org/my-repo:
- Fixed bug in feature X
- Added new test cases for feature Y
```

#### Pull Request Event:
```
Pull Request opened:
Fixes bug in feature X
https://github.com/my-org/my-repo/pull/1
```

#### Issue Event:
```
Issue opened:
Title: Bug in feature X
https://github.com/my-org/my-repo/issues/1
```

#### Fork Event:
```
New fork event: my-org/my-repo forked
```

#### Star Event:
```
Star event on repository my-org/my-repo
```

---
