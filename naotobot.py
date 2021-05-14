import discord
import json
import random
from discord.ext import commands
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
from googlesearch import search

url = 'https://wrapapi.com/use/txxx/currency/usd-try/0.1.0?wrapAPIKey=7YQu0z1Qy6xPA5Dg6cReTQprt96iGj3g'
response = requests.get(url)
data = response.json()

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = 'n!', intents = intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Acı çekiyor'))
    print('Bot is ready.')

@client.event
async def on_member_join(member):
    print(f'{member} has appeared on guild {member.guild}!')

@client.event
async def on_member_remove(member):
    print(f'{member} has leaved from guild {member.guild}!')

@client.command()
async def gay(ctx):
    await ctx.send('Why are you gay!')

@client.command()
async def ping(ctx):
    await ctx.send(f'Your ping {round(client.latency*1000)}ms')

@client.command()
async def clear(ctx, amount):
    await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member: discord.Member = None):
    await member.kick()

@client.command()
async def ban(ctx, member: discord.Member = None):
    await member.ban()
    await ctx.send('ÇIKARILDIN')

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if(user.name, user.discriminator) == (member_name,member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send('AFFEDİLDİN')
            return

@client.command()
async def dolar(ctx):
    x = data["data"]["usdtry"]
    await ctx.send(f'{x}')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

@client.command()
async def hltb(ctx, *, gameName):
    query = 'how long to beat ' + gameName
    urls = [] 
    for j in search(str(query),tld="com",start=0, num=10, stop=10, pause=0):
        print(j)
        if 'https://howlongtobeat.com/game?id=' in j:
            j = j.split('&')[0]
            urls.append(j)
        if 'https://howlongtobeat.com/game.php?id=' in j:
            if '&' in j:
                j = j.split('&')[0]
            urls.append(j)
        if 'https://hl2b.com/game?id=' in j:
            j = j.split('&')[0]
            urls.append(j)
        if 'https://hl2b.com/game.php?id=' in j:
            j = j.split('&')[0]
            urls.append(j)
        
    html_text = requests.get(urls[0],headers=headers)
    soup = BeautifulSoup(html_text.text,'lxml')
    findIndex = 'short time_'
    index = 10
    images = soup.find_all('div', class_ = 'game_image desktop_hide')
    for image in images:
        imageLink = image.img
    imageLink = 'https://howlongtobeat.com' + imageLink.get('src')
    await ctx.send(f'{imageLink}')
    while(index != 110):
        findIndex = findIndex + str(index)
        times =  soup.find_all('li', class_ = findIndex)
        for time in times:
             game_name = time.h5.text
             game_time = time.div.text
             await ctx.send(f'{game_name}: {game_time}')
        index = index + 10
        findIndex = 'short time_'
@client.command()
async def a(ctx, *, animeName):
    query = '''
    query ($id: Int, $page: Int, $perPage: Int, $search: String) {
    Page (page: $page, perPage: $perPage) {
        pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
            perPage
        }
        media (id: $id, search: $search, type: ANIME) {
            id
            title {
                romaji
            }
        }
    }
    }
    '''
    variables = {
    'search': animeName,
    'page': 1,
    'perPage': 1
    }
    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    x = response.json()
    print(x["data"])
    animeLink = 'https://anilist.co/anime/' + str(x["data"]["Page"]["media"][0]["id"])
    
    await ctx.send(animeLink)
@client.command()
async def m(ctx, *, mangaName):
    query = '''
    query ($id: Int, $page: Int, $perPage: Int, $search: String) {
    Page (page: $page, perPage: $perPage) {
        pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
            perPage
        }
        media (id: $id, search: $search, type: MANGA) {
            id
            title {
                romaji
            }
        }
    }
    }
    '''
    variables = {
    'search': mangaName,
    'page': 1,
    'perPage': 1
    }
    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    x = response.json()
    print(x["data"])
    mangaLink = 'https://anilist.co/manga/' + str(x["data"]["Page"]["media"][0]["id"])
    await ctx.send(mangaLink)
@client.command()
async def steam(ctx, *, gameName):
    query = 'steam ' + gameName
    urls = [] 
    for j in search(str(query),tld="com",start=0, num=10, stop=10, pause=0):
        print(j)
        if 'https://store.steampowered.com/' in j:
            urls.append(j)
    await ctx.send(urls[0])
@client.command()
async def ahegao(ctx):
    url2 = 'https://ahegao.egecelikci.com/api'
    response = requests.get(url2)
    data2 = response.json()
    x = data2["msg"]
    await ctx.send(f'{x}')

client.run('')
