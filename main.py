# Enjoy the product.

import discord
from discord.ext import commands
from characterai import PyCAI
import asyncio

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

client = PyCAI('CAI TOKEN')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def start_conversation(ctx, char_id: str):
    chat = client.chat.get_chat(char_id)

    participants = chat['participants']

    if not participants[0]['is_human']:
        tgt = participants[0]['user']['username']
    else:
        tgt = participants[1]['user']['username']

    await ctx.send('Start Talking')

    while True:
        try:
            reply = await bot.wait_for('message', timeout=300, check=lambda m: m.author == ctx.author)
            text = reply.content

            data = client.chat.send_message(chat['external_id'], tgt, text)

            name = data['src_char']['participant']['name']
            text = data['replies'][0]['text']

            await ctx.send(f"{name}: {text}")

        except asyncio.TimeoutError:
            await ctx.send('Conversation timed out.')
            break

bot.run('DISCORD TOKEN')
