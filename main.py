import os

import discord
from discord import app_commands
from dotenv import load_dotenv

import dba
import emojis

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

def base_embed() -> discord.Embed:
    embed = discord.Embed(color=0xeca333)
    embed.set_footer(text="To delete this message, react with `❌`!")
    embed.set_author(name=client.user.name,
                     icon_url=client.user.display_avatar.url)

    return embed

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_TEST))

    print(f"RM4D {STAGE} {VERSION} synced and running!")

@client.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == '❓':
        current_channel = client.get_channel(payload.channel_id)
        queried_message = await current_channel.fetch_message(payload.message_id)

        if queried_message.author.id != client.application_id:

            phraselist = dba.fetch_phrases()
            phrasecount = 0

            embed = base_embed()

            for phrase in phraselist:
                if queried_message.content.lower().find(phrase) >= 0:
                    text = dba.connect()['info'].find_one(phrase=phrase)['simple']

                    for key in emojis.EMOJIS.keys():
                        text = text.replace(key, emojis.EMOJIS[key])

                    embed.add_field(name=phrase, value=text, inline=False)
                    phrasecount += 1

            embed.title = f"Found {phrasecount}..."

            if phrasecount == 0:
                embed.description = "**No phrases to iterate on found.**\n" \
                               "If you believe there is a phrase to be added, please contact `Leah#0004`."

            await current_channel.send(embed=embed, reference=queried_message, mention_author=False)

    if payload.emoji.name == '❌':
        current_channel = client.get_channel(payload.channel_id)
        queried_message = await current_channel.fetch_message(payload.message_id)

        if queried_message.author.id == client.application_id:
            await queried_message.delete()

client.run(TOKEN)
