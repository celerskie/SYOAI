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

# --- AUTO-DETECT MODEL ---
def get_working_model():
    """Finds the first available model that supports text generation."""
    print("Searching for available Gemini models...")
    try:
        # Ask Google which models are available for this API Key
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Prefer the Flash model if available (faster/free-tier friendly)
                if 'flash' in m.name:
                    print(f"Auto-selected model: {m.name}")
                    return genai.GenerativeModel(m.name)
        
        # If no Flash model, take the first available one (usually gemini-pro)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Auto-selected model: {m.name}")
                return genai.GenerativeModel(m.name)
                
    except Exception as e:
        print(f"Error finding models: {e}")
    
    # Fallback if auto-detect fails
    print("Auto-detect failed. Trying standard 'gemini-1.5-flash'...")
    return genai.GenerativeModel('gemini-1.5-flash')

# Initialize the model automatically
model = get_working_model()

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
        # Generate response using the auto-selected model
        response = await model.generate_content_async(question)
        
        if hasattr(response, 'text'):
            await send_long_message(interaction, response.text)
        else:
            await interaction.followup.send("I couldn't answer that due to safety guidelines.")

    except ValueError:
        await interaction.followup.send("Error: The AI response was blocked (Safety Filter).")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}")

keep_alive.keep_alive()
client.run(DISCORD_TOKEN
