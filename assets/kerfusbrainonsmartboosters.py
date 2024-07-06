from asyncio import run_coroutine_threadsafe
from discord import Embed, File, Color
from sqlite3 import connect



def increment_user_data(ctx, column: str, increment: int)->int:
    connection = connect('assets/kerfusmemorymachine.db')
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT * FROM users WHERE id=:id", {'id': ctx.author.id})
        all_data = cursor.fetchall()
        if len(all_data) < 1:
            cursor.execute("INSERT INTO users VALUES (:id, 0, 0, 0)", {'id': ctx.author.id})
        cursor.execute(f"SELECT {column} FROM users WHERE id=:id", {'id': ctx.author.id})
        data = cursor.fetchone()
        cursor.execute(f"UPDATE users SET {column}=:increment WHERE id=:id", {'increment': data[0]+increment, 'id': ctx.author.id})
        return data[0]+increment


async def embed_create(bot, ctx, embtitle: str, desc: str, *, thumbnail: str = None, img: str = None, clr = Color.blue()):
        embmsg = Embed(title=embtitle, description=desc, color=clr)
        if thumbnail != None:
            thumbnailimg = File(thumbnail, filename=thumbnail[thumbnail.find('images/')+len('images/'):])
            embmsg.set_thumbnail(url=f"attachment://{thumbnail[thumbnail.find('images/')+len('images/'):]}")
            run_coroutine_threadsafe(ctx.send(file=thumbnailimg, embed=embmsg), bot.loop)
        if img != None:
            image = File(img, filename=img[img.find('selfies/')+len('selfies/'):])
            embmsg.set_image(url=f"attachment://{img[img.find('selfies/')+len('selfies/'):]}")
            run_coroutine_threadsafe(ctx.send(file=image, embed=embmsg), bot.loop)