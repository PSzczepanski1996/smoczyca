# Smoczyca 2020 by Hoshi Yemazaki, all memes reserved
import platform
import random

import discord
import psutil
from discord.ext import commands

import glac_lib
from json_utils import (add_shitpost_record, delete_shitpost_record,
                        init_file_existence, read_json_file)

config = read_json_file('config.json')
desc = 'Smoczyca meme bot.'
bot = commands.Bot(command_prefix="!", description=desc)
init_file_existence('shitpost.json')


@bot.event
async def on_ready():
    """Print that bot logged in as."""
    print(f'Logged in as {bot.user.name} | ID: {bot.user.id}!')


@bot.event
async def on_command_error(ctx, error):
    shitpost = read_json_file('shitpost.json')
    command = ctx.message.content
    if command in shitpost.keys():
        await ctx.send(shitpost[command])


@bot.command()
async def add(ctx, arg, *args):
    if ctx.message.author.top_role.name in config.get('allow_permission', []):
        if args and arg[0] == '!':
            shitpost_keys = read_json_file('shitpost.json').get('shitpost', {}).keys()
            if arg not in shitpost_keys:
                add_shitpost_record(arg, ' '.join(args))
                await ctx.send(f'Added command: {arg}')
            else:
                await ctx.send('Command already exist!')
        else:
            await ctx.send('Command does not start with ! or either does not have content.')
    else:
        await ctx.send('Incorrect permission!')


@bot.command()
async def delete(ctx, arg):
    if ctx.message.author.top_role.name in config.get('allow_permission', []):
        if delete_shitpost_record(arg):
            await ctx.send("Deleted command!")
        else:
            await ctx.send("Nothing to delete!")
    else:
        await ctx.send("Incorrect permissions!")


@bot.command()
async def system(ctx):
    if ctx.message.author.top_role.name in config.get('allow_permission', []):
        ram = psutil.virtual_memory()
        cpu = platform.processor()
        cpu_usage = psutil.cpu_percent()
        kernel = platform.release()
        ram_used = ram.used >> 20
        ram_total = ram.total >> 20
        embed = discord.Embed(
            title="Smoczyca v2137 running on discord.py ver:", description=discord.__version__)
        embed.add_field(
            name='CPUInfo:', value=f'__Arch:__ {cpu} | __Usage:__ {cpu_usage}/100', inline=False)
        embed.add_field(
            name='RAM:', value=f'__Usage__: {ram_used}/{ram_total}', inline=False)
        embed.add_field(name='Kernel:', value=kernel, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Incorrect permission!")


@bot.command()
async def glac(ctx, arg='s1'):
    data = glac_lib.read(arg)
    if data is not None:
        embed = discord.Embed(
            title='Status glacy [DEPRECATED AT 15.03.2020]',
            description=f'[{arg}] Kochajmy glacowiczów, tak szybko umierają.'
        )
        embed.add_field(name="Anioły", value=data["angels"]["progress"], inline=False)
        embed.add_field(name="Demony", value=data["demons"]["progress"], inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send('Server not found!')


@bot.command()
async def avatar(ctx):
    if ctx.message.mentions:
        for user in ctx.message.mentions:
            await ctx.send(user.avatar_url)


@bot.command()
async def choose(ctx, *args):
    if len(args) > 2:
        content = ' '.join(args)
        choose = content.split('|')
        await ctx.send(choose[random.randint(0, len(choose)-1)])
    else:
        await ctx.send('No words to choose!')

bot.run(config.get('token'))
