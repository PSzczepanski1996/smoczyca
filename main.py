# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord, os
import glac, config
import psutil, platform

client = discord.Client()
fTable = []
allow_permission = ["Szef", "Schizol", "Zastępca"]

def readShitpost():
    del fTable[:]
    with open("shitpost.txt") as file:
        for line in file:
            cmd = line.split(" ")
            fTable.append(cmd[0])

readShitpost()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith(tuple(fTable)):
        cmdBuff = message.content.split(" ")
        cmd = cmdBuff[0]
        index = fTable.index(cmd)
        fBuffer = open("shitpost.txt", "r")
        with fBuffer as file:
            for i, line in enumerate(file):
                if i == index:
                    cmdBuff = line.split(" ")
                    msg = ' '.join(cmdBuff[1:])
        fBuffer.close()
        await client.send_message(message.channel, msg)

    if message.content.startswith('!add'):
        if(message.author.top_role.name in allow_permission):
            msg = message.content.split(" ")
            if(len(msg) > 2):
                fContent = ' '.join(msg[1:])
                fBuffer = open("shitpost.txt", "a")
                fBuffer.write(fContent + '\n')
                await client.send_message(message.channel, ("Added command: {:s}".format(msg[1])))
                fBuffer.close()
                readShitpost()
            else:
                await client.send_message(message.channel, "Three or more words needed!")
        else:
            await client.send_message(message.channel, "Incorrect permission!")

    if message.content.startswith('!delete'):
        if(message.author.top_role.name in allow_permission):
            cmdBuff = message.content.split(" ")
            cmd = cmdBuff[1]
            fBuffer = open("shitpost.txt", "r")
            lines = fBuffer.readlines()
            fBuffer.close()
            fBuffer = open("shitpost.txt", "w")
            with fBuffer as file:
                for line in lines:
                    if not line.startswith(cmd):
                        file.write(line)
            fBuffer.close()
            await client.send_message(message.channel, ("Deleted command!"))
            readShitpost()
        else:
            await client.send_message(message.channel, "Inorrect permission!")

    if message.content.startswith('!system'):
        if(message.author.top_role.name in allow_permission):
            ram = psutil.virtual_memory()
            cpu = platform.processor()
            cpu_usage = psutil.cpu_percent()
            kernel = platform.release()
            embed = discord.Embed(title="Smoczyca v2137 running on django.py ver:", description=discord.__version__)
            embed.add_field(name="CPUInfo:", value="__Arch:__ {:s} | __Usage:__ {:d}/100".format(cpu, int(cpu_usage)), inline=False)
            embed.add_field(name="RAM:", value="__Usage__: {:d}/{:d}".format(ram.used >> 20, ram.total >> 20), inline=False)
            embed.add_field(name="Kernel:", value=kernel, inline=False)
            await client.send_message(message.channel, embed=embed)
        else:
            await client.send_message(message.channel, "Inorrect permission!")

    if message.content.startswith('!glac'):
        data = glac.read()
        embed = discord.Embed(title="Status glacy", description="Kochajmy glacowiczów, tak szybko umierają.")
        embed.add_field(name="Anioły", value=data["angels"]["progress"], inline=False)
        embed.add_field(name="Demony", value=data["demons"]["progress"], inline=False)
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith('!avatar'):
        if len(message.mentions) > 0:
            for user in message.mentions:
                msg = user.avatar_url
                await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print("Logged in as {:s} as ID: {:s}".format(client.user.name, client.user.id))
    print('------')

client.run(config.returnToken())
