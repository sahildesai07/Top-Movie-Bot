import os, asyncio, time, math, json, re
from pyrogram.errors import FloodWait
from pyrogram.types import Message 
from database.users_chats_db import db
from pyrogram import Client, filters, enums
from pyrogram.errors import ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid, PeerIdInvalid
from pyrogram.enums import MessageMediaType
from ethon.telefunc import fast_upload
from telethon.tl.types import DocumentAttributeVideo
from utils import temp
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from info import SAVE_RESTRICTED_MODE

MAX = 2 * 1024 * 1024 * 1024
FINISHED_PROGRESS_STR = "🟨"
UN_FINISHED_PROGRESS_STR = "⬜"
DOWNLOAD_LOCATION = "/app"


@Client.on_message(filters.private & filters.command(['cancel_save']))
async def cancel_save(client: Client, message: Message):
    if SAVE_RESTRICTED_MODE == False:
        return 
    update = message.from_user.id
    save = await db.get_save(update)
    if save == False:
        return await message.reply("**No Task Found.**")
    await db.set_save(update, save=False)
    await message.reply("**ᴅᴏɴᴇ.**")

@Client.on_message(filters.private & filters.command(['save']))
async def start_save(client: Client, message: Message):
    if SAVE_RESTRICTED_MODE == False:
        return 
    update = message.from_user.id
    save = await db.get_save(update)
    if save == True:
        return await message.reply("**ʏᴏᴜ'ᴠᴇ ᴀʟʀᴇᴀᴅʏ sᴛᴀʀᴛᴇᴅ ᴏɴᴇ ʙᴀᴛᴄʜ, ᴡᴀɪᴛ ғᴏʀ ɪᴛ ᴛᴏ ᴄᴏᴍᴘʟᴇᴛᴇ ʏᴏᴜ ᴅᴜᴍʙғᴜᴄᴋ ᴏᴡɴᴇʀ ❗**\n\n**Cancel Ongoing Task By - /cancel_save**")
    vj_link = await client.ask(update, "**sᴇɴᴅ ᴍᴇ ᴛʜᴇ ᴍᴇssᴀɢᴇ ʟɪɴᴋ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴛᴀʀᴛ sᴀᴠɪɴɢ ғʀᴏᴍ, ᴀs ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜɪs ᴍᴇssᴀɢᴇ.**")
    try:
        link = get_link(vj_link.text)
        if not link:
            return await vj_link.reply("**ɴᴏ ʟɪɴᴋ ғᴏᴜɴᴅ.**")
    except TypeError:
        return 
    _range = await client.ask(update, "**sᴇɴᴅ ᴍᴇ ᴛʜᴇ ɴᴜᴍʙᴇʀ ᴏғ ғɪʟᴇs/ʀᴀɴɢᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴀᴠᴇ ғʀᴏᴍ ᴛʜᴇ ɢɪᴠᴇɴ ᴍᴇssᴀɢᴇ, ᴀs ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜɪs ᴍᴇssᴀɢᴇ.**")
    try:
        value = int(_range.text)
        if value > 100:
            await _range.reply("**ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ ɢᴇᴛ ᴜᴘᴛᴏ 100 ғɪʟᴇs ɪɴ ᴀ sɪɴɢʟᴇ ʙᴀᴛᴄʜ.**")
            return
    except ValueError:
        await _range.reply("**ʀᴀɴɢᴇ ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ**")
    await db.set_save(update, save=True)
    await run_save(client, update, _link, value) 
    await db.set_save(update, save=False)

async def run_save(client, sender, link, _range):
    for i in range(_range):
        timer = 60
        if i < 25:
            timer = 5
        if i < 50 and i > 25:
            timer = 10
        if i < 100 and i > 50:
            timer = 20
        if not 't.me/c/' in link:
            if i < 25:
                timer = 5
            else:
                timer = 10
        try: 
            save = await db.get_save(sender)
            if batch == False:
                await client.send_message(sender, "**ʙᴀᴛᴄʜ ᴄᴏᴍᴘʟᴇᴛᴇᴅ.**")
                break
        except Exception as e:
            print(e)
            await client.send_message(sender, "**ʙᴀᴛᴄʜ ᴄᴏᴍᴘʟᴇᴛᴇᴅ.**")
            break
        try:
            await get_bulk_msg(client, sender, link, i) 
        except FloodWait as fw:
            if int(fw.x) > 299:
                await client.send_message(sender, "**ᴄᴀɴᴄᴇʟʟɪɴɢ ʙᴀᴛᴄʜ sɪɴᴄᴇ ʏᴏᴜ ʜᴀᴠᴇ ғʟᴏᴏᴅᴡᴀɪᴛ ᴍᴏʀᴇ ᴛʜᴀɴ 5 ᴍɪɴᴜᴛᴇs.**")
                break
            await asyncio.sleep(fw.x + 5)
            await get_bulk_msg(client, sender, link, i)
        protection = await client.send_message(sender, f"**sʟᴇᴇᴘɪɴɢ ғᴏʀ** `{timer}` **sᴇᴄᴏɴᴅs ᴛᴏ ᴀᴠᴏɪᴅ ғʟᴏᴏᴅᴡᴀɪᴛs ᴀɴᴅ ᴘʀᴏᴛᴇᴄᴛ ᴀᴄᴄᴏᴜɴᴛ**")
        await asyncio.sleep(timer)
        await protection.delete()
    await client.send_message(sender, "**ʙᴀᴛᴄʜ ᴄᴏᴍᴘʟᴇᴛᴇᴅ.**")

