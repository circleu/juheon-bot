import json

def getSpecialCommandsJson():
	with open("specialcommands.json", "r", encoding="utf-8") as specialCommandsJson:
		specialCommandsData = json.load(specialCommandsJson)
	return specialCommandsData
def getCommandsJson():
	with open("commands.json", "r", encoding="utf-8") as commandsJson:
		commandsData = json.load(commandsJson)
	return commandsData
def getUserCommandsJson():
	with open("usercommands.json", "r", encoding="utf-8") as userCommandsJson:
		userCommandsData = json.load(userCommandsJson)
	return userCommandsData

def getPreferencesJson():
	with open("preferences.json", "r", encoding="utf-8") as preferencesJson:
		preferencesData = json.load(preferencesJson)
	return preferencesData

def putSpecialCommandsJson(dic):
	with open("specialcommands.json", "w    ", encoding="utf-8") as specialCommandsJson:
		specialCommandsOut = json.dumps(dic, indent="\t", sort_keys=True, ensure_ascii=False)
		print(specialCommandsOut, file=specialCommandsJson)
	return
def putUserCommandsJson(dic):
	with open("usercommands.json", "w", encoding="utf-8") as userCommandsJson:
		userCommandsOut = json.dumps(dic, indent="\t", sort_keys=True, ensure_ascii=False)
		print(userCommandsOut, file=userCommandsJson)
	return

def putPreferencesJson(dic):
	with open("preferences.json", "w", encoding="utf-8") as preferencesJson:
		preferencesOut = json.dumps(dic, indent="\t", sort_keys=True, ensure_ascii=False)
		print(preferencesOut, file=preferencesJson)
	return


def matchWords(words1, words2):
	if not isinstance(words1, list):
		words1 = [words1]
	if not isinstance(words2, list):
		words2 = [words2]

	for word1 in words1:
		for word2 in words2:
			if word1 == word2:
				return 0

	return 1

def findWords(words1, words2):
	if not isinstance(words1, list):
		words1 = [words1]
	if not isinstance(words2, list):
		words2 = [words2]

	for word1 in words1:
		for word2 in words2:
			if word1 in word2:
				return 0

	return 1
