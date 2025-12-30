import os
import discord
from discord import app_commands
import google.generativeai as genai
import keep_alive 

# --- CONFIGURATION ---
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Configure Google Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Use the "Flash" model (Fastest and Free-tier eligible)
model = genai.GenerativeModel('gemini-1.5-flash')

class MyClient(discord.Client):
    def __init__(self):
        # We need message_content intent even for slash commands sometimes
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

# Helper to handle long messages (Discord limit is 2000 chars)
async def send_long_message(interaction, content):
    if len(content) <= 2000:
        await interaction.followup.send(content)
    else:
        # Split into chunks of 1900 to be safe
        chunks = [content[i:i+1900] for i in range(0, len(content), 1900)]
        for chunk in chunks:
            await interaction.followup.send(chunk)

@client.tree.command(name="ask", description="Ask the AI a question")
@app_commands.describe(question="Your question for the AI")
async def ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer(thinking=True)

    try:
        # Generate response using Gemini
        response = await
        model.generate_content_async(question)
        
        # Check if the response was blocked by safety filters
        if hasattr(response, 'text'):
            await send_long_message(interaction, response.text)
        else:
            await interaction.followup.send("I couldn't answer that due to safety guidelines.")

    except ValueError:
        await interaction.followup.send("Error: The AI response was blocked (Safety Filter).")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}")

# Start the web server to keep the bot alive
keep_alive.keep_alive()

# Run the bot
client.run(DISCORD_TOKEN)