async def get_bulk_msg(client, sender, msg_link, i):
    x = await client.send_message(sender, text="**ᴘʀᴏᴄᴇssɪɴɢ ❗**")
    await get_msg(client, temp.TELETHON, sender, x.id, msg_link, i)

async def get_msg(client, bot, sender, edit_id, msg_link, i):
    edit = ""
    chat = ""
    round_message = False
    if "?single" in msg_link:
        msg_link = msg_link.split("?single")[0]
    msg_id = int(msg_link.split("/")[-1]) + int(i)
    height, width, duration, thumb_path = 90, 90, 0, None
    if ('t.me/c/' in msg_link) or ('t.me/b/' in msg_link):
        if 't.me/b/' in msg_link:
            chat = str(msg_link.split("/")[-2])
        else:
            chat = int('-100' + str(msg_link.split("/")[-2]))
        file = ""
        try:
            msg = await temp.USERBOT.get_messages(chat, msg_id)
            if msg.media:
                if msg.media==MessageMediaType.WEB_PAGE:
                    edit = await client.edit_message_text(sender, edit_id, "**ᴄʟᴏɴɪɴɢ.**")
                    await client.send_message(sender, msg.text.markdown)
                    await edit.delete()
                    return
            if not msg.media:
                if msg.text:
                    edit = await client.edit_message_text(sender, edit_id, "**ᴄʟᴏɴɪɴɢ.**")
                    await client.send_message(sender, msg.text.markdown)
                    await edit.delete()
                    return
            edit = await client.edit_message_text(sender, edit_id, "**ᴛʀʏɪɴɢ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ.**")
            if msg.media==MessageMediaType.VIDEO:
                if msg.video.file_size > MAX:
                    return await client.edit_message_text(sender, edit_id, f"**ғᴀɪʟᴇᴅ ᴛᴏ sᴀᴠᴇ:** `{msg_link}`\n\n**ᴇʀʀᴏʀ: Can't Upload File Bigger Than 2 GB**")
            if msg.media==MessageMediaType.VIDEO_NOTE:
                if msg.video_note.file_size > MAX:
                    return await client.edit_message_text(sender, edit_id, f"**ғᴀɪʟᴇᴅ ᴛᴏ sᴀᴠᴇ:** `{msg_link}`\n\n**ᴇʀʀᴏʀ: Can't Upload File Bigger Than 2 GB**")
            if msg.media==MessageMediaType.DOCUMENT:
                if msg.document.file_size > MAX:
                    return await client.edit_message_text(sender, edit_id, f"**ғᴀɪʟᴇᴅ ᴛᴏ sᴀᴠᴇ:** `{msg_link}`\n\n**ᴇʀʀᴏʀ: Can't Upload File Bigger Than 2 GB**")
           
            file = await temp.USERBOT.download_media(
                msg,
                progress=progress_for_pyrogram,
                progress_args=(
                    client,
                    "🖥️ **ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ:**\n",
                    edit,
                    time.time()
                )
            )
            print(file)
            await edit.edit('**ᴘʀᴇᴘᴀʀɪɴɢ ᴛᴏ ᴜᴘʟᴏᴀᴅ ❗**')
            caption=None
            if msg.caption is not None:
                caption = msg.caption
            VJ = True
            if VJ == True:
                try: 
                    if msg.media==MessageMediaType.VIDEO and msg.video.mime_type in ["video/mp4", "video/x-matroska"]:
                        UT = time.time()
                        uploader = await fast_upload(f'{file}', f'{file}', UT, bot, edit, '**ᴜᴘʟᴏᴀᴅɪɴɢ:**')
                        attributes = [DocumentAttributeVideo(duration=msg.video.duration, w=msg.video.width, h=msg.video.height, round_message=round_message, supports_streaming=True)] 
                        try:
                            thumb_path = await temp.USERBOT.download_media(msg.video.thumbs[0].file_id)
                        except:
                            thumb_path = None
                        await bot.send_file(sender, uploader, caption=caption, thumb=thumb_path, attributes=attributes, force_document=False)
                    elif msg.media==MessageMediaType.VIDEO_NOTE:
                        uploader = await fast_upload(f'{file}', f'{file}', UT, bot, edit, '**ᴜᴘʟᴏᴀᴅɪɴɢ:**')
                        attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, round_message=round_message, supports_streaming=True)] 
                        try:
                            thumb_path = await temp.USERBOT.download_media(msg.video_note.thumbs[0].file_id)
                        except:
                            thumb_path = None
                        await bot.send_file(chat_sender, uploader, caption=caption, thumb=thumb_path, attributes=attributes, force_document=False)
                    elif msg.media==MessageMediaType.PHOTO:
                        await edit.edit("**ᴜᴘʟᴏᴀᴅɪɴɢ ᴘʜᴏᴛᴏ.**")
                        await bot.send_file(sender, file, caption=caption)
                    else:
                        UT = time.time()
                        uploader = await fast_upload(f'{file}', f'{file}', UT, bot, edit, '**ᴜᴘʟᴏᴀᴅɪɴɢ:**')
                        try:
                            thumb_path = await temp.USERBOT.download_media(msg.document.thumbs[0].file_id)
                        except:
                            thumb_path = None
                        await bot.send_file(chat_sender, uploader, caption=caption, thumb=thumb_path, force_document=True)
                    if os.path.isfile(file) == True:
                        os.remove(file)
                except Exception as e:
                    print(e)
                    await client.edit_message_text(sender, edit_id, f'**ғᴀɪʟᴇᴅ ᴛᴏ sᴀᴠᴇ:** `{msg_link}`\n\n**ᴇʀʀᴏʀ**: {str(e)}')
                    try:
                        os.remove(file)
                    except Exception:
                        return
                    return
            try:
                os.remove(file)
                if os.path.isfile(file) == True:
                    os.remove(file)
            except Exception:
                pass
            await edit.delete()
        except (ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid):
            await client.edit_message_text(sender, edit_id, "**My Owner Account Don't Join Your Channel.\n\nSend /join then send your channel invite link then try again**")
            return
        except PeerIdInvalid:
            chat = msg_link.split("/")[-3]
            try:
                int(chat)
                new_link = f"t.me/c/{chat}/{msg_id}"
            except:
                new_link = f"t.me/b/{chat}/{msg_id}"
            return await get_msg(client, bot, sender, edit_id, msg_link, i)
        except Exception as e:
            print(e)
    else:
        edit = await client.edit_message_text(sender, edit_id, "**ᴄʟᴏɴɪɴɢ.**")
        chat =  msg_link.split("t.me")[1].split("/")[1]
        try:
            msg = await client.get_messages(chat, msg_id)
            if msg.empty:
                new_link = f't.me/b/{chat}/{int(msg_id)}'
                #recurrsion 
                return await get_msg(client, bot, sender, edit_id, new_link, i)
            await client.copy_message(sender, chat, msg_id)
        except Exception as e:
            print(e)
            return await client.edit_message_text(sender, edit_id, f'**ғᴀɪʟᴇᴅ ᴛᴏ sᴀᴠᴇ:** `{msg_link}`\n\n**ᴇʀʀᴏʀ**: {str(e)}')
        await edit.delete() 

