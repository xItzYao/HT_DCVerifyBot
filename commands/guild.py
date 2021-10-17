import discord
from discord.ext import commands
from core.classes import Cog_Extension
import core.hypixel as hypixel
import datetime
import core.getGuildLevel as getGuildLevel

class GuildInfo(Cog_Extension):
    @commands.command()
    async def guild(self,ctx,*guildNameInput:str):
        try:
            guildNameAdd = ""
            for name in guildNameInput:
                guildNameAdd = f"{guildNameAdd} {name}"
            guildNameConvert = guildNameAdd[1:].replace(' ','%20')
            print(guildNameConvert)
            guildID = hypixel.Guild.getGuildbyName(guildNameConvert)
            guild = hypixel.Guild(guildID)
            guildJSON = guild.JSON
            guildName = guildJSON['name']
            guildCreating = int(guildJSON['created'])/1000
            guildCreatingTime = datetime.datetime.fromtimestamp(guildCreating).strftime('%Y-%m-%d %H:%M:%S')
            guildMasterID = guildJSON['members'][0]['uuid']
            player = hypixel.Player(guildMasterID)
            guildMaster = player.getName()
            onlinePlayersCounting = guildJSON['achievements']['ONLINE_PLAYERS']
            lineColor = 0x8a8a8a
            if 'tag' in guildJSON:
                tag = guildJSON['tag']
                guildTag = f"[{tag}] {guildName}"
                guildTagColor = guildJSON['tagColor']
                if guildTagColor == "YELLOW":
                    lineColor = 0xebf924
                elif guildTagColor == "AQUA":
                    lineColor = 0x079cb6
                else:
                    lineColor = 0x8a8a8a
            else:
                guildTag = f"{guildName}"
            preferredGames = []
            if 'preferredGames' in guildJSON:
                preferredGames = guildJSON['preferredGames']
            else:
                preferredGames = ['None']
            preferredGamesAdd = ""
            for game in preferredGames:
                preferredGamesAdd = f"{preferredGamesAdd}、{game}"
            guildPreferredGames = preferredGamesAdd[1:].replace('BEDWARS', 'Bedwars').replace('SKYBLOCK', 'SkyBlock').replace('MURDER_MYSTERY', 'Murder Mystery').replace('SKYWARS', 'SkyWars').replace('DUELS', 'Duels').replace('SPEED_UHC', 'Speed UHC').replace('ARCADE', 'Arcade').replace('TNTGAMES', 'TNTGames')
            guildLevel = format(getGuildLevel.getLevel(guildJSON['exp']), '.1f')
            embed=discord.Embed(title=guildTag, url=f"https://plancke.io/hypixel/guild/name/{guildNameConvert}", color=lineColor)
            embed.add_field(name="公會長", value=guildMaster, inline=False)
            embed.add_field(name="公會等級", value=guildLevel, inline=False)
            embed.add_field(name="主打遊戲", value=guildPreferredGames, inline=False)
            embed.add_field(name="公會人數", value=len(guildJSON['members']), inline=False)
            embed.add_field(name="上線人數", value=onlinePlayersCounting, inline=False)
            embed.add_field(name="創建時間", value=guildCreatingTime, inline=False)
            await ctx.send(embed=embed)
        except hypixel.GuildIDNotValid:
            await ctx.send("查無此公會")


def setup(bot):
    bot.add_cog(GuildInfo(bot))