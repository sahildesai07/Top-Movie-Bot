from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest
from info import AUTO_APPROVE_MODE
from database.users_chats_db import db

@Client.on_chat_join_request((filters.group | filters.channel))
async def auto_approve(client, message: ChatJoinRequest):
    if AUTO_APPROVE_MODE == True:
        if not await db.is_user_exist(message.from_user.id):
            await db.add_user(message.from_user.id, message.from_user.first_name)
        chat = message.chat 
        user = message.from_user  
        await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
        text = f"<b>ʜᴇʟʟᴏ {message.from_user.mention} 👋,\n\nʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ {message.chat.title} ɪs ᴀᴘᴘʀᴏᴠᴇᴅ.\n\nᴘᴏᴡᴇʀᴇᴅ ʙʏ - @VJ_Botz</b>"
        await client.send_message(chat_id=user.id, text=text)
