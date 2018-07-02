# Smoczyca 2018 by Hoshi, all memes reserved
from config import *
import discord, os, random
import glac
import psutil, platform
from discord.ext import commands

fTable = []
desc = "Smoczyca meme bot."
bot = commands.Bot(command_prefix="!", description=desc)

async def shitpost(ctx):
    ctx.send("Lol")

def readShitpost():
    del fTable[:]
    with open("shitpost.txt") as file:
        for line in file:
            cmd = line.split()
            fTable.append(cmd[0])

readShitpost()

@bot.event
async def on_ready():
    print("Logged in as {0} | ID: {1}!".format(bot.user.name, bot.user.id))

@bot.event
async def on_command_error(ctx, error):
    if(ctx.message.content.startswith(tuple(fTable))):
        cmdBuff = ctx.message.content.split()
        cmd = cmdBuff[0]
        index = fTable.index(cmd)
        fBuffer = open("shitpost.txt", "r")
        with fBuffer as file:
            for i, line in enumerate(file):
                if i == index:
                    cmdBuff = line.split()
                    msg = ' '.join(cmdBuff[1:])
        fBuffer.close()
        await ctx.send(msg)

@bot.command()
async def add(ctx, arg, *args):
    if(ctx.message.author.top_role.name in allow_permission):
        if arg and args:
            if(arg[0] == '!'):
                if(arg not in fTable):
                    fContent = ' '.join(args)
                    fBuffer = open("shitpost.txt", "a")
                    fBuffer.write(arg + ' ')
                    fBuffer.write(fContent + '\n')
                    await ctx.send("Added command: {:s}".format(arg))
                    fBuffer.close()
                    readShitpost()
                else:
                    await ctx.send("Command already exist!")
            else:
                await ctx.send("Command does not start with !")
        else:
            await ctx.send("No command given!")
    else:
        await ctx.send("Incorrect permission!")

@bot.command()
async def delete(ctx, arg):
    if(ctx.message.author.top_role.name in allow_permission):
        Deleted = False
        fBuffer = open("shitpost.txt", "r")
        lines = fBuffer.readlines()
        fBuffer.close()
        fBuffer = open("shitpost.txt", "w")
        with fBuffer as file:
            for line in lines:
                if not line.startswith(arg):
                    file.write(line)
                else:
                    Deleted = True
        fBuffer.close()
        if(Deleted):
            await ctx.send("Deleted command!")
            readShitpost()
        else:
            await ctx.send("Nothing to delete!")
    else:
        await ctx.send("Incorrect permissions!")

@bot.command()
async def system(ctx):
    if(ctx.message.author.top_role.name in allow_permission):
        ram = psutil.virtual_memory()
        cpu = platform.processor()
        cpu_usage = psutil.cpu_percent()
        kernel = platform.release()
        embed = discord.Embed(title="Smoczyca v2137 running on discord.py ver:", description=discord.__version__)
        embed.add_field(name="CPUInfo:", value="__Arch:__ {:s} | __Usage:__ {:d}/100".format(cpu, int(cpu_usage)), inline=False)
        embed.add_field(name="RAM:", value="__Usage__: {:d}/{:d}".format(ram.used >> 20, ram.total >> 20), inline=False)
        embed.add_field(name="Kernel:", value=kernel, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Incorrect permission!")

@bot.command()
async def glac(ctx):
    data = glac.read
    embed = discord.Embed(title="Status glacy", description="Kochajmy glacowiczów, tak szybko umierają.")
    embed.add_field(name="Anioły", value=data["angels"]["progress"], inline=False)
    embed.add_field(name="Demony", value=data["demons"]["progress"], inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx):
    if len(ctx.message.mentions) > 0:
        for user in ctx.message.mentions:
            await ctx.send(user.avatar_url)

@bot.command()
async def choose(ctx, *args):
    if(len(args) > 2):
        content = ' '.join(args)
        choose = content.split('|')
        await ctx.send(choose[random.randint(0, len(choose)-1)])
    else:
        await ctx.send("No words to choose!")

bot.run(token)