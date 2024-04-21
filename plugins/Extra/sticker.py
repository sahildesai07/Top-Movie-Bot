from pyrogram import Client, filters

@Client.on_message(filters.command("stickerid") & filters.private)
async def stickerid(bot, message):   
    if message.reply_to_message.sticker:
        await message.reply_text(f"**Sticker ID is**  \n `{message.reply_to_message.sticker.file_id}` \n \n ** Unique ID is ** \n\n`{message.reply_to_message.sticker.file_unique_id}`")
    else: 
        await message.reply_text("Oops !! Not a sticker file")
