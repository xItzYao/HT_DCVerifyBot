import discord
import json
import os
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(os.environ['prefix'] , intents = intents)

@bot.event
async def on_ready():
    print('澳門首家ㄐㄐ賭場上線啦')
    await bot.change_presence(activity = discord.Streaming(name = "!help | !check進行身分認證", url = "https://www.twitch.tv/discord"))
    
@bot.event
async def on_member_join(member):
    await member.send(f'----------------------------------------------------------\n阿囉哈{member}d(d＇∀＇)\n請更改群內暱稱格式為\n> 暱稱<Minecraft ID>(區分大小寫)\n若無MC ID,請將暱稱改為\n> 暱稱<no ID>(須注意大小寫以及空格)\n後至<#697062783073779792>輸入指令```!check```\nHaving Fun!\n----------------------------------------------------------')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Error')

for fileName in os.listdir('./commands'):
    if fileName.endswith('.py'):
        bot.load_extension(f'commands.{fileName[:-3]}')

if __name__ == "__main__":
    bot.run(os.environ['token'])
