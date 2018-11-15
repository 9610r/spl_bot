#-*- -*- -*- -*- -*- -*- -*- -*- coding:UTF-8 -*- -*- -*- -*- -*- -*- -*- -*- -
import json
import discord
import requests
import re
from random import randint,choice
import datetime
import os
#-*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
LOG_CHANNEL_ID = os.environ["LOG_CHANNEL_ID"]
LOOK_SERVER_ID = os.environ["LOOK_SERVER_ID"]
RECT_CHANNEL_ID = os.environ["RECT_CHANNEL_ID"]

def getStageInfo(index=0):
	'''ステージ情報'''
	links = (
				'gachi/now','gachi/next',
				'league/now','league/next',
				'regular/now','regular/next',
				'coop/schedule'
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

	elif index < 4:
		msg = discord.Embed(title='リーグマッチ',colour=0xff00ff)
		msg.set_thumbnail(url="https://img.game8.jp/1624587/c4a871db639f4c8a809639b6a8cda050.png/show?1526527769")
		msg.add_field(name="ルール："+dic['rule'], value=dic['maps'][0]+" and "+dic['maps'][1], inline=True)
		return msg

	elif index < 6:
		msg = discord.Embed(title='ナワバリ',colour=0xadff2f)
		msg.set_thumbnail(url="https://img.game8.jp/1624580/4a48b2bf985a9b5e79b78bdc7753f8b3.png/show?1526527741")
		msg.add_field(name="ルール："+dic['rule'], value=dic['maps'][0]+" and "+dic['maps'][1], inline=True)
		return msg

def randBuki(buki_list, users):
	len_u = len(users)
	return {i:choice(buki_list) for i in users}
#clientオブジェクトの生成
client = discord.Client()
with open('buki.csv', encoding='UTF-8') as f:
	buki_list = f.readlines()
	
def randBuki_class(buki_list, users):
	len_u = len(users)
	return {i:choice(buki_list) for i in users}
#clientオブジェクトの生成
client = discord.Client()
with open('buki_class.csv', encoding='UTF-8') as f:
	buki_list = f.readlines()

def randBuki_sub(buki_list, users):
	len_u = len(users)
	return {i:choice(buki_list) for i in users}
#clientオブジェクトの生成
client = discord.Client()
with open('subeapon.csv', encoding='UTF-8') as f:
	buki_list = f.readlines()

def randBuki_sp(buki_list, users):
	len_u = len(users)
	return {i:choice(buki_list) for i in users}
#clientオブジェクトの生成
client = discord.Client()
with open('special.csv', encoding='UTF-8') as f:
	buki_list = f.readlines()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	await client.change_presence(game=discord.Game(name="Splatoon2"))
	print('------')

@client.event
async def on_voice_state_update(before, after):
	if after.server.id == LOOK_SERVER_ID:
		nowtime = datetime.datetime.utcnow()
		nowtime = nowtime + datetime.timedelta(hours=9)
		nowtime = nowtime.strftime("%m/%d-%H:%M")
		#print(getserver.voice_channel)
		vcchannel = client.get_channel(LOG_CHANNEL_ID)

		if(before.voice_channel is None):
			jointext=jptime + "に"+ after.name + "　が　"+ after.voice_channel.name + " に参加しました。"
			await client.send_message(vcchannel, jointext)
		elif(after.voice_channel is None):
			outtext=jptime + "に"+ before.name + "　が　"+ before.voice_channel.name + " から退出しました。"
			await client.send_message(vcchannel, outtext)

@client.event
async def on_message(message):
	#"random_buki"とチャットに入力があった場合反応
	'''ランダム武器'''
	if message.content.startswith('.rand'):
		voice_channel = discord.utils.get(message.server.channels, id=message.author.voice.voice_channel.id)
		p_list = voice_channel.voice_members
		voice_users= [ p_list[i].display_name for i in range(len(p_list))]
		rand_buki = randBuki(buki_list,voice_users)
		mbuki = ''
		for i in rand_buki.keys():
			mbuki =  mbuki + '{}:{}'.format(i,rand_buki[i])
		msg = discord.Embed(title='ブキを決めるよ',description=mbuki, colour=0xffffff)
		msg.set_thumbnail(url="./ink01.png")
		await client.send_message(message.channel, embed=msg)
	
	elif message.content.startswith('.randclass'):
		voice_channel = discord.utils.get(message.server.channels, id=message.author.voice.voice_channel.id)
		p_list = voice_channel.voice_members
		voice_users= [ p_list[i].display_name for i in range(len(p_list))]
		rand_buki = randBuki_class(buki_list,voice_users)
		mbuki = ''
		for i in rand_buki.keys():
			mbuki =  mbuki + '{}:{}'.format(i,rand_buki[i])
		msg = discord.Embed(title='ブキの種類を決めるよ',description=mbuki, colour=0xffffff)
		msg.set_thumbnail(url="./ink01.png")
		await client.send_message(message.channel, embed=msg)
		
	elif message.content.startswith('.randsub'):
		voice_channel = discord.utils.get(message.server.channels, id=message.author.voice.voice_channel.id)
		p_list = voice_channel.voice_members
		voice_users= [ p_list[i].display_name for i in range(len(p_list))]
		rand_buki = randBuki_sub(buki_list,voice_users)
		mbuki = ''
		for i in rand_buki.keys():
			mbuki =  mbuki + '{}:{}'.format(i,rand_buki[i])
		msg = discord.Embed(title='サブを決めるよ',description=mbuki, colour=0xffffff)
		msg.set_thumbnail(url="./ink01.png")
		await client.send_message(message.channel, embed=msg)
		
	elif message.content.startswith('.randsp'):
		voice_channel = discord.utils.get(message.server.channels, id=message.author.voice.voice_channel.id)
		p_list = voice_channel.voice_members
		voice_users= [ p_list[i].display_name for i in range(len(p_list))]
		rand_buki = randBuki_sp(buki_list,voice_users)
		mbuki = ''
		for i in rand_buki.keys():
			mbuki =  mbuki + '{}:{}'.format(i,rand_buki[i])
		msg = discord.Embed(title='スペシャルを決めるよ',description=mbuki, colour=0xffffff)
		msg.set_thumbnail(url="./ink01.png")
		await client.send_message(message.channel, embed=msg)

	elif message.content.startswith('おはよう'):
		# 送り主がBotだった場合反応しない
		if client.user != message.author:
			m = "おはよう、" + message.author.name + "！"
			# メッセージが送られてきたチャンネルへメッセージ送信
			await client.send_message(message.channel, m)
	elif message.content.startswith('.help'):
		# 送り主がBotだった場合反応しない
		if client.user != message.author:
			m = "これを見てね！\n" +"https://qiita.com/IkayomeCh/private/5c3ada164e5f2af9d88a"
			# メッセージが送られてきたチャンネルへメッセージ送信
			await client.send_message(message.channel, m)

	elif message.content.startswith("サイコロ"):
		saikoro_choice = choice(['1','2','3','4','5','6'])
		if client.user != message.author:
			# メッセージを書きます
			m = saikoro_choice
			await client.send_message(message.channel,'{} {}'.format(message.author.mention,m))

	elif client.user.id in message.content:
		await client.send_message(message.channel, '{} 呼んだか？'.format(message.author.mention))

	elif message.content.startswith('.gachi'):
		m = getStageInfo(0)
		await client.send_message(message.channel, embed=m)

	elif message.content.startswith("..gachi"):
		m = getStageInfo(1)
		await client.send_message(message.channel, embed=m)

	elif message.content.startswith(".league"):
		m = getStageInfo(2)
		await client.send_message(message.channel, embed=m)

	elif message.content.startswith("..league"):
		m = getStageInfo(3)
		await client.send_message(message.channel, embed=m)

	elif message.content.startswith(".nawabari"):
		m = getStageInfo(4)
		await client.send_message(message.channel, embed=m)

	elif message.content.startswith("..nawabari"):
		m = getStageInfo(5)
		await client.send_message(message.channel, embed=m)

	elif message.content.startswith(".salmon"):
		headers = {"User-Agent": "IKSbot/1.0(twitter @ikayomech)"}
		url = "https://spla2.yuu26.com/coop/schedule"
		response = requests.get(url,headers=headers)
		dic = json.loads(response.text)
		dic = dic['result'][0]

		time_st,time_ed = dic['start'],dic['end']
		time_st = time_st.replace('T',' ')[5:16]
		time_stc = time_st.replace('-',' ').replace(':',' ').replace(' ','')
		time_ed = time_ed.replace('T',' ')[5:16]
		time_edc = time_ed.replace('-',' ').replace(':',' ').replace(' ','')
		time = time_st.replace('-','/')+"～"+time_ed.replace('-','/')
		nowtime = datetime.datetime.now().strftime("%m%d%H%M")
		if nowtime > time_stc and nowtime < time_edc:
			nowinfo = "≪開催中！!≫"
		else:
			nowinfo = "≪シフト予定≫"
		msg = discord.Embed(title='サーモンラン '+nowinfo, description=time,colour=0xFB7E00)
		msg.set_thumbnail(url=dic['stage']['image'])
		msg.add_field(name=dic['stage']['name'],value=dic['weapons'][0]['name']+'\n'+dic['weapons'][1]['name']+'\n'+dic['weapons'][2]['name']+'\n'+dic['weapons'][3]['name'], inline=True)
		await client.send_message(message.channel, embed=msg)

	elif message.content.startswith("!"):
		boturl = "https://chatbot-api.userlocal.jp/api/chat?message=" + message.content[1:] + "&key=f2ff5ccc7af428543654"
		headers = {"content-type": "application/json"}
		r = requests.get(boturl, headers=headers)
		data = r.json()
		reply=data["result"]

		if client.user != message.author:
			await client.send_message(message.channel, reply)

	'''
			"""メンバー募集 (.rect 内容 @数字)"""
	elif message.content.startswith(".rect"):
		m = re.split(' ', message.content)
		# ['one', 'two', 'one', 'two']
		mcount = int(m[2][1:])
		text= m[1]+"あと{}人 募集中\n"
		revmsg = text.format(mcount)
		#friend_list 押した人のList
		frelist = []
		msg = await client.send_message(message.channel, revmsg)
		finish_msg = '募集終了\n'+ '\n'.join(frelist)
		#投票の欄
		await client.add_reaction(msg, '\u21a9')
		await client.add_reaction(msg, '⏫')
		await client.add_reaction(msg, '📌')
		await client.pin_message(msg)

		#serverログ監視
		botlog = "{} type {}to{}".format(message.author.name,message.content,message.channel.id)
		devchannel = client.get_channel(RECT_CHANNEL_ID)
		await client.send_message(devchannel, botlog)

		#リアクションをチェックする
		while len(frelist) < int(m[2][1:]):
			target_reaction = await client.wait_for_reaction(message=msg)
			#発言したユーザが同一でない場合 真
			if target_reaction.user != msg.author:
				#==============================================================
				#押された絵文字が既存のものの場合 >> 左　del
				if target_reaction.reaction.emoji == '\u21a9':
					#==========================================================
					#◀のリアクションに追加があったら反応 frelistにuser.nameがあった場合　真
					if target_reaction.user.name in frelist:
						frelist.remove(target_reaction.user.name)
						mcount += 1
						#リストから名前削除
						await client.edit_message(msg, text.format(mcount) +'\n'.join(frelist))
						#メッセージを書き換え

					else:
						pass
						#==============================================================
						#押された絵文字が既存のものの場合　>> 右　add
				elif target_reaction.reaction.emoji == '⏫':
					if target_reaction.user.name in frelist:
						pass

					else:
						frelist.append(target_reaction.user.name)
						#リストに名前追加
						mcount = mcount - 1
						await client.edit_message(msg, text.format(mcount) +'\n'.join(frelist))

				elif target_reaction.reaction.emoji == '📌':
					await client.edit_message(msg, '募集終了')
					await client.unpin_message(msg)
					await client.send_message(message.channel, m[1]+'に'+ '\n'.join(frelist)+'が集まりました')
					break

				await client.remove_reaction(msg, target_reaction.reaction.emoji, target_reaction.user)
					#ユーザーがつけたリアクションを消す※権限によってはエラー
					#==============================================================
		else:
			await client.edit_message(msg, '終了')
			await client.unpin_message(msg)
			await client.send_message(message.channel, m[1]+'に'+ '\n'.join(frelist)+'が集まりました')
	'''

client.run(DISCORD_TOKEN)
