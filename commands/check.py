from re import match
from typing import Sequence
import discord
import requests
import json
import os
from discord.ext import commands
from core.classes import Cog_Extension
from discord.utils import get
from difflib import *

class Check(Cog_Extension):
    @commands.command()
    async def check(self, ctx):
        await ctx.send(f"<@!{ctx.message.author.id}> Checking......")
        nickname = str(ctx.message.author.display_name)
        if SequenceMatcher(None, nickname, "<").ratio() == 0 or SequenceMatcher(None, nickname, ">").ratio() == 0:
            await ctx.send("暱稱格式不正確\n請改為暱稱<Minecraft ID>\n如果沒有Minecraft ID 請將暱稱改為暱稱<no ID>")
        else:
            id = nickname.split('<')
            id1 = id[1].split('>')
            await ctx.send(f"Minecraft ID : {id1[0]}")
            if id1[0] == "no ID":
                memberRoleG = discord.utils.get(ctx.guild.roles, name='🌈好捧油🌈<Friend>')
            else:
                r2 = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{id1[0]}")
                print(r2.status_code)
                if r2.status_code == 200:
                    pName = r2.json()
                    r = requests.get(f"https://api.hypixel.net/findGuild?key={os.environ['API_KEY']}&byUuid={pName['id']}")
                    gid = r.json()
                    if gid['guild'] is None:
                        await ctx.send('查無公會')
                    else:
                        r1 = requests.get(f"https://api.hypixel.net/guild?key={os.environ['API_KEY']}&id={gid['guild']}")
                        gjson = r1.json()
                        await ctx.send(f"目前所在公會 : {gjson['guild']['name']}")
                else:
                    await ctx.send('查無此ID')
                r3 = requests.get(f"https://api.hypixel.net/player?key={os.environ['API_KEY']}&uuid={pName['id']}")
                playerRank = r3.json()
                if "rank" in playerRank['player']:
                    pRank = playerRank['player']['rank']
                else:
                    if "monthlyPackageRank" in playerRank['player']:
                        pRank = "MVP_PLUS_PLUS"
                    else:
                        if "newPackageRank" in playerRank['player']:
                            pRank = playerRank['player']['newPackageRank']
                        else:
                            pRank = "None"
                await ctx.send(f"Hypixel Rank : {pRank}")
                if pRank == "MVP_PLUS_PLUS":
                    memberRole = discord.utils.get(ctx.guild.roles, name='MVP++')
                elif pRank == "MVP_PLUS":
                    memberRole = discord.utils.get(ctx.guild.roles, name='MVP+')
                elif pRank == "MVP":
                    memberRole = discord.utils.get(ctx.guild.roles, name='MVP')
                elif pRank == "VIP_PLUS":
                    memberRole = discord.utils.get(ctx.guild.roles, name='VIP+')
                elif pRank == "VIP":
                    memberRole = discord.utils.get(ctx.guild.roles, name='VIP')
                elif pRank == "None":
                    memberRole = discord.utils.get(ctx.guild.roles, name='none')
                elif pRank == "ADMIN":
                    memberRole = discord.utils.get(ctx.guild.roles, name='Hypixel Admin')
                elif pRank == "YOUTUBER":
                    memberRole = discord.utils.get(ctx.guild.roles, name='Hypixel Youtuber')
                else:
                    await ctx.send("查無Rank，請聯絡管理員:(")
                    memberRole = discord.utils.get(ctx.guild.roles, name='none')
                print(memberRole)
                await ctx.author.add_roles(memberRole)
                await ctx.send("Hypixel Rank身分組成功增加")
                if gid['guild'] is None:
                    memberRoleG = discord.utils.get(ctx.guild.roles, name='🌈好捧油🌈<Friend>')
                elif gjson['guild']['name'] == "HelloTaiwan":
                    memberRoleG = discord.utils.get(ctx.guild.roles, name='普通會員<Member>')
                else:
                    memberRoleG = discord.utils.get(ctx.guild.roles, name='🌈好捧油🌈<Friend>')
            await ctx.author.add_roles(memberRoleG)
            await ctx.send("Discord身分組成功增加\nHaving Fun :U")

def setup(bot):
    bot.add_cog(Check(bot))
