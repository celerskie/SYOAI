import discord
import openai

# --------------------
# Add your keys here
# --------------------
DISCORD_TOKEN = "MTQ1NTI5MzEyODg3Njc1MjkxNg.Gv8tmd.2QbqKtOD8jrK6E6eOTDXmM35tGiB8pKOC79EuA"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# --------------------
# Bot events
# --------------------
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!ask"):
        prompt = message.content[len("!ask "):]
        await message.channel.send("🤖 Thinking...")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response['choices'][0]['message']['content']
            await message.channel.send(answer)
        except Exception as e:
            await message.channel.send(f"Error: {e}")

# --------------------
# Run the bot
# --------------------

client.run(DISCORD_TOKEN)

