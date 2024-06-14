import discord
from discord.ext import commands
from random import randrange
from os import listdir
from kerfusbrainonsmartboosters import *

bot = commands.Bot(command_prefix="-kerfus:",intents=discord.Intents.all(),help_command=None)


kerfussounds = KerfusSounds()

# Kerfus events/commands
@bot.event # starts when kerfus turns on
async def on_ready():
    print("-----------------\nKerfus has risen!\n-----------------")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="the sounds of the Swiss wilderness."))

@bot.command(aliases=["pet", "pat"]) # pet kerfus
async def pet_command(ctx):
    await kerfussounds.join_vc(ctx)
    await kerfussounds.play_sound(ctx)

@bot.command(aliases=["sing", "play", "p"]) # make kerfus sing
async def sing_command(ctx):
    await kerfussounds.join_vc(ctx)
    await kerfussounds.play_sound(ctx, sound="SONG")

@bot.command(name="shutup") # be mean to kerfus and stop him from singing
async def stop_command(ctx):
    await kerfussounds.stop_sound(ctx)

@bot.command(aliases=["songs", "list", "songlist", "listsongs"]) # list the songs which kerfus can sing
async def songs_command(ctx):
    songlist = f"```The list of {len(kerfussounds.songs)} songs which Kerfus can sing:\n"
    for i in kerfussounds.songs:
        songlist += i[:i.find(".mp3")]+"\n"
    await ctx.send(songlist+"```")

@bot.command(aliases=["leave", "getout", "die"]) # be mean to kerfus and make him leave vc
async def leave_command(ctx):
    await kerfussounds.leave_vc(ctx)

@bot.command(name="selfie") # get kerfus to send a selfie
async def selfie_command(ctx):
    randimage = listdir("assets/images/kerfusselfie")[randrange(0, len(listdir("assets/images/kerfusselfie"))-1)]
    await embed_create(ctx, title="Kerfus took a selfie!", desc="Here it is...", img=f"assets/images/kerfusselfie/{randimage}")

@bot.command(name="off") # turn kerfus off
async def off_command(ctx):
    await embed_create(ctx, title="Kerfus is getting a little sleepy...", desc=f"{ctx.author.mention} turned Kerfus off.", thumbnail="assets/images/kerfusoff.png")
    await bot.close()

@bot.command(name="help") # learn the kerfus ways
async def help(ctx):
    helpstring: str = """```
    Commands:
    - 'pet'/'pat': You pet Kerfus, which forces him into your voice channel.
    - 'sing'/'play'/'p': Make Kerfus sing a random Meowsynth song (except for that one non-Meowsynth song), also forces him into VC.
    - 'songs'/'list'/'songlist'/'listsongs': List all available songs which Kerfus can randomly choose from.
    - 'leave'/'getout'/'die': Kicks Kerfus out of your voice channel.
    - 'shutup': You are mean to Kerfus and it makes him stop singing.
    - 'selfie': Sends a random image of Kerfus
    - 'off': Turns off the bot. Like, I have to turn it back on manually, so don't do this.

    
    - Brought to you by your beloved, R 'brbrbrbr' D.
    ```"""
    await ctx.send(helpstring)


bot.run("put the token here")