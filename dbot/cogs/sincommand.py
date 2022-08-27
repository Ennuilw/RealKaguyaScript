from email.policy import default
import config as c
import discord,dateutil.parser,random,subprocess,datetime,sys,spotipy,aiohttp,time,json,asyncio
from discord.ext import commands
from discord.commands import Option
from discord.ui import View, Button, Select

from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = c.spotify_client_id, client_secret = c.spotify_client_secret))

class MyView(View):
    def __init__(self):
        pass 

class MyBanner():
    def __init__(self):
        pass



class Sub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member=None

    @commands.Cog.listener()
    async def on_ready(self):
        print("[sincommand.py] Set ready.")
        await self.bot.change_presence(activity=discord.Streaming(platform="YouTube", name="D-tecnoLife", url="https://www.youtube.com/watch?v=IITjr6Ysh60"))
        
    @commands.slash_command(name="about", description="About this bot")
    async def about(self, interaction):
        user= self.bot.get_user(956042267221721119)
        members = 0
        for guild in self.bot.guilds:members += guild.member_count - 1
        embed= discord.Embed(title="About this bot", description="なぜか日本語と英語が入り混じってます。\n適当にスクリプト書いた。駄作です。<:Cirnohi:1010798243866755114>", color= 0x6dc1d1)
        embed.add_field(name= "Customers",value= f"> **Servers:** {str(len(self.bot.guilds))}\n> **Members:** {str(members)}", inline= False)
        embed.add_field(name= "Support", value= f"> **Deveroper:** {user.mention}\n> **Source:** [Github](https://github.com/Ennuilw/RealKaguyaScript)\n\
            > **Our server:** ||[Click me](https://discord.gg/projectengage)||", inline= False)
        embed.set_footer(text=f"By: {str(interaction.author)}")
        await interaction.respond(embed=embed)

    @commands.slash_command(name="account", description="アカウントの作成・参加日時")
    async def account(self, interaction:discord.Interaction, user:discord.Member=None):
        if not user:user=interaction.author
        date_format="%Y/%m/%d %H:%M:%S"
        e = discord.Embed(color=0x6dc1d1).set_author(name=f"{user} ID: {user.id}",url=user.display_avatar)
        e.add_field(name=f"アカウント作成日", value=f"**`{user.created_at.strftime(date_format)}`**")
        e.add_field(name="サーバー参加日", value= f"**`{user.joined_at.strftime(date_format)}`**").set_footer(text= f"By: {str(interaction.author)}")
        await interaction.response.send_message(embed=e)



    @commands.slash_command(name="avatar", description="サーバープロフィールのアイコンを取得")
    async def avatar(self, interaction:discord.Interaction, user:discord.Member=None):
        if not user: user= interaction.author
        avatar= user.display_avatar
        embed= discord.Embed(description= f"{user.mention} Avatar", color= 0x6dc1d1).set_image(url= avatar).set_footer(text= f"By: {str(interaction.author)}")
        await interaction.response.send_message(embed= embed)

    @commands.slash_command(name="banner", description="ユーザープロフィールからバナーを取得。もしあれば。")
    async def banner(self, interaction:discord.Interaction, user:discord.Member=None):
        if not user:user=interaction.author
        user = await self.bot.fetch_user(user.id)
        try:
            banner_url = user.banner.url
            avatar=user.display_avatar
            e=discord.Embed(description= f"{user.mention} Banner", color= 0x6dc1d1).set_image(url= banner_url).set_footer(text= f"By: {str(interaction.author)}")
            await interaction.respond(embed=e)
        except:await interaction.response.send_message("Bannerが検出できない")



    @commands.slash_command(name="userinfo", description="ユーザー情報を送信")
    async def userinfo(self, interaction, user:discord.Member=None):
        if not user: user= interaction.author
        date_format="%Y/%m/%d"
        s = str(user.status)
        s_icon = ""
        if s == "online":s_icon = "🟢"
        elif s == "idle":s_icon = "🟡"
        elif s == "dnd":s_icon = "🔴"
        elif s == "offline":s_icon = "⚫"
        embed= discord.Embed(title= f"{user}", description= f"**ID : `{user.id}`**", color= 0x6dc1d1)
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name= "Name", value= f"{user}", inline= True)
        embed.add_field(name= "Nickname", value= f"{user.display_name}", inline= True)
        embed.add_field(name="Status", value=f"> `{s_icon} {s}`", inline=True)
        if len(user.roles) >= 1:
            new_role = ([r.mention for r in user.roles][1:])
            embed.add_field(name= f"Roles `{len(user.roles)-1}`", value= f"> {' '.join(new_role[::-1])}", inline=False)
        embed.add_field(name= "Createion Account", value= f"> `{user.created_at.strftime(date_format)}`", inline= True)
        embed.add_field(name= "Joined Server", value= f"> `{user.joined_at.strftime(date_format)}`", inline= True)
        user = await self.bot.fetch_user(user.id)
        try:embed.set_image(url=user.banner.url)
        except:pass
        embed.set_footer(text= f"By: {str(interaction.author)}")
        await interaction.respond(embed= embed)


    @commands.slash_command(name="serverinfo", description="サーバーの詳細を表示")
    async def serverinfo(self, interaction):
        guild = interaction.guild
        date_f= "%Y/%m/%d"
        tchannels= len(guild.text_channels)
        vchannels= len(guild.voice_channels)
        roles= [role for role in guild.roles]
        emojis= [1 for emoji in guild.emojis]
        online= [1 for user in guild.members if user.status != discord.Status.offline]
        stickers = [sticker  for sticker in guild.stickers]
        embed= discord.Embed(title=f"{guild.name}", description= f":crown: **Owner : **{guild.owner.mention}\n\
            :id: **Server id : `{guild.id}`**\n\
            :calendar_spiral: Createion : **`{guild.created_at.strftime(date_f)}`**", color= 0x6dc1d1)
        try:embed.set_thumbnail(url= guild.icon.url)
        except:pass
        embed.add_field(name= ":shield: Role", value= f"Roles: **{len(roles)}**", inline= True)
        embed.add_field(name= f":gem: Boost [{guild.premium_subscription_count}]", value= f"Tier: ** {guild.premium_tier}**")
        try:
            vanity =  await guild.vanity_invite()
            embed.add_field(name=":link: Vanity URL", value=f"`{str(vanity).replace('https://discord.gg/', '')}`")
        except:embed.add_field(name=":link: Vanity URL", value=f"`None`")        
        embed.add_field(name= ":grinning: Emoji", value= f"Emojis: **{len(emojis)}**\nStickers: **{len(stickers)}**")
        embed.add_field(name= f":busts_in_silhouette: Members [{guild.member_count}]", 
                value= f"User: **{str(sum(1 for member in guild.members if not member.bot))}**\nBot: **{str(sum(1 for member in guild.members if member.bot))}**\nOnline: **{len(online)}**")
        embed.add_field(name= f":speech_left: Channels [{tchannels+vchannels}]", 
                value= f"Text: **{tchannels}**\nVoice: **{vchannels}**\nCategory: **{len(guild.categories)}**",inline= True)
        embed.set_footer(text= f"By: {str(interaction.author)}")
        await interaction.respond(embed=embed)

    @commands.slash_command(name="server_splash", description="サーバーの招待背景を表示")
    async def invite_iplash(self, interaction):
        try:await interaction.respond(embed=discord.Embed().set_image(url=interaction.guild.splash))
        except:interaction.respond("Error")

    @commands.slash_command(name="track", description="現在アクティビティにあるSpotifyの楽曲のURLを送信")
    async def track(self, interaction:discord.Interaction, user:discord.Member=None):
        if not user: user=interaction.author
        spotify_result = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
        if not spotify_result:await interaction.response.send_message(f"{user.name} is not listening to Spotify!")
        else:await interaction.response.send_message(f"> https://open.spotify.com/track/{spotify_result.track_id}")

    @commands.slash_command(name="spotify", description="アクティビティからSpotifyの楽曲情報を送信")
    async def spotify(self, ctx, user:discord.Member=None):
        if not user:user=ctx.author
        _spotify_result= next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
        if not _spotify_result:await ctx.respond(f"{user.name} is not listening to Spotify!")
        else:
            embed=discord.Embed(color=_spotify_result.color)
            embed.set_thumbnail(url=_spotify_result.album_cover_url)
            embed.add_field(name="Song Title", value=f"```{_spotify_result.title}```", inline=False)
            artists = _spotify_result.artists
            if not artists[0]: re_result=_spotify_result.artist
            else: re_result = ', '.join(artists)
            embed.add_field(name="Artist[s]", value=f"```{re_result}```")
            embed.add_field(name="Album", value=f"```{_spotify_result.album}```")
            embed.add_field(name="Time", value=f"```{dateutil.parser.parse(str(_spotify_result.duration)).strftime('%M:%S')}```", inline=False)
            embed.set_footer(text=f"By: {str(ctx.author)}")
            b = Button(label="URL", style=discord.ButtonStyle.green, emoji="<:App_logo_spotify_p:1007557495436365905>")
            jacket = Button(label="see jacket", style=discord.ButtonStyle.blurple, emoji="<:Icon_api:1007536617470312509>")#, row=1
            view = View()
            view.add_item(b)
            view.add_item(jacket)
            async def Button_1_callback(interaction:discord.Interaction):
                b.disabled=True
                await interaction.response.send_message(f"https://open.spotify.com/track/{_spotify_result.track_id}")
            async def Button_callback(interaction:discord.Interaction):
                await interaction.response.send_message(_spotify_result.album_cover_url, ephemeral=True)
            jacket.callback = Button_callback
            b.callback = Button_1_callback
            await ctx.respond(embed=embed, view=view)

    @commands.slash_command(name="spotify_songs_search", description="Spotify楽曲を検索・・・日本語だとたまにエラー出る")
    async def search(selfd, interaction, *, keyword):
        result = sp.search(q=keyword, limit=5)
        e = discord.Embed(color=c.s_c)
        for track in enumerate(result['tracks']['items']):
            song_title = track['name']
            song_url = track['external_urls']['spotify']
            e.add_field(name = f"{song_title} [{track['album']['name']}] - {track['artists'][0]['name']}", value= f"-[Jumo to song]({song_url})", inline=False)
        await interaction.respond(embed=e)

    @commands.slash_command(name="原神聖遺物スコア計算", desciption="小数点も要する")
    async def clac_score(senf, interaction:discord.Interaction,
            会心率:Option(float,"会心率 / Membership rate")=None,
            会心ダメージ:Option(float, "会心ダメージ / Membership rate")=None,
            攻撃_防御力:Option(float, "攻撃力 or 防御力 / ATK or DEF")=None,
            聖遺物:Option(str, "聖遺物を選択してください / Choice your Artifacts" ,choices=["花/羽/杯", "時計/冠"] )=None
        ):
        msg = await interaction.respond("<a:Loading_6:1012760935343063050>")
        if not 攻撃_防御力: 攻撃_防御力=0
        if not 会心ダメージ:会心ダメージ=0
        if not 会心率:会心率=0
        score = 攻撃_防御力 + (会心率 * 2) + 会心ダメージ

        e = discord.Embed(description=f"**スコア** : **{round(score, 1)}**\n\n> 会心率```{会心率} %```\n> 会心ダメージ```{会心ダメージ} %```\n> 攻撃力・防御力```{攻撃_防御力} %```", color=0x6dc1d1)
        e.set_footer(text="20Lv想定でサブスコアのみ計算してます | Beta ver")
        if not 聖遺物:pass
        else:
            if 聖遺物 in ("時計/冠"):
                if score >= 30:e.title="時計/冠 -合格"
                else:e.title="時計/冠 -カスコアやんけ捨てろよwww"
            else:
                if score >= 50:e.title="花/羽/杯 -合格"
                else:e.title="花/羽/杯 -カスコアやんけ捨てろよwww"
        await msg.edit_original_message(content=None,embed=e)


    """十字軍・深夜祭コマンド"""
    @commands.slash_command(name="タイプ別憤死")
    async def type_funshi(self, interaction):
        await interaction.respond("""**典型的憤死パターン** <:emoji_15:1004313871705702441>\n
        **1.発狂型憤死**
        明らかに劣勢な状態になってから露骨に発作を起こしキチガイムーヴを始めるタイプ。
        ネタに走って有耶無耶にしようという意図が見え見えである。

        **2.生存本能型憤死**
        生存本能タイムアウト/ブロック/ミュート/BANを行うタイプ。
        憤死回避のために実力行使を行ってしまったが故の行動である。

        **3.糖質化型憤死**
        明らかな決めつけや思い込みをし始め勝手に憤慨し続けるタイプ。
        \*\*\*の圧倒的煽りによって極度のストレスを受けた故の行動である。

        **4.ノーダメアピール型憤死**
        ノーダメアピールを繰り返し精神的勝利を訴え続けるタイプ。
        トマトフェイスを隠しきれていないため周りから見ると滑稽である。

        **5.スルー型憤死**
        突然話題を変えることで露骨にスルーアピールをするタイプ。
        指摘されるとすぐ必死になって否定をしてくることが多い。

        [十字軍に行く](https://discord.gg/aKyTHXZC)""")

    @commands.slash_command(name="憤死ワード")
    async def word_list(self, interaction):
        await interaction.respond("""**典型的憤死ワード集** <:emoji_15:1004313871705702441>
        ・荒らしで時間無駄にしてて草
        ・しょうもないことして楽しい？
        ・BANすればいいだけ 残念だったな
        ・ムカつくから黙れ
        ・学歴しか誇れないゴミで草
        ・楽しんでて哀れ
        ・暇つぶし楽しかったよ
        ・学歴と頭脳は比例しない
        ・あーもうこいつうるさいから蹴ろう
        ・誤字してて草
        ・十字軍はくだらない組織
        ・あそんでいるだけなんだが？

        [十字軍に行く](https://discord.gg/aKyTHXZC)""") 

    @commands.slash_command(name="yufu_yt", description="香港人Yufuさんの勝手に切り抜きした動画リンクを送信。")
    async def yufu_yt(self, interaction:discord.Interaction,
        movie:Option(str, "選んでください", choices=["ほんこんじん（編集済み）", "YUFUダイジェスト"])):
        if int(interaction.author.id) in c._users:
            await interaction.response.send_message("勝手に切り抜いてごめんなさい＞＜", ephemeral=True)
        if movie in ("ほんこんじん（編集済み）"):await interaction.response.send_message("https://youtu.be/pP_rrVc0KKY")
        else:await interaction.response.send_message("https://youtu.be/rKb0jmfE020")

def setup(bot):
    return bot.add_cog(Sub(bot))
