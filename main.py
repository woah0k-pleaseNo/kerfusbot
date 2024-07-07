import discord
from discord.ext import commands
from sqlite3 import connect
from os.path import isfile
from asyncio import run

if isfile('token'):
    with open('token', 'r') as f:
        token = f.read()
else:
    with open('token', 'w') as f:
        f.write("please replace all this text and put your bot token here (ToT)/~~~ (also please turn your priveleged gateway intents on)")

bot = commands.Bot(command_prefix="-kerfus:", intents=discord.Intents.all(), help_command=None)
run(bot.load_extension(f'assets.kerfusmindmachine'))

connection = connect('assets/kerfusmemorymachine.db')
cursor = connection.cursor()
with connection:
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                   id integer, pets integer, shutups integer, friendship integer)""")



@bot.event # starts when kerfus turns on
async def on_ready():
    print("-----------------\nKerfus has risen!\n-----------------")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="the sounds of the Swiss wilderness."))


@bot.command(name='help')
async def help(ctx):
    help_string = """```
    Commands:
    - 'pet'/'pat'/'join': You pet Kerfus, which forces him into your voice channel.
    - 'leave'/'getout'/'die': Kicks Kerfus out of your voice channel.
    - 'sing'/'play'/'p': Make Kerfus sing a random Meowsynth song (except for that one non-Meowsynth song), also forces him into VC.
    - 'skip'/'s'/'forward': Makes Kerfus sing a new random Meowsynth song.
    - 'shutup': You are mean to Kerfus and it makes him stop singing.
    - 'songs'/'list'/'songlist'/'listsongs': List all available songs which Kerfus can randomly choose from.
    - 'selfie': Sends a random image of Kerfus.
    - 'mood': Makes Kerfus talk about his feelings.

    
    - Brought to you by, your beloved, R 'brbrbrbr' D.
    ```"""
    await ctx.send(help_string)



try:
    bot.run(token)
except discord.errors.LoginFailure:
    print("You're going to need a valid Discord bot token. Please put a bot token into the 'token' file, found in the same directory as the 'main.py' file.")
except NameError:
    print("The, once missing, 'token' file has just been made, please put your Discord bot token in it.")
