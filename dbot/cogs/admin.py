from socket import inet_aton
from turtle import position
from unittest.result import failfast
import config as c
import discord,dateutil.parser,random,subprocess,datetime,sys,spotipy,aiohttp,time,json,asyncio
from discord.ext import commands
from discord.commands import Option
from discord.ui import View, Button, Select

class Admin(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("[Admin.py] Set ready.")

    @commands.slash_command(name="stop", description="開発者限定緊急停止")
    async def SCRIPT_STOP(self, interaction):
        if not int(interaction.author.id) in c.admin_users:
            await interaction.respond("帰れ")
            return
        user = self.bot.get_user(    )
        e = discord.Embed(title="強制終了報告", description=f"{datetime.datetime.now()}",color=0x6dc1d1)
        await user.send(embed=e)
        await interaction.respond(f"{datetime.datetime.now()}\n{interaction.author}\n{interaction.author.id}")    
        sys.exit()

    @commands.slash_command(name="twitter_search", descriotion="TwitterAccにてシャドウBANなどの確認")
    async def b(self, interaction, twitterid):
        if not int(interaction) in c.admin_users:
            await interaction.respond("帰れ", ephemeral=True)
            return
          
    @commands.slash_command(name="invite_delete", description="サーバーの招待コードを全削除")
    @commands.has_permissions(administrator=True)
    async def Delete_invite(self, interaction):
        guild = interaction.guild
        for invite in await guild.invites():
            await invite.delete()
        await interaction.respond("終わった")

    @commands.slash_command(name="reset", description="チャンネルを再作成")
    @commands.has_permissions(administrator=True)
    async def nuke(self, interaction, channel:discord.TextChannel=None, meonly:Option(str, "再作成後のチャンネルメンションについて", choices=["Yes", "No"])=None):
        if not channel:channel = interaction.channel
        else:channel=discord.utils.get(interaction.guild.channels, name=channel.name)
        position = channel.position
        new_ch = await channel.clone()
        await new_ch.edit(position=position)
        await channel.delete()
        if meonly in ("Yes"):await interaction.respond(f"<#{new_ch.id}>", ephemeral=True)
        else: await interaction.respond(f"<#{new_ch.id}>")


    @commands.slash_command(name="purge", description="数値分メッセージを削除")
    @commands.has_permissions(manage_messages=True)
    async def mesasge_purge(self, interaction:discord.Interaction, amount:Option(int, "整数を入力")):
        deleted = await interaction.channel.purge(limit=amount)
        e = discord.Embed(description=f"Message Purged!```{len(deleted)} messages```\nAutomatically deleted after 5 seconds").set_footer(text=f"By: {interaction.author}")
        await interaction.response.send_message(embed=e, delete_after=5)

    @commands.slash_command(name="kick", description="メンバーをキック")
    @commands.has_permissions(kick_members=True)
    async def kick_member(self, interaction, user:discord.Member, reason:Option(str, "ユーザーをBANする理由。無くても可。")= None):
        if not reason: reason = "No reason provided."
        user.kick(reason=reason)
        e=discord.Embed(title=f":wave::wave: {user}", description=f"ID: {user.id}", color=0xff0000).add_field(name="Reason", value=f"```{reason}```")
        await interaction.respond(embed=e)

    @commands.slash_command(name="ban", description="メンバーをBAN")
    @commands.has_permissions(ban_members= True)
    async def ban(self, interaction, user:discord.Member, reason:Option(str, "ユーザーをBANする理由。無くても可。")= None):
        if not reason:reason="No reason"
        await user.ban(reason=reason)
        e=discord.Embed(title=f":wave::wave: {user}", description=f"ID: {user.id}", color=0xff0000).add_field(name="Reason", value=f"```{reason}```")
        await interaction.respond(embed=e)

    @commands.slash_command(name="leave", description="開発者専用")
    async def leave(self, interaction, guild_id=None):
        if not int(interaction.author.id) in c.admin_users:
            await interaction.respond("帰れ。", ephemeral=True)
            return
        guild = self.bot.get_guild(int(guild_id))
        await guild.leave()
        await interaction.respond(f"{guild} から脱退しました。")

    @commands.slash_command(name="global_ban", description="開発者専用", guild_ids=[])
    async def global_ban(self, interaction, member : discord.Member, reason=None):
        if not int(interaction.author.id) in c.admin_users:
            await interaction.response.send_message("帰れ", ephemeral=True)
            return


    @commands.slash_command(name="inserver", description="管理者専用Botが入ってるサーバーを表示")
    async def inserver(self, interaction):
        if not int(interaction.author.id) in c.admin_users:
            await interaction.send("gfy")
            return
        with open("server.txt", "w", encoding='utf-8') as f:
            activeservers = self.bot.guilds
            for guild in activeservers:
                f.write(f"[ {str(guild.id)} ] {guild.name}\n")
        await interaction.send(file=discord.File("server.txt", filename="SERVERLIST.txt"))


    @commands.slash_command(name="xserver", description="server idを入れてね!このボットが入ってるサーバーの情報を取得")
    @commands.cooldown(1,60, commands.BucketType.user)
    async def xserver(self, interaction, id:str):
        if not int(interaction.author.id) in c.admin_users:
            await interaction.respond("帰れ。", ephemeral=True)
            return
        guild = self.bot.get_guild(int(id))
        date_f= "%Y/%m/%d"
        tchannels= len(guild.text_channels)
        vchannels= len(guild.voice_channels)
        roles= [role for role in guild.roles]
        emojis= [1 for emoji in guild.emojis]
        online= [1 for user in guild.members if user.status != discord.Status.offline]
        stickers = [sticker  for sticker in guild.stickers]
        embed= discord.Embed(title=f"{guild.name}", description= f":crown: **Owner : **{guild.owner.mention}\n\
            :id: **Server id : `{guild.id}`**\n\:calendar_spiral: Createion : **`{guild.created_at.strftime(date_f)}`**", color= 0x6dc1d1)
        try:embed.set_thumbnail(url= guild.icon.url)
        except:pass
        embed.add_field(name= ":shield: Role", value= f"Roles: **{len(roles)}**", inline= True)
        embed.add_field(name= f":gem: Boost [{guild.premium_subscription_count}]", value= f"Tier: ** {guild.premium_tier}**")
        try:
            vanity =  await guild.vanity_invite()
            embed.add_field(name=":link: Vanity URL", value=f"`{str(vanity).replace('https://discord', '')}`")
        except:embed.add_field(name=":link: Vanity URL", value=f"`None`")        
        embed.add_field(name= ":grinning: Emoji", value= f"Emojis: **{len(emojis)}**\nStickers: **{len(stickers)}**")
        embed.add_field(name= f":busts_in_silhouette: Members [{guild.member_count}]", 
                value= f"User: **{str(sum(1 for member in guild.members if not member.bot))}**\nBot: **{str(sum(1 for member in guild.members if member.bot))}**\nOnline: **{len(online)}**")
        embed.add_field(name= f":speech_left: Channels [{tchannels+vchannels}]", 
                value= f"Text: **{tchannels}**\nVoice: **{vchannels}**\nCategory: **{len(guild.categories)}**",inline= True)
        embed.set_footer(text= f"By: {str(interaction.author)}")
        await interaction.respond(embed=embed)


def setup(bot):
    return bot.add_cog(Admin(bot))
