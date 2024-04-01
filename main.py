import discord
import asyncio
import random
import JuheonBotKeywords
from discord.ext import commands
from JuheonBotFunctions import *


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)
botToken = "yourtokenhere"
botChannel = None

specialCommandsData = getSpecialCommandsJson()
commandsData = getCommandsJson()


async def timer(message, time):
    alertTime = time / 8

    await message.author.send(f"ㅇㅋ {message.author.mention}")
    await asyncio.sleep(time - alertTime)

    if alertTime > 60:
        await message.author.send(f"{alertTime / 60}분 남았다")
    else:
        await message.author.send(f"{alertTime}초 남았다")

    await asyncio.sleep(alertTime)

    for i in range(10):
        alert = await message.author.send(f"{message.author.mention}")
        await asyncio.sleep(0.25)
        await alert.delete()

    return

async def commandError(message):
    await message.reply("뭐라는거야 병신아")
    return


@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready.")
    print(f"id is {bot.user.id}.")
    print("----------------")


@bot.event
async def on_voice_state_update(member, before, after):
    global botChannel
    channel = after.channel

    await asyncio.sleep(1)

    if channel:
        botChannel.play(discord.FFmpegPCMAudio("hello.ogg"))
    
    return

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    parsedMessage = message.content.split(" ")
    preferencesData = getPreferencesJson()
    isCommand = False
    commandIndex = None

    for index, value in enumerate(parsedMessage, start=1):
        if matchWords(value, "주헌아"):
            isCommand = True
            commandIndex = index
            break
    
    if isCommand:
        try:
            command = parsedMessage[commandIndex:]

            if specialCommandsData[command[0]] == 6:
                await bot.change_presence(status=discord.Status.offline)

                preferencesData["awake"] = False
                putPreferencesJson(preferencesData)

                await message.reply("ㅅㅂ")
                return
            elif specialCommandsData[command[0]] == 7:
                await bot.change_presence(status=discord.Status.online)

                preferencesData["awake"] = True
                putPreferencesJson(preferencesData)

                await message.reply("ㅇ")
                return
        except KeyError:
            print("")
        except IndexError:
            await commandError(message)
            return
        
    await bot.process_commands(message)
    return

@bot.listen()
async def on_message(message):
    preferencesData = getPreferencesJson()
    if message.author.bot:
        return
    if not preferencesData["awake"]:
        return
    
    parsedMessage = message.content.split(" ")
    userCommandsData = getUserCommandsJson()
    isCommand = False
    commandIndex = None

    for index, value in enumerate(parsedMessage, start=1):
        if matchWords(value, "주헌아"):
            isCommand = True
            commandIndex = index
            break
        elif findWords(JuheonBotKeywords.media, value):
            if not findWords(JuheonBotKeywords.whitelist, value):
                if preferencesData["censoring"]:
                    await message.delete()
                
                return
    
    if isCommand:
        try:
            command = parsedMessage[commandIndex:]

            if specialCommandsData[command[0]] == 1:
                key = command[1]
                value = ""

                if matchWords(command[-1][-1], ["임", "야"]):
                    value += " ".join(command[2:])
                    value = [value[:-1], message.author.id]

                    for i in list(userCommandsData.keys()):
                        if matchWords(value[0], userCommandsData[i]):
                            await message.reply("있던거잖아 병신아")
                            return
                    
                    if matchWords(key, list(userCommandsData.keys())):
                        userCommandsData[key].append(value)
                    else:
                        userCommandsData[key] = [value]

                    putUserCommandsJson(userCommandsData)

                    await message.reply("ㅇㅇ")
                    return
            elif specialCommandsData[command[0]] == 3:
                await message.reply(JuheonBotKeywords.guide)
                return
            elif specialCommandsData[command[0]] == 4:
                if not preferencesData["censoring"]:
                    preferencesData["censoring"] = True
                    putPreferencesJson(preferencesData)

                    await message.reply("켰음")
                    return
                elif preferencesData["censoring"]:
                    preferencesData["censoring"] = False
                    putPreferencesJson(preferencesData)

                    await message.reply("껐음")
                    return
            elif specialCommandsData[command[0]] == 5:
                answer = ["ㅇ", "ㄴ"]

                await message.reply(random.choice(answer))
                return
            elif specialCommandsData[command[0]] == 8:
                if matchWords(command[1][-1], ["초", "분"]):
                    time = float(command[1][:-1])
                    
                    if command[1][-1] == "분":
                        time *= 60
                    
                    if time > 0:
                        await timer(message, time)
                        return
                else:
                    await commandError(message)
                    return
        except KeyError:
            if matchWords(command[0], list(commandsData.keys())):
                    await message.reply(random.choice(commandsData[command[0]]))
                    return
            elif matchWords(command[0], list(userCommandsData.keys())):
                try:
                    if matchWords(command[1], ["목록"]):
                        commandList = []

                        for i in userCommandsData[command[0]]:
                            commandList.append(i[0])
                        
                        await message.reply(", ".join(commandList))
                        return
                    elif matchWords(command[-1], ["지워"]):
                        answer += " ".join(command[1:-1])

                        for i, j in enumerate(userCommandsData[command[0]]):
                            if answer == j[0]:
                                del userCommandsData[command[0]][i]
                                putUserCommandsJson(userCommandsData)

                                await message.reply("ㅇㅇ")
                                return
                    else:
                        await commandError(message)
                except IndexError:
                    await message.reply(random.choice(userCommandsData[command[0]])[0])
                    return
        except IndexError:
            await commandError(message)
            return

    return


@bot.listen()
async def on_message(message):
	preferencesData = getPreferencesJson()
	if message.author.bot:
		return
	if not preferencesData["awake"]:
		return

	chance = random.randint(1, 100)
	wait = 0

	if wait == 0:
		if chance >= 98:
			print("Sending miku gif...")
			wait = 1
			await asyncio.sleep(3)
			wait = 0
			await message.reply(random.choice(JuheonBotKeywords.miku), mention_author=False)

	return


@bot.command(aliases=["들어와"])
async def _join(ctx):
	preferencesData = getPreferencesJson()
	if not preferencesData["awake"]:
		return

	global botChannel

	try:
		channel = ctx.author.voice.channel
		vc = await channel.connect()
		botChannel = vc
		vc.play(discord.FFmpegPCMAudio("hello.ogg"))
		return
	except:
		await ctx.reply("https://tenor.com/view/hatsune-miku-miku-angry-gif-22557182")
		return
	

@bot.command(aliases=["꺼져", "나가"])
async def _leave(ctx):
	preferencesData = getPreferencesJson()
	if not preferencesData["awake"]:
		return
	
	try:
		await ctx.voice_client.disconnect()
		return
	except:
		await ctx.reply("느금")
		return


bot.run(botToken)