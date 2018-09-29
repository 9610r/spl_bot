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
				'league/now','league/next',
				'regular/now','regular/next',
				'schedule'
			)

	headers = {"User-Agent": "IKSbot/1.0(twitter @ikayomech)"}

	#now or next
	url = "https://spla2.yuu26.com/" + links[index]
	response = requests.get(url,headers=headers)
	dic = json.loads(response.text)
	dic = dic['result'][0]

	if index < 2:
		msg = discord.Embed(title='ガチマッチ',colour=0xfbb31c)
		msg.set_thumbnail(url="https://img.game8.jp/1624573/ba4f5f835f2f94ca431b7c11173e43db.png/show?1526527610")
		msg.add_field(name="ルール："+dic['rule'], value=dic['maps'][0]+" and "+dic['maps'][1], inline=True)
		return msg
	if index < 4:
		msg = discord.Embed(title='リーグマッチ',colour=0xff00ff)
		msg.set_thumbnail(url="https://img.game8.jp/1624587/c4a871db639f4c8a809639b6a8cda050.png/show?1526527769")
		msg.add_field(name="ルール："+dic['rule'], value=dic['maps'][0]+" and "+dic['maps'][1], inline=True)
		return msg
	else:
		msg = discord.Embed(title='ナワバリ',colour=0xadff2f)
		msg.set_thumbnail(url="https://img.game8.jp/1624580/4a48b2bf985a9b5e79b78bdc7753f8b3.png/show?1526527741")
		msg.add_field(name="ルール："+dic['rule'], value=dic['maps'][0]+" and "+dic['maps'][1], inline=True)
		return msg

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


	#"!random_buki"とチャットに入力があった場合反応
	'''ランダム武器'''
	if message.content.startswith('random_buki'):
		voice_channel = discord.utils.get(message.server.channels, id=message.author.voice.voice_channel.id)
		p_list = voice_channel.voice_members
		voice_users= [ p_list[i].display_name for i in range(len(p_list))]
		rand_buki = randBuki(buki_list,voice_users)
		for i in rand_buki.keys():
			mbuki = '{}:{}'.format(i,rand_buki[i])
			msg = discord.Embed(title='ブキを決めるよ',description=mbuki, colour=0xffffff)
			msg.set_thumbnail(url="https://gashapon.jp/splatoon/images/shoplist/bg_ink_shoplist01.png")
			await client.send_message(message.channel, embed=msg)

	if message.content.startswith('おはよう'):
		# 送り主がBotだった場合反応しない
		if client.user != message.author:
			m = "おはよう、" + message.author.name + "！"
			# メッセージが送られてきたチャンネルへメッセージ送信
			await client.send_message(message.channel, m)

	if message.content.startswith("サイコロ"):
		saikoro = ['1','2','3','4','5','6']
		saikoro_choice = choice(saikoro)
		if client.user != message.author:
			# メッセージを書きます
			m = saikoro_choice
			await client.send_message(message.channel, '{} {}'.format(message.author.mention,m))

	if client.user.id in message.content:
		await client.send_message(message.channel, '{} 呼んだか？'.format(message.author.mention))

	if message.content.startswith('ガチマ'):
		m = getStageInfo(0)
		await client.send_message(message.channel, embed=m)

	if message.content.startswith("次のガチマ"):
		m = getStageInfo(1)
		await client.send_message(message.channel, embed=m)

	if message.content.startswith("リグマ"):
		m = getStageInfo(2)
		await client.send_message(message.channel, embed=m)

	if message.content.startswith("次のリグマ"):
		m = getStageInfo(3)
		await client.send_message(message.channel, embed=m)

	if message.content.startswith("ナワバリ"):
		m = getStageInfo(4)
		await client.send_message(message.channel, embed=m)

	if message.content.startswith("次のナワバリ"):
		m = getStageInfo(5)
		await client.send_message(message.channel, embed=m)

	if message.content.startswith("!"):
		m = "＊この機能は現在メンテナンス中です＊"
		await client.send_message(message.channel, m)
'''
	if message.content[0] == '!':
		boturl = "https://chatbot-api.userlocal.jp/api/chat?message=" + message.content + "&key=f2ff5ccc7af428543654"
		headers = {"content-type": "application/json"}
		r = requests.get(boturl, headers=headers)
		data = r.json()
		reply=data["result"]

		if client.user != message.author:
			await client.send_message(message.channel, reply)
'''

client.run("NDY3MTgxMTU3ODcyNjk3MzQ0.Do9LpQ.GXRLzbKePmAbVYCo-4pnsl2irZY")
"""
if __name__ == '__mian__':
	main()
"""
