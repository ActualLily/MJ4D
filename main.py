import os

import discord
from discord import app_commands
from dotenv import load_dotenv

import dba

load_dotenv("private.env")
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_TEST = os.getenv("GUILD_TEST")

load_dotenv("data.env")
STAGE = os.getenv("STAGE")
VERSION = os.getenv("VERSION")
BOT_ID = os.getenv("BOT_ID")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

print(f"Launching RM4D {STAGE} {VERSION}...")

messages = []

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_TEST))

    print(f"RM4D {STAGE} {VERSION} synced and running!")

@client.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == '❓':
        current_channel = client.get_channel(payload.channel_id)
        queried_message = await current_channel.fetch_message(payload.message_id)

        phraselist = dba.fetch_phrases()
        foundphrases = []

        for phrase in phraselist:
            if queried_message.content.find(phrase) >= 0:
                foundphrases.append(phrase)

        await current_channel.send("Test " + foundphrases.pop(), reference=queried_message, mention_author=False)

    if payload.emoji.name == '❌':
        current_channel = client.get_channel(payload.channel_id)
        queried_message = await current_channel.fetch_message(payload.message_id)

        if queried_message.author.id == client.application_id:
            await queried_message.delete()

client.run(TOKEN)