async def progress_for_pyrogram(
    current,
    total,
    bot,
    ud_type,
    message,
    start
):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        status = DOWNLOAD_LOCATION + "/status.json"
        if os.path.exists(status):
            with open(status, 'r+') as f:
                statusMsg = json.load(f)
                if not statusMsg["running"]:
                    bot.stop_transmission()
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "**[{0}{1}]** `| {2}%`\n\n".format(
            ''.join([FINISHED_PROGRESS_STR for i in range(math.floor(percentage / 10))]),
            ''.join([UN_FINISHED_PROGRESS_STR for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2))

        tmp = progress + "⏳ **ɢʀᴏss:** **{0}** **ᴏғ** **{1}**\n\n🚀 **sᴘᴇᴇᴅ:** **{2}**/**s**\n\n🕛 **ᴇᴛᴀ:** **{3}**\n\n**Powered By : @VJ_Botz**".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            if not message.photo:
                await message.edit_text(
                    text="{}\n {}".format(
                        ud_type,
                        tmp
                    )
                )
            else:
                await message.edit_caption(
                    caption="{}\n {}".format(
                        ud_type,
                        tmp
                    )
                )
        except:
            pass


def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2]

def get_link(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)   
    try:
        link = [x[0] for x in url][0]
        if link:
            return link
        else:
            return False
    except Exception:
        return False
