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


async def embed_create(bot, ctx, emb_title: str, desc: str, *, thumbnail: str = None, img: str = None, clr = Color.blue()):
        embmsg = Embed(title=emb_title, description=desc, color=clr)
        if thumbnail != None:
            thumbnailimg = File(thumbnail, filename=thumbnail.split('/')[-1])
            embmsg.set_thumbnail(url=f"attachment://{thumbnail.split('/')[-1]}")
            run_coroutine_threadsafe(ctx.send(file=thumbnailimg, embed=embmsg), bot.loop)
        if img != None:
            image = File(img, filename=img.split('/')[-1])
            embmsg.set_image(url=f"attachment://{img.split('/')[-1]}")
            run_coroutine_threadsafe(ctx.send(file=image, embed=embmsg), bot.loop)