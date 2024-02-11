# Smoczyca 2023 by PSzczepanski1996
import platform
import random

import discord
import psutil
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand

from utils import (add_message_record, delete_message_record,
                   init_file_existence, read_json_file, get_commit_version)

from consts import db_json_name


class CustomHelpCommand(DefaultHelpCommand):

    def __init__(self, **options):
        super().__init__(**options)
        self.no_category = 'General'


config = read_json_file('config.json')
desc = 'Smoczyca bot made by KenSoft.'
intents = discord.Intents.default()
intents.message_content = True
activity = discord.Game('Python Virtualenv')
client = discord.Client(
    intents=intents,
    command_prefix='!',
    activity=activity,
    description=desc,
    help_command=CustomHelpCommand(),
)
tree = app_commands.CommandTree(client)
init_file_existence(db_json_name)


@tree.command
async def on_ready():
    """Print that bot logged in as."""
    await tree.sync()
    print(f'Logged in as {bot.user.name} | ID: {bot.user.id}!')


@client.event
async def on_command_error(ctx, error):
    get_msgs = read_json_file(db_json_name)
    command = ctx.message.content
    if command in get_msgs.keys():
        await ctx.send(get_msgs[command])


@tree.command(brief='Adds and saves custom command to database')
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


@tree.command(brief='Deletes custom command from database')
async def delete(ctx, arg):
    if ctx.message.author.top_role.name not in config.get('allow_permission', []):
        await ctx.send('Incorrect permissions!')
        return
    if not delete_message_record(arg):
        await ctx.send('Nothing to delete!')
        return
    await ctx.send('Deleted command!')


@tree.command(brief='Gives general bot system information')
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


@tree.command(brief='Shows user avatar')
async def avatar(ctx):
    if ctx.message.mentions:
        mention = ctx.message.mentions[0]
        await ctx.send(mention.avatar.url)


@tree.command(brief='Estimates ping from bot server to discord')
async def ping(ctx):
    await ctx.send(f'Pong: {round(bot.latency, 7)}...')


@tree.command(brief='Dice roll')
async def choose(ctx, *args):
    if len(args) > 2:
        content = ' '.join(args)
        choose = content.split('|')
        await ctx.send(choose[random.randint(0, len(choose)-1)])
    else:
        await ctx.send('No words to choose!')

client.run(config.get('token'))
