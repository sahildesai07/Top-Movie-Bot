# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

from pyrogram import Client, filters 
from database.users_chats_db import db

@Client.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
    caption = await client.ask(message.chat.id, "**__𝙶𝚒𝚟𝚎 𝚖𝚎 𝚊 𝚌𝚊𝚙𝚝𝚒𝚘𝚗 𝚝𝚘 𝚜𝚎𝚝.__\n\nFormat:- `{filename}`\n\n💾 Size: `{filesize}`\n\n⏰ Duration: `{duration}`**")
    await db.set_caption(message.from_user.id, caption=caption.text)
    await message.reply_text("__**✅ 𝚈𝙾𝚄𝚁 𝙲𝙰𝙿𝚃𝙸𝙾𝙽 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝚂𝙰𝚅𝙴𝙳**__")

    
@Client.on_message(filters.private & filters.command('del_caption'))
async def delete_caption(client, message):
    caption = await db.get_caption(message.from_user.id)  
    if not caption:
       return await message.reply_text("😔**Sorry ! No Caption found...**😔")
    await db.set_caption(message.from_user.id, caption=None)
    await message.reply_text("**Your Caption deleted successfully**✅️")
                                       
@Client.on_message(filters.private & filters.command('see_caption'))
async def see_caption(client, message):
    caption = await db.get_caption(message.from_user.id)  
    if caption:
       await message.reply_text(f"**Your Caption:-**\n\n`{caption}`")
    else:
       await message.reply_text("😔**Sorry ! No Caption found...**😔")
