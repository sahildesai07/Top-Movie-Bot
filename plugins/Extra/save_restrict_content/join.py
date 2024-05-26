from pyrogram.errors import FloodWait, InviteHashInvalid, InviteHashExpired, UserAlreadyParticipant
from pyrogram import Client, filters
from info import *
from utils import temp 

@Client.on_message(filters.private & filters.command('join'))
async def join_command(bot, message):
    if SAVE_RESTRICTED_MODE == False:
        return 
    await bot.send_message(message.chat.id, "**Now Send Me Your Channel Invite Link From Where You Want To Save The Restricted Content.**")


async def join(message, invite_link):
    if SAVE_RESTRICTED_MODE == False:
        return 
    try:
        client = Client("saverestricted", session_string=SESSION_STRING, api_hash=API_HASH, api_id=API_ID)
        await client.connect()
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
    
