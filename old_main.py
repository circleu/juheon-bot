import discord
import random
import asyncio
import JuheonBotKeywords
from discord.ext import commands
from JuheonBotFunctions import *


discordBotToken = "tokenhere"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)
botChannel = None

specialCommandsData = getSpecialCommandsJson()
commandsData = getCommandsJson()


async def timer(msg, time):
	alertTime = time / 8

	await msg.author.send(f"ㅇㅋ {msg.author.mention}")
	await asyncio.sleep(time - alertTime)

	if alertTime > 60:
		await msg.author.send(f"{alertTime / 60}분 남았다")
	else:
		await msg.author.send(f"{alertTime}초 남았다")

	await asyncio.sleep(alertTime)

	for i in range(10):
		botMsg = await msg.author.send(f"{msg.author.mention}")
		await asyncio.sleep(0.25)
		await botMsg.delete()
	
	return



@bot.event
async def on_ready():
	print(bot.user.name, "준비되었습니다.")
	print("아이디는", bot.user.id, "입니다.")
	print("----------")


@bot.event
async def on_voice_state_update(member, before, after):
	global botChannel

	channel = after.channel
	vc = 0

	await asyncio.sleep(1)

	if channel:
		botChannel.play(discord.FFmpegPCMAudio("hello.ogg"), after=lambda e: print("done", e))
		return
	else:
		return


@bot.event
async def on_message(message):
	if message.author.bot:
		return

	parsedMessage = message.content.split(" ")
	preferencesData = getPreferencesJson()
	isCommand = 0
	indexTemp = 0

	for index, value in enumerate(parsedMessage, start=1):
		if matchWords(value, "주헌아") == 0:
			isCommand = 1
			indexTemp = index
			break

	if isCommand == 1:
		for index, value in enumerate(parsedMessage[indexTemp:], start=indexTemp):
			try:
				if specialCommandsData[value] == "_06":
					await bot.change_presence(status=discord.Status.offline)
					preferencesData["awake"] = 0
					putPreferencesJson(preferencesData)

					await message.reply("ㅅㅂ")
					return
				elif specialCommandsData[value] == "_07":
					await bot.change_presence(status=discord.Status.online)
					preferencesData["awake"] = 1
					putPreferencesJson(preferencesData)

					await message.reply("ㅇ")
					return
			except:
				print("")

	await bot.process_commands(message)
	return


