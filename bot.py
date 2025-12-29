import os
import discord
import openai

# Get tokens from environment variables
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Set intents (required for reading messages)
intents = discord.Intents.default()
intents.message_content = True  # Privileged intent must be enabled in Discord Developer Portal
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')  # Confirms bot is online

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages from the bot itself

    if message.content.startswith("!ask"):
        prompt = message.content[len("!ask "):].strip()
        if not prompt:
            await message.channel.send("Please type a question after !ask.")
            return

        await message.channel.send("🤖 Thinking...")
        try:
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response['choices'][0]['message']['content']
            await message.channel.send(answer)
        except Exception as e:
            await message.channel.send(f"Error: {e}")

# Run the bot
client.run(DISCORD_TOKEN)
