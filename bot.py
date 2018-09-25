#-*- -*- -*- -*- -*- -*- -*- -*- coding:UTF-8 -*- -*- -*- -*- -*- -*- -*- -*- -
import json
import discord
import requests
from random import randint,choice
#-*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*

def getStageInfo(index=0):
	'''ステージ情報'''
	links = (
				'gachi/now','gachi/next',
				'league/now','leage/next',
				'regular/now','regular/next',
				'/schedule'
			)

	headers = {"User-Agent": "IKSbot/1.0(twitter @ikayomech)"}

	#now or next
	url = "https://spla2.yuu26.com/" + links[index]
	response = requests.get(url,headers=headers)

	#response.json => response.dict
	dic = json.loads(response.text)
	dic = dic['result'][0]

	if index < 5:
		return '**{}**で__{}__と__{}__だぞ'.format(dic['rule'],dic['maps'][0],dic['maps'][1])
	else:
		return '次のガチマは__{}__で、リグマは__{}__だ'.format(dic['result'][2]['gachi'][0]['rule'],dic['result'][3]['league'][0]['rule'])

def randBuki(buki_list, users):
	len_u = len(users)
	return {i:choice(buki_list) for i in users}

#clientオブジェクトの生成
client = discord.Client()
#channel_l = discord.utils.get(client.channels, name=x_y, type=ChannelType.voice)
with open('buki.csv', encoding='UTF-8') as f:
	buki_list = f.readlines()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	await client.change_presence(game=discord.Game(name="Splatoon2"))
	print('------')

@client.event
async def on_message(message):
    voice_channel = discord.utils.get(message.server.channels, id=message.author.voice.voice_channel.id)
    p_list = voice_channel.voice_members

    for x in range(len(p_list)):
        print(p_list[x].display_name)

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

	'''ランダム武器'''
	#"!random_buki"とチャットに入力があった場合反応
	if message.content.startswith('random_buki'):
		voice_channel = discord.utils.get(message.server.channels, id=message.author.voice.voice_channel.id)
		p_list = voice_channel.voice_members
		voice_users= [ p_list[i].display_name for i in range(len(p_list))]
		rand_buki = randBuki(buki_list,voice_users)
		for i in rand_buki.keys():
			m = '{}:{}'.format(i,rand_buki[i])
			await client.send_message(message.channel, m)

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

	if message.content.startswith("サイコロ"):
		saikoro = ['1','2','3','4','5','6']
		saikoro_choice = choice(saikoro)
		if client.user != message.author:
			# メッセージを書きます
			m = saikoro_choice
			await client.send_message(message.channel, '{}{}'.format(m,message.author.mention))

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
"""
if __name__ == '__mian__':
	main()
"""
