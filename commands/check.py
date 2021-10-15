import json
import urllib.request
from re import match
from typing import Sequence
import discord
from discord.ext import commands
from core.classes import Cog_Extension
from discord.utils import get
from difflib import *
import core.hypixel as hypixel
import os

API_KEYS = [os.environ['API_KEY']]
hypixel.setKeys(API_KEYS)

class Check(Cog_Extension):
    @commands.command()
    async def check(self,ctx):
          playerRank = {"rank":"None"}
          await ctx.send(f"{ctx.message.author.mention} Checking......")
          nickname = ctx.message.author.display_name
          if SequenceMatcher(None, nickname, "<").ratio() == 0 or SequenceMatcher(None, nickname, ">").ratio() == 0:
              await ctx.send("暱稱格式不正確\n請改為暱稱<Minecraft ID>")
          else:
              id = nickname.split('<')
              id1 = id[1].split('>')
              if id1[0] != "no ID":
                  resource_url = 'https://api.mojang.com/users/profiles/minecraft/' + id1[0]
                  getPlayerUUID = json.loads(urllib.request.urlopen(resource_url).read())
                  playerUUID = getPlayerUUID['id']
                  player = hypixel.Player(playerUUID)
                  playerRank = player.getRank()
                  memberRankRole = discord.utils.get(ctx.guild.roles, name=playerRank['rank'])
                  await ctx.author.add_roles(memberRankRole)
                  #公會ID
                  playerGuildID = player.getGuildID()
                  if playerGuildID is not None:
                      guild = hypixel.Guild(playerGuildID)
                      playerGuildData = guild.JSON
                      playerGuildName = str(playerGuildData['name'])
                      print(playerGuildName)
                      is_role_ava = discord.utils.get(ctx.guild.roles,name=playerGuildName)
                      if is_role_ava is None:
                           await ctx.guild.create_role(name = playerGuildName)
                           memberGuildRole = discord.utils.get(ctx.guild.roles, name=playerGuildName)
                      else:
                           memberGuildRole = discord.utils.get(ctx.guild.roles, name=playerGuildName)
                      await ctx.author.add_roles(memberGuildRole)
                      if playerGuildName == 'HelloTaiwan':
                          memberRoleName = '普通會員<Member>'
                          print(memberRoleName)
                      else:
                          memberRoleName = '🌈好捧油🌈<Friend>'
                          print(memberRoleName)
                  else:
                    memberRoleName = '🌈好捧油🌈<Friend>'
                    playerRank['rank'] = "None"
                    playerGuildName = "None"
              elif id1[0] == "no ID":
                playerGuildName = "None"
                playerRank['rank'] = "None"
                memberRoleName = '🌈好捧油🌈<Friend>'
              else:
                pass
              memberRole = discord.utils.get(ctx.guild.roles, name=memberRoleName)
              await ctx.author.add_roles(memberRole)
              embed=discord.Embed(title="Player Information", description="以下會秀出你的資訊", color=0xe2ff0a)
              embed.add_field(name="Minecraft ID", value=id1[0], inline=False)
              embed.add_field(name="Hypixel Rank", value=playerRank['rank'], inline=False)
              embed.add_field(name="目前所在公會", value=playerGuildName, inline=False)
              embed.set_footer(text="身分組添加完畢 Having Fun :P")
              await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Check(bot))