@bot.listen()
async def on_message(message):
	preferencesData = getPreferencesJson()
	if message.author.bot:
		return
	if preferencesData["awake"] == 0:
		return

	parsedMessage = message.content.split(" ")
	parsedMessageLen = len(parsedMessage)
	userCommandsData = getUserCommandsJson()
	isCommand = 0
	indexTemp = 0

	for index, value in enumerate(parsedMessage, start=1):
		print(index, value)

		if matchWords(value, "주헌아") == 0:
			isCommand = 1
			indexTemp = index
			break
		elif findWords(JuheonBotKeywords.media, value) == 0:
			if findWords(JuheonBotKeywords.whitelist, value) == 1:
				if preferencesData["censoring"] == 1:
					await message.delete()
					return
				else:
					return

	if isCommand == 1:
		for index, value in enumerate(parsedMessage[indexTemp:], start=indexTemp):
			try:
				if specialCommandsData[value] == "_00":
					continue
				elif specialCommandsData[value] == "_01":
					addKey = parsedMessage[index+1]
					addValue = ""

					for i in range(index+2, parsedMessageLen):
						if matchWords(parsedMessage[i][-1], ["임", "야"]) == 0:
							addValue += parsedMessage[i][:-1]
							addValue = [addValue, message.author.id]

							for key in list(userCommandsData.keys()):
								if matchWords(addValue, userCommandsData[key]) == 0:
									await message.reply("있던거잖아 병신아")
									return

							try:
								userCommandsData[addKey].append(addValue)
							except:
								userCommandsData[addKey] = [addValue]

							putUserCommandsJson(userCommandsData)

							await message.reply("ㅇㅇ")
							return
						else:
							addValue += parsedMessage[i] + " "
				elif specialCommandsData[value] == "_02":
					for key in list(userCommandsData.keys()):
						for i, answer in enumerate(userCommandsData[key]):
							if answer[1] == message.author.id:
								del userCommandsData[key][i]

					putUserCommandsJson(userCommandsData)

					await message.reply("리셋함")
					return
				elif specialCommandsData[value] == "_03":
					await message.reply(JuheonBotKeywords.guide)
					return
				elif specialCommandsData[value] == "_04":
					if preferencesData["censoring"] == 0:
						preferencesData["censoring"] = 1
						putPreferencesJson(preferencesData)

						await message.reply("켰음")
						return
					elif preferencesData["censoring"] == 1:
						preferencesData["censoring"] = 0
						putPreferencesJson(preferencesData)

						await message.reply("껐음")
						return
				elif specialCommandsData[value] == "_05":
					answer = ["ㅇ", "ㄴ"]

					await message.reply(random.choice(answer))
					return
				elif specialCommandsData[value] == "_06":
					continue
				elif specialCommandsData[value] == "_07":
					continue
				elif specialCommandsData[value] == "_08":
					if matchWords(parsedMessage[index+1][-1], ["초", "분"]) == 0:
						time = float(parsedMessage[index+1][:-1])
						
						if parsedMessage[index+1][-1] == "분":
							time *= 60
						
						if time > 0:
							await timer(message, time)
							return
			except:
				if matchWords(value, list(commandsData.keys())) == 0:
					await message.reply(random.choice(commandsData[value]))
					return
				elif matchWords(value, list(userCommandsData.keys())) == 0:
					try:
						if matchWords(parsedMessage[index+1], ["목록"]) == 0:
							commandList = []

							for i in userCommandsData[value]:
								commandList.append(i[0])
							
							await message.reply(", ".join(commandList))
							return
						elif matchWords(parsedMessage[index+2], ["지워"]) == 0:
							answer = parsedMessage[index+1]

							for i, j in enumerate(userCommandsData[value]):
								if answer == j[0]:
									del userCommandsData[value][i]
									putUserCommandsJson(userCommandsData)
									await message.reply("ㅇㅇ")
									
									return
					except:
						await message.reply(random.choice(userCommandsData[value])[0])
						return
			await message.reply("뭐라는거야 병신아")
			return
	else:
		return
	

@bot.listen()
async def on_message(message):
	preferencesData = getPreferencesJson()
	if message.author.bot:
		return
	if preferencesData["awake"] == 0:
		return

	chance = random.randint(1, 100)
	wait = 0

	if wait == 0:
		if chance >= 97:
			print("Sending miku gif...")
			wait = 1
			await asyncio.sleep(2.5)
			wait = 0
			await message.reply(random.choice(JuheonBotKeywords.miku), mention_author=False)

	return


@bot.command(aliases=["들어와"])
async def _join(ctx):
	preferencesData = getPreferencesJson()
	if preferencesData["awake"] == 0:
		return

	global botChannel

	try:
		channel = ctx.author.voice.channel
		print(channel)
		vc = await channel.connect()
		botChannel = vc
		vc.play(discord.FFmpegPCMAudio("hello.ogg"), after=lambda e: print("done", e))
		return
	except:
		await ctx.reply("https://tenor.com/view/hatsune-miku-miku-angry-gif-22557182")
		return
	

@bot.command(aliases=["꺼져", "나가"])
async def _leave(ctx):
	preferencesData = getPreferencesJson()
	if preferencesData["awake"] == 0:
		return
	
	try:
		await ctx.voice_client.disconnect()
		return
	except:
		await ctx.reply("느금")
		return


bot.run(discordBotToken)