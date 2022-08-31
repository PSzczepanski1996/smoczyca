# Smoczyca 2022 by PSzczepanski1996
import platform
import random

import discord
import psutil
from discord.ext import commands

from utils import (add_message_record, delete_message_record,
                   init_file_existence, read_json_file, get_commit_version)

from consts import db_json_name

config = read_json_file('config.json')
desc = 'Smoczyca bot made by KenSoft.'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    intents=intents,
    command_prefix='!',
    description=desc,
)
init_file_existence(db_json_name)


@bot.event
async def on_ready():
    """Print that bot logged in as."""
    print(f'Logged in as {bot.user.name} | ID: {bot.user.id}!')


@bot.event
async def on_command_error(ctx, error):
    get_msgs = read_json_file(db_json_name)
    command = ctx.message.content
    if command in get_msgs.keys():
        await ctx.send(get_msgs[command])


@bot.command()
async def add(ctx, arg, *args):
    if ctx.message.author.top_role.name not in config.get('allow_permission', []):
        await ctx.send('Incorrect permission!')
        return
    if not args or arg[0] != '!':
        await ctx.send('Command does not start with ! or either does not have content.')
        return
    msg_keys = read_json_file(db_json_name).keys()
    if arg in msg_keys:
        await ctx.send('Command already exist!')
        return
    add_message_record(arg, ' '.join(args))
    await ctx.send(f'Added command: {arg}')


@bot.command()
async def delete(ctx, arg):
    if ctx.message.author.top_role.name not in config.get('allow_permission', []):
        await ctx.send('Incorrect permissions!')
        return
    if not delete_message_record(arg):
        await ctx.send('Nothing to delete!')
        return
    await ctx.send('Deleted command!')


@bot.command()
async def system(ctx):
    if ctx.message.author.top_role.name in config.get('allow_permission', []):
        ram = psutil.virtual_memory()
        cpu = platform.processor()
        cpu_usage = psutil.cpu_percent()
        kernel = platform.release()
        ram_used = ram.used >> 20
        ram_total = ram.total >> 20
        hash_ver = get_commit_version()
        embed = discord.Embed(
            title=f'Smoczyca [#{hash_ver}] running on discord.py ver:', description=discord.__version__)
        embed.add_field(
            name='CPUInfo:', value=f'__Arch:__ {cpu} | __Usage:__ {cpu_usage}/100', inline=False)
        embed.add_field(
            name='RAM:', value=f'__Usage__: {ram_used}/{ram_total}', inline=False)
        embed.add_field(name='Kernel:', value=kernel, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send('Incorrect permission!')


@bot.command()
async def avatar(ctx):
    if ctx.message.mentions:
        mention = ctx.message.mentions[0]
        await ctx.send(mention.avatar.url)


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong: {round(bot.latency, 7)}...')


@bot.command()
async def choose(ctx, *args):
    if len(args) > 2:
        content = ' '.join(args)
        choose = content.split('|')
        await ctx.send(choose[random.randint(0, len(choose)-1)])
    else:
        await ctx.send('No words to choose!')

bot.run(config.get('token'))
