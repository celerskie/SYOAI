import os
import discord
from discord import app_commands
from openai import OpenAI

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

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
    print(f"Logged in as {client.user}")

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
        await interaction.followup.send(reply)

    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

client.run(DISCORD_TOKEN)
