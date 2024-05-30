from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest
from info import AUTO_APPROVE_MODE, AUTH_CHANNEL
from database.users_chats_db import db
from database.join_reqs import JoinReqs

join_db = JoinReqs

@Client.on_chat_join_request((filters.group | filters.channel))
async def auto_approve(client, message: ChatJoinRequest):
    if message.chat.id == AUTH_CHANNEL:
        if join_db().isActive():
            user_id = message.from_user.id
            first_name = message.from_user.first_name
            username = message.from_user.username
            date = message.date
            await join_db().add_user(user_id=user_id, first_name=first_name, username=username, date=date)
            return 
    if AUTO_APPROVE_MODE == True:
        if not await db.is_user_exist(message.from_user.id):
            await db.add_user(message.from_user.id, message.from_user.first_name)
        chat = message.chat 
        user = message.from_user  
        await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
        text = f"<b>ʜᴇʟʟᴏ {message.from_user.mention} 👋,\n\nʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ {message.chat.title} ɪs ᴀᴘᴘʀᴏᴠᴇᴅ.\n\nᴘᴏᴡᴇʀᴇᴅ ʙʏ - @VJ_Botz</b>"
        await client.send_message(chat_id=user.id, text=text)
