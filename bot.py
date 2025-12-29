import os
import discord
from openai import OpenAI

# Environment variables
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# OpenAI client (NEW API)
client_ai = OpenAI(api_key=OPENAI_API_KEY)

# Discord intents
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!ask"):
        prompt = message.content[5:].strip()
        if not prompt:
            await message.channel.send("Please type a question after !ask.")
            return

        await message.channel.send("🤖 Thinking...")

        try:
            response = client_ai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            reply = response.choices[0].message.content
            await message.channel.send(reply)

        except Exception as e:
            await message.channel.send(f"Error: {e}")

client.run(DISCORD_TOKEN)
