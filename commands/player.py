import discord
from discord.ext import commands
from core.classes import Cog_Extension
import core.hypixel as hypixel
import json
import urllib.request
import datetime

class PlayerInfo(Cog_Extension):
    @commands.command()
    async def player(self,ctx,mcid):
        try:
            resource_url = 'https://api.mojang.com/users/profiles/minecraft/' + mcid
            getPlayerUUID = json.loads(urllib.request.urlopen(resource_url).read())
            playerUUID = getPlayerUUID['id']
            player = hypixel.Player(playerUUID)
            playerInfo = player.getPlayerInfo()
            firstLogin = int(playerInfo['firstLogin'])/1000
            firstLoginTime = datetime.datetime.fromtimestamp(firstLogin).strftime('%Y-%m-%d %H:%M:%S')
            try:
                lastLogin = int(playerInfo['lastLogin'])/1000
                lastLoginTime = datetime.datetime.fromtimestamp(lastLogin).strftime('%Y-%m-%d %H:%M:%S')
            except KeyError:
                lastLoginTime = "None"
            playerRank = player.getRank()
            playerGuildID = player.getGuildID()
            if playerGuildID is None:
                playerGuildName = "無公會"
            else:
                guild = hypixel.Guild(playerGuildID)
                playerGuildData = guild.JSON
                playerGuildName = playerGuildData['name']
            if 'karma' in playerInfo:
                playerKarma = playerInfo['karma']
            else:
                playerKarma = 0
            playerLevel = player.getLevel()
            if playerRank['rank'] == "None":
                lineColor = 0x676b66
            if playerRank['rank'] == "VIP" or playerRank['rank'] =="VIP+":
                lineColor = 0x3de114
            if playerRank['rank'] == "MVP" or playerRank['rank'] =="MVP+":
                lineColor = 0x0df8dc
            if playerRank['rank'] == "MVP++":
                lineColor = 0xf9b92f
            if playerRank['rank'] == "Hypixel Helper":
                lineColor = 0x0544d6
            if playerRank['rank'] == "Hypixel Mod":
                lineColor = 0x1d8109
            if playerRank['rank'] == "Hypixel Admin" or playerRank['rank'] =="Hypixel Youtuber":
                lineColor = 0xff0000
            embed=discord.Embed(title="Player Info", description="以下為玩家資料", color=lineColor)
            embed.set_author(name=mcid, url="https://plancke.io/hypixel/player/stats/" + mcid, icon_url="https://crafatar.com/renders/head/" + playerUUID)
            embed.set_thumbnail(url="https://crafatar.com/renders/body/" + playerUUID)
            embed.add_field(name="玩家等級", value=format(playerLevel , '.1f'), inline=False)
            embed.add_field(name="目前所在公會", value=playerGuildName, inline=False)
            embed.add_field(name="Hypixel Rank", value=playerRank['rank'], inline=False)
            embed.add_field(name="Karma", value=playerKarma, inline=False)
            embed.add_field(name="首次登入時間", value=firstLoginTime, inline=False)
            embed.add_field(name="最後一次登入時間", value=lastLoginTime, inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send("查無此ID")


def setup(bot):
    bot.add_cog(PlayerInfo(bot))
