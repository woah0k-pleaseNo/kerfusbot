import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from random import randrange
from os import listdir


# Function for creating embeds so that my life becomes 121% easier very nice ヾ(•ω•`)o
async def embed_create(ctx, title: str = None, desc: str = None, thumbnail: str = None, img: str = None, clr: discord = discord.Color.blue()):
    embmsg = discord.Embed(title=title, description=desc, color=clr)
    
    if thumbnail != None:
        thumbnailimg = discord.File(thumbnail, filename=thumbnail[thumbnail.find("images/")+7:])
        embmsg.set_thumbnail(url=f"attachment://{thumbnail[thumbnail.find('images/')+7:]}")
        await ctx.send(file=thumbnailimg, embed=embmsg)
    
    if img != None:
        image = discord.File(img, filename=img[img.find("kerfusselfie/")+13:])
        embmsg.set_image(url=f"attachment://{img[img.find('kerfusselfie/')+13:]}")
        await ctx.send(file=image, embed=embmsg)

# Sound class for storing/playing sounds
class KerfusSounds:
    def __init__(self):
        self.meow = "assets/audio/kerfusmeow.mp3"
        self.songs = listdir("assets/audio/kerfussing")
        self.vc = None
    
    async def join_vc(self, ctx): # forces kerfus to join vc
        if ctx.author.voice: # runs if author is in a vc
            if self.vc == None or not self.vc.is_connected(): # runs if kerfus is not in a vc
                self.vc = await ctx.message.author.voice.channel.connect() # kerfus joins vc
                if self.vc == None or not self.vc.is_connected(): # runs if kerfus is still not in vc
                    print("hey! couldnt join vc")
            else:
                await self.vc.move_to(ctx.message.author.voice.channel) # kerfus moves vc
        else:
            await embed_create(ctx, title="Kerfus can't find you! o(≧口≦)o", desc="You need to be in a voice channel so that Kerfus can join you!", thumbnail="assets/images/kerfuserror.png", clr=discord.Color.red())

    async def leave_vc(self, ctx): # forces kerfus out of vc
        if self.vc != None and self.vc.is_connected():
            await ctx.guild.voice_client.disconnect()
            await embed_create(ctx, title="So mean...", desc=f"{ctx.author.mention} was mean to Kerfus and made him leave!", thumbnail="assets/images/kerfuserror.png")
        else:
            await embed_create(ctx, title="Kerfus isn't in a VC! Don't lie to Kerfus! (╬▔皿▔)╯", desc="Kerfus needs to be in a voice channel before he can leave one.", thumbnail="assets/images/kerfuserror.png", clr=discord.Color.red())

    async def play_sound(self, ctx, sound: str = "MEOW"): # kerfus plays chosen sound if in vc
        if self.vc != None or self.vc.is_connected(): # check if kerfus is in vc
            try: # to catch the error it gives when trying to play audio when there is already is audio playing
                if sound == "MEOW":
                    self.vc.play(FFmpegPCMAudio(self.meow))
                    await embed_create(ctx, title="Meow!", desc=f"{ctx.author.mention} pet Kerfus!", thumbnail="assets/images/kerfuspet.png")
                elif sound == "SONG":
                    randsong = self.songs[randrange(0, len(self.songs)-1)]
                    self.vc.play(FFmpegPCMAudio(f"assets/audio/kerfussing/{randsong}"))
                    await embed_create(ctx, title="Meow!", desc=f"{ctx.author.mention} asked Kerfus to sing!\nKerfus is now singing {randsong[:randsong.find('.mp3')]}", thumbnail="assets/images/kerfuspet.png")
                else:
                    print("not viable sound")
            except:
                await embed_create(ctx, title="Kerfus is in the middle of something, don't interrupt! ヽ（≧□≦）ノ", desc="Kerfus is in the middle of something, please either stop him or wait for him to finish.", thumbnail="assets/images/kerfuserror.png", clr=discord.Color.red())
        else:
            print("bot was not in vc")
    
    async def stop_sound(self, ctx): # stops sound if playing
        if self.vc.is_playing():
            self.vc.stop()
            await embed_create(ctx, title="How cruel...", desc=f"{ctx.author.mention} was mean to Kerfus and made him stop singing!", thumbnail="assets/images/kerfuserror.png")
        else:
            await embed_create(ctx, title="Who're you telling to shut up! Kerfus isn't saying anything! *( ￣皿￣)", desc="Kerfus needs to be playing a sound before you can stop him from doing so.", thumbnail="assets/images/kerfuserror.png", clr=discord.Color.red())