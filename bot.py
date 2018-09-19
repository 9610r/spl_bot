import requests
import json
import discord

def getStageInfo(index=0):
	'''
		ステージ情報
	'''
	links = ('gachi/now','gachi/next','league/now','leage/next','regular/now','regular/next','/schedule')
	headers = {"User-Agent": "IKSbot/1.0(twitter @ikayomech)"}
	#gachi/now or gachi/next
	url = "https://spla2.yuu26.com/" + links[index]
	response = requests.get(url,headers=headers)
	#response.json => response.dict
	dic = json.loads(response.text)
	dic = dic['result'][0]
	#num = [0,1,2,3,4,5]
	if 5 > index:
		return '**{}**で__{}__と__{}__だぞ'.format(dic['rule'],dic['maps'][0],dic['maps'][1])
	else:
		return "次のガチマは__{}__で、リグマは__{}__だ".format(dic['result'][2]['gachi'][0]['rule'],dic['result'][3]['league'][0]['rule'])
#clientオブジェクトの生成
client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

#チャンネルの呼び出し
#	if client.user.id in message.content:
#		await client.send_message(message.channel, '{} 呼んだ？'.format(message.author.mention))

@client.event
async def on_message(message):

	if message.content[0] == '!':
		boturl = "https://chatbot-api.userlocal.jp/api/chat?message=" + message.content + "&key=f2ff5ccc7af428543654"
		headers = {"content-type": "application/json"}
		r = requests.get(boturl, headers=headers)
		data = r.json()
		reply=data["result"]

		if client.user != message.author:
			await client.send_message(message.channel, reply)

	if message.content.startswith('おはよう'):
		# 送り主がBotだった場合反応しない
		if client.user != message.author:
			m = "おはよう、" + message.author.name + "！"
			# メッセージが送られてきたチャンネルへメッセージ送信
			await client.send_message(message.channel, m)

	if message.content.startswith("司令"):
		# 送り主がBotだった場合反応したくないので
		if client.user != message.author:
			# メッセージを書きます
			m = "なんだ、" + message.author.name +"!"
			await client.send_message(message.channel, m)

	if client.user.id in message.content:
		await client.send_message(message.channel, '{} 呼んだか？'.format(message.author.mention))

	if message.content.startswith('ガチマ'):
		m = getStageInfo(0)
		await client.send_message(message.channel, m)

	if message.content.startswith("次のガチマ"):
		m = getStageInfo(1)
		await client.send_message(message.channel, m)

	if message.content.startswith("リグマ"):
		m = getStageInfo(2)
		await client.send_message(message.channel, m)

	if message.content.startswith("次のリグマ"):
		m = getStageInfo(3)
		await client.send_message(message.channel, m)

	if message.content.startswith("ナワバリ"):
		m = getStageInfo(4)
		await client.send_message(message.channel, m)

	if message.content.startswith("次のナワバリ"):
		m = getStageInfo(5)
		await client.send_message(message.channel, m)

	if message.content.startswith("次のルール"):
		m = getStageInfo(6)
		await client.send_message(message.channel, m)



client.run("NDY3MTgxMTU3ODcyNjk3MzQ0.Dim34w.6vRlS-LHG9VPmQgTJany1DpoSck")
