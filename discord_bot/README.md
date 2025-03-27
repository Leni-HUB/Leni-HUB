# Discord Bot

A simple Discord bot built with discord.py that can respond to commands.

## Setup

1. Create a Discord Application and Bot:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name
   - Go to the "Bot" section and click "Add Bot"
   - Copy your bot token

2. Configure the bot:
   - Paste your bot token in the `.env` file:
     ```
     DISCORD_TOKEN=your_token_here
     ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the bot:
   ```
   python bot.py
   ```

## Commands

- `!hello` - Bot responds with a greeting
- `!ping` - Check bot's latency

## Adding the Bot to Your Server

1. Go to your application in the Discord Developer Portal
2. Go to OAuth2 > URL Generator
3. Select the following scopes:
   - bot
   - applications.commands
4. Select bot permissions:
   - Send Messages
   - Read Messages/View Channels
5. Copy and open the generated URL
6. Select your server and authorize the bot
