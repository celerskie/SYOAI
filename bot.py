import os
import discord
from discord import app_commands
from openai import OpenAI
import keep_alive 

# --- HARDCODE MODE (FOR DEBUGGING) ---
# Replace the text inside the quotes with your real, long Discord Token.
# keep the quote marks "" around it!
DISCORD_TOKEN = "MTQ1NTI5MzEyODg3Njc1MjkxNg.GBTk3f.18G35TL_wACOujDDMD3DSM9maIecGKlPq9dXqk"

# We can keep OpenAI as an environment variable (since that part wasn't failing)
# If this also fails later, we can hardcode it too.
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Initialize OpenAI
client_ai = OpenAI(api_key=OPENAI_API_KEY)

class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("Slash commands synced")

client = MyClient()

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")

# Helper to handle long messages
async def send_long_message(interaction, content):
    if len(content) <= 2000:
        await interaction.followup.send(content)
    else:
        chunks = [content[i:i+1900] for i in range(0, len(content), 1900)]
        for chunk in chunks:
            await interaction.followup.send(chunk)

@client.tree.command(name="ask", description="Ask the AI a question")
@app_commands.describe(question="Your question for the AI")
async def ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer(thinking=True)

    try:
        response = client_ai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": question}]
        )
        reply = response.choices[0].message.content
        await send_long_message(interaction, reply)

    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

# Start the Web Server
keep_alive.keep_alive()

# Run the Bot
client.run(DISCORD_TOKEN)
