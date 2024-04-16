# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

from pyrogram import Client, filters, enums
from database.users_chats_db import db

@Client.on_message(filters.private & filters.command(['view_thumb']))
async def viewthumb(client, message):    
    thumb = await db.get_thumbnail(message.from_user.id)
    if thumb:
        await client.send_photo(
	    chat_id=message.chat.id, 
	    photo=thumb)
    else:
        await message.reply_text("😔**Sorry ! No thumbnail found...**😔") 
		
@Client.on_message(filters.private & filters.command(['del_thumb']))
async def removethumb(client, message):
    await db.set_thumbnail(message.from_user.id, file_id=None)
    await message.reply_text("**Thumbnail deleted successfully**✅️")
	
@Client.on_message(filters.private & filters.command(['set_thumb']))
async def addthumbs(client, message):
    thumb = await client.ask(message.chat.id, "**Send me your thumbnail**")
    if thumb.media and thumb.media == enums.MessageMediaType.PHOTO:
	await db.set_thumbnail(message.from_user.id, file_id=thumb.photo.file_id)
	await message.reply("**Thumbnail saved successfully**✅️")
    else:
	await message.reply("**This is not a picture**")
	
