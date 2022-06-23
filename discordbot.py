import discord
from discord.ext import commands
from typing import Union
from os import getenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='~', intents=intents)


def get_image_channel(channels: list) -> Union[discord.TextChannel, None]:
    for ch in channels:
        if not isinstance(ch, discord.TextChannel):
            continue
        if ch.topic is None:
            continue
        if '#images' in ch.topic:
            return ch
    return None


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    current_ch = message.channel
    channels = await message.guild.fetch_channels()
    image_channel = get_image_channel(channels)
    if image_channel is None:
        return
    if not message.attachments:
        return
    images = []
    for attachment in message.attachments:
        c_type = attachment.content_type
        if 'image' in c_type or 'video' in c_type:
            images.append(attachment)
    if len(images) == 0:
        return
    for img in images:
        image_file = await img.to_file()
        msg = await image_channel.send(file=image_file)
        description = '[メディアを表示](' + msg.jump_url + ')'
        if message.content:
            description = message.content + '\n\n' + description
        embed = discord.Embed(title="📷", description=description)
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        await message.delete()
        await current_ch.send(embed=embed)


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
