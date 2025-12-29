import discord
import openai

# --------------------
# Add your keys here
# --------------------
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

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

