#-*- -*- -*- -*- -*- -*- -*- -*- coding:UTF-8 -*- -*- -*- -*- -*- -*- -*- -*- -
import json
import discord #v1.0
import requests
import re
from random import randint,choice
import datetime
import os
from discord.ext import commands
#-*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*

#DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
#LOG_CHANNEL_ID = os.environ["LOG_CHANNEL_ID"]
#LOOK_SERVER_ID = os.environ["LOOK_SERVER_ID"]
#RECT_CHANNEL_ID = os.environ["RECT_CHANNEL_ID"]

client = commands.Bot(command_prefix='.', description='bot')
sai = range(1,101)

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

def randBuki(buki_list1, users):
	len_u = len(users)
	return {i:choice(buki_list1) for i in users}
with open('buki.csv', encoding='UTF-8') as f:
	buki_list1 = f.readlines()

def rand_Stage():
	with open('stage.csv', encoding='UTF-8') as f:
		stage_list = f.readlines()
		stage_list = choice(stage_list)
		return stage_list



@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	await client.change_presence(activity=discord.Game(name="Spl2Bot v.1.1"))
	print('------')

@client.command()
async def echo(ctx, what):
    await ctx.send(f'{what}とはなんですか')

@client.command()
async def dice(ctx, ss: int):
    if ss == '':
        saikoro_choice = choice(sai)
        print(saikoro_choice)
        await ctx.send(saikoro_choice)
    else :
        saikoro_choice = choice(sai[:ss])
        print(saikoro_choice)
        await ctx.send(saikoro_choice)

@client.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a+b)

@client.command()
async def remove(ctx, a: int, b: int):
    await ctx.send(a-b)

@client.command()
async def multiply(ctx, a: int, b: int):
    await ctx.send(a*b)

@client.command()
async def greet(ctx):
    await ctx.send(":smiley: :wave: Hello, there!")

@client.command()
async def random(ctx):
	voice_channel = discord.utils.get(ctx.guild.channels, id=ctx.author.voice.channel.id)
	p_list = voice_channel.members
	voice_users= [ p_list[i].display_name for i in range(len(p_list))]
	rand_buki1 = randBuki(buki_list1,voice_users)
	mbuki1 = ''
	stage = "test"
	for i in rand_buki1.keys():
		mbuki1 =  mbuki1 + '{}: {}'.format(i,rand_buki1[i])
	msg = discord.Embed(title=stage,description=mbuki1, colour=0xffffff)
	#msg.set_thumbnail(url="https://pbs.twimg.com/profile_images/819765217957552132/1WftJJM1_400x400.jpg")
	await ctx.send(embed=msg)

@client.command()
async def info(ctx):
    embed = discord.Embed(title="Splatoon2 bot", description="This bot is Spl2Bot.", color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="ikayomeCh")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

client.remove_command('help')

@client.command()
async def help(ctx):
    embed = discord.Embed(title="<<<Splatoon2 bot>>>", description="commands list:", color=0xeeefff)

    embed.add_field(name="$add X Y", value="Gives the addition of **X** and **Y**", inline=False)
    embed.add_field(name="$multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
    embed.add_field(name="$greet", value="Gives a nice greet message", inline=False)
    embed.add_field(name="$cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
    embed.add_field(name="$info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="$help", value="Gives this message", inline=False)

    await ctx.send(embed=embed)





@client.event
async def on_message(message):
	if message.content.startswith('.gachi'):
		m = getStageInfo(0)
		await message.channel.send(embed=m)

	elif message.content.startswith("..gachi"):
		m = getStageInfo(1)
		await message.channel.send(embed=m)

	elif message.content.startswith(".league"):
		m = getStageInfo(2)
		await message.channel.send(embed=m)

	elif message.content.startswith("..league"):
		m = getStageInfo(3)
		await message.channel.send(embed=m)

	elif message.content.startswith(".nawabari"):
		m = getStageInfo(4)
		await message.channel.send(embed=m)

	elif message.content.startswith("..nawabari"):
		m = getStageInfo(5)
		await message.channel.send(embed=m)

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
		if time_stc < nowtime < time_edc:
			nowinfo = "≪開催中！!≫"
		else:
			nowinfo = "≪シフト予定≫"

		msg = discord.Embed(title='サーモンラン'+nowinfo, description=time,colour=0xFB7E00)
		msg.set_thumbnail(url=dic['stage']['image'])
		msg.add_field(name=dic['stage']['name'],value=dic['weapons'][0]['name']+'\n'+dic['weapons'][1]['name']+'\n'+dic['weapons'][2]['name']+'\n'+dic['weapons'][3]['name'], inline=True)
		await message.channel.send(embed=msg)
	await client.process_commands(message)


client.run(DISCORD_TOKEN)
