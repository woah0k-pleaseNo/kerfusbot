from assets.kerfusbrainonsmartboosters import increment_user_data, embed_create
from discord import FFmpegPCMAudio, Color
from discord.ext import commands
from random import randrange
from sqlite3 import connect
from asyncio import run
from os import listdir



class KerfusMindMachine(commands.Cog): # handles audio/vc stuff etc.
    def __init__(self, bot):
        self.bot = bot
        self.vc = None
        self.songs = listdir('assets/audio/songs')
        self.singing = False
        self.selfies = listdir('assets/images/selfies')


    async def play_song(self, ctx):
        if self.singing:
            random_song = self.songs[randrange(0, len(self.songs))]
            self.vc.play(FFmpegPCMAudio(f'assets/audio/songs/{random_song}'), after=lambda _: run(self.play_song(ctx)))
            await embed_create(self.bot, ctx, "Meow!", f"Kerfus is now singing {random_song[:random_song.find('.mp3')]}", thumbnail='assets/images/kerfuspet.png')


    @commands.Cog.listener()
    async def on_ready(self):
        print("Kerfus' brain has been found. (kerfusmindmachine cog has worked)")


    @commands.command(aliases=['p', 'play', 'sing'])
    async def sing_command(self, ctx):
        # join vc
        if ctx.author.voice and (self.vc == None or not self.vc.is_connected()):
            self.vc = await ctx.message.author.voice.channel.connect()
        elif (self.vc != None and self.vc.is_connected()):
            await self.vc.move_to(ctx.message.author.voice.channel)
        else:
            await embed_create(self.bot, ctx, "Kerfus can't find you! o(≧口≦)o", "You need to be in a voice channel so that Kerfus can join you!", thumbnail='assets/images/kerfuserror.png', clr=Color.red())
            increment_user_data(ctx, 'friendship', -5)
            return None
        
        # play random song
        if (self.vc != None and self.vc.is_connected) and not self.vc.is_playing():
            self.singing = True
            await self.play_song(ctx)
            increment_user_data(ctx, 'friendship', 5)
        else:
            await embed_create(self.bot, ctx, "Kerfus is in the middle of something, don't interrupt! ヽ（≧□≦）ノ", "Kerfus is in the middle of something, please either stop him or wait for him to finish.", thumbnail='assets/images/kerfuserror.png', clr=Color.red())
            increment_user_data(ctx, 'friendship', -5)
    

    @commands.command(aliases=['stop', 'shutup', 'idontwanttohearyou', 'shutyourselfup', 'youloudmouth'])
    async def stop_command(self, ctx):
        if (self.vc != None and self.vc.is_connected()) and self.vc.is_playing() and self.singing:
            self.singing = False
            self.vc.stop()
            shutups = increment_user_data(ctx, 'shutups', 1)
            await embed_create(self.bot, ctx, "How cruel...", f"{ctx.author.mention} was mean to Kerfus and made him stop singing!\n{ctx.author.mention} has already told Kerfus to shut up {shutups} time\s", thumbnail='assets/images/kerfuserror.png')
            increment_user_data(ctx, 'friendship', -5)
        else:
            await embed_create(self.bot, ctx, "Who're you telling to shut up! Kerfus isn't saying anything! *( ￣皿￣)", "Kerfus needs to be playing a sound before you can stop him from doing so.", thumbnail='assets/images/kerfuserror.png', clr=Color.red())
            increment_user_data(ctx, 'friendship', -5)
    

    @commands.command(aliases=['skip', 's', 'forward', 'nextoneplease', 'wedontlikethisone'])
    async def skip_command(self, ctx):
        if (self.vc != None and self.vc.is_connected()) and self.vc.is_playing() and self.singing:
            self.vc.stop()
            await embed_create(self.bot, ctx, "Kerfus is a little bummed...", f"{ctx.author.mention} asked Kerfus to sing another song, even though Kerfus wanted to sing that song! He chose it himself...", thumbnail='assets/images/kerfuserror.png')
            increment_user_data(ctx, 'friendship', -5)
        else:
            await embed_create(self.bot, ctx, "Who're you yelling at! Kerfus isn't doing anything! *( ￣皿￣)", "Kerfus needs to be singing something before you can skip a song.", thumbnail='assets/images/kerfuserror.png', clr=Color.red())
            increment_user_data(ctx, 'friendship', -5)
    

    @commands.command(aliases=['songs', 'list', 'songlist', 'listsongs'])
    async def list_command(self, ctx):
        song_list = f"```The list of {len(self.songs)} songs which Kerfus can sing:\n"
        for s in self.songs:
            song_list += s[:s.find(".mp3")]+"\n"
        await ctx.send(song_list+"```")


    @commands.command(aliases=['join', 'pet', 'pat'])
    async def join_command(self, ctx):
        # join vc
        if ctx.author.voice and (self.vc == None or not self.vc.is_connected()):
            self.vc = await ctx.message.author.voice.channel.connect()
        elif self.vc != None and self.vc.is_connected():
            await self.vc.move_to(ctx.message.author.voice.channel)
        else:
            await embed_create(self.bot, ctx, "Kerfus can't find you! o(≧口≦)o", "You need to be in a voice channel so that Kerfus can join you!", thumbnail='assets/images/kerfuserror.png', clr=Color.red())
            increment_user_data(ctx, 'friendship', -5)
            return None
        
        # meow
        if (self.vc != None and self.vc.is_connected()) and not self.vc.is_playing():
            self.vc.play(FFmpegPCMAudio('assets/audio/kerfusmeow.mp3'))
            pets = increment_user_data(ctx, 'pets', 1)
            await embed_create(self.bot, ctx, "Meow!", f"{ctx.author.mention} pet Kerfus!\n{ctx.author.mention} has pet Kerfus {pets} time\s!", thumbnail='assets/images/kerfuspet.png')
            increment_user_data(ctx, 'friendship', 5)
        else:
            await embed_create(self.bot, ctx, "Kerfus is in the middle of something, don't interrupt! ヽ（≧□≦）ノ", "Kerfus is in the middle of something, please either stop him or wait for him to finish.", thumbnail='assets/images/kerfuserror.png', clr=Color.red())
            increment_user_data(ctx, 'friendship', -5)


    @commands.command(aliases=['leave', 'getout', 'die'])
    async def leave_command(self, ctx):
        if (self.vc != None and self.vc.is_connected()) and self.singing:
            self.singing = False
            await ctx.guild.voice_client.disconnect()
            await embed_create(self.bot, ctx, "So mean...", f"{ctx.author.mention} was mean to Kerfus and made him leave!", thumbnail='assets/images/kerfuserror.png')
            increment_user_data(ctx, 'friendship', -5)
        elif (self.vc != None and self.vc.is_connected()) and not self.singing:
            await ctx.guild.voice_client.disconnect()
            await embed_create(self.bot, ctx, "So mean...", f"{ctx.author.mention} was mean to Kerfus and made him leave!", thumbnail='assets/images/kerfuserror.png')
            increment_user_data(ctx, 'friendship', -5)
        else:
            await embed_create(self.bot, ctx, "Kerfus isn't in a VC! Don't lie to Kerfus! (╬▔皿▔)╯", "Kerfus needs to be in a voice channel before he can leave one.", "assets/images/kerfuserror.png", clr=Color.red())
            increment_user_data(ctx, 'friendship', -5)
    

    @commands.command(name='selfie')
    async def selfie_command(self, ctx):
        random_image = self.selfies[randrange(0, len(self.selfies))]
        await embed_create(self.bot, ctx, "Kerfus took a selfie!", "Here it is...", img=f'assets/images/selfies/{random_image}')
    

    @commands.command(aliases=['mood', 'howareyoufeelingrightnow?'])
    async def mood_command(self, ctx):
        # getting mood sum
        connection = connect('assets/kerfusmemorymachine.db')
        cursor = connection.cursor()
        with connection:
            cursor.execute("SELECT friendship FROM users")
            all_friendship = []
            for t in cursor.fetchall():
                all_friendship.append(t[0])
        mood = sum(all_friendship)

        # beautiful elif statement love hearts in my eyes
        if mood in range(-50, 51):
            mood = "neutral."
        elif mood in range(51, 101):
            mood = "well!"
        elif mood in range(101, 151):
            mood = "good!!"
        elif mood in range(151, 201):
            mood = "great!!!"
        elif mood > 200:
            mood = "ecstatic!!!!"
        elif mood in range(-51, -101, -1):
            mood = "down."
        elif mood in range(-101, -151, -1):
            mood = "sad.."
        elif mood in range(-151, -201, -1):
            mood = "depressed..."
        elif mood < -200:
            mood = "desolate...."
        await embed_create(self.bot, ctx, "Kerfus wants to talk about his feelings... (✿◡‿◡)", f"Kerfus is currently feeling {mood}", thumbnail='assets/images/kerfusfacedefault.png')



async def setup(bot):
    await bot.add_cog(KerfusMindMachine(bot))