from pyrogram.errors import FloodWait, InviteHashInvalid, InviteHashExpired, UserAlreadyParticipant
from pyrogram import Client, filters
from info import SAVE_RESTRICTED_MODE

@Client.on_message(filters.private & filters.command('join'))
async def join(bot, message):
    if SAVE_RESTRICTED_MODE == False:
        return 
    invite_link = await bot.ask(message.chat.id, "**Now Send Me Your Channel Invite Link From You Want To Save Restricted Content.**")
    if not 't.me/+' in invite_link:
        return 
    try:
    #    client = ......userbot
        await client.join_chat(invite_link)
        return await message.reply("Successfully joined the Channel")
    except UserAlreadyParticipant:
        return await message.reply("User is already a participant.")
    except (InviteHashInvalid, InviteHashExpired):
        return await message.reply("Could not join. Maybe your link is expired or Invalid.")
    except FloodWait:
        return await message.reply("Too many requests, try again later.")
    except Exception as e:
        print(e)
        return await message.reply("Could not join, try joining manually.")
    
