# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os, string, logging, random, asyncio, time, datetime, re, sys, json, base64
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import *
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id, get_bad_files
from database.users_chats_db import db, delete_all_referal_users, get_referal_users_count, get_referal_all_users, referal_add_user
from database.join_reqs import JoinReqs
from info import *
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from utils import get_settings, pub_is_subscribed, get_size, is_subscribed, save_group_settings, temp, verify_user, check_token, check_verification, get_token, get_shortlink, get_tutorial, get_seconds
from database.connections_mdb import active_connection
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
logger = logging.getLogger(__name__)

BATCH_FILES = {}

@Client.on_message(filters.new_chat_members & filters.chat(AUTH_CHANNEL))
async def fsub_wto_try(client, message):
    if REQUEST_TO_JOIN_MODE == False:
        if TRY_AGAIN_BTN == True:
            return
        data = await db.get_msg_command(message.from_user.id)
        
        if data.split("-", 1)[0] == "VJ":
            user_id = int(data.split("-", 1)[1])
            vj = await referal_add_user(user_id, message.from_user.id)
            if vj and PREMIUM_AND_REFERAL_MODE == True:
                await client.send_message(message.from_user.id, f"<b>You have joined using the referral link of user with ID {user_id}\n\nSend /start again to use the bot</b>")
                num_referrals = await get_referal_users_count(user_id)
                await client.send_message(chat_id = user_id, text = "<b>{} start the bot with your referral link\n\nTotal Referals - {}</b>".format(message.from_user.mention, num_referrals))
                if num_referrals == REFERAL_COUNT:
                    time = REFERAL_PREMEIUM_TIME       
                    seconds = await get_seconds(time)
                    if seconds > 0:
                        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
                        user_data = {"id": user_id, "expiry_time": expiry_time} 
                        await db.update_user(user_data)  # Use the update_user method to update or insert user data
                        await delete_all_referal_users(user_id)
                        await client.send_message(chat_id = user_id, text = "<b>You Have Successfully Completed Total Referal.\n\nYou Added In Premium For {}</b>".format(REFERAL_PREMEIUM_TIME))
                        return 
            else:
                if PREMIUM_AND_REFERAL_MODE == True:
                    buttons = [[
                        InlineKeyboardButton('⤬ Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ⤬', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                    ],[
                        InlineKeyboardButton('Eᴀʀɴ Mᴏɴᴇʏ 💸', callback_data="shortlink_info"),
                        InlineKeyboardButton('⌬ Mᴏᴠɪᴇ Gʀᴏᴜᴘ', url=GRP_LNK)
                    ],[
                        InlineKeyboardButton('〄 Hᴇʟᴘ', callback_data='help'),
                        InlineKeyboardButton('⍟ Aʙᴏᴜᴛ', callback_data='about')
                    ],[
                        InlineKeyboardButton('🔻 ɢᴇᴛ ғʀᴇᴇ/ᴘᴀɪᴅ sᴜʙsᴄʀɪᴘᴛɪᴏɴ 🔻', callback_data='subscription')
                    ],[
                        InlineKeyboardButton('✇ Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ✇', url=CHNL_LNK)
                    ]]
                else:
                    buttons = [[
                        InlineKeyboardButton('⤬ Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ⤬', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                    ],[
                        InlineKeyboardButton('Eᴀʀɴ Mᴏɴᴇʏ 💸', callback_data="shortlink_info"),
                        InlineKeyboardButton('⌬ Mᴏᴠɪᴇ Gʀᴏᴜᴘ', url=GRP_LNK)
                    ],[
                        InlineKeyboardButton('〄 Hᴇʟᴘ', callback_data='help'),
                        InlineKeyboardButton('⍟ Aʙᴏᴜᴛ', callback_data='about')
                    ],[
                        InlineKeyboardButton('✇ Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ✇', url=CHNL_LNK)
                    ]]
                reply_markup = InlineKeyboardMarkup(buttons)
                m=await client.send_sticker(chat_id = message.from_user.id, sticker = "CAACAgUAAxkBAAEKVaxlCWGs1Ri6ti45xliLiUeweCnu4AACBAADwSQxMYnlHW4Ls8gQMAQ") 
                await asyncio.sleep(1)
                await m.delete()
                await client.send_photo(
                    chat_id=message.from_user.id,
                    photo=random.choice(PICS),
                    caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
                    reply_markup=reply_markup,
                    parse_mode=enums.ParseMode.HTML
                )
                return 
        try:
            pre, file_id = data.split('_', 1)
        except:
            file_id = data
            pre = ""
        if data.split("-", 1)[0] == "verify":
            userid = data.split("-", 2)[1]
            token = data.split("-", 3)[2]
            if str(message.from_user.id) != str(userid):
                return await client.send_message(
                    chat_id=message.from_user.id,
                    text="<b>Invalid link or Expired link !</b>",
                    protect_content=True
                )
            is_valid = await check_token(client, userid, token)
            if is_valid == True:
                await client.send_message(
                    chat_id=message.from_user.id,
                    text=f"<b>Hey {message.from_user.mention}, You are successfully verified !\nNow you have unlimited access for all movies till today midnight.</b>",
                    protect_content=True
                )
                await verify_user(client, userid, token)
            else:
                return await client.send_message(
                    chat_id=message.from_user.id,
                    text="<b>Invalid link or Expired link !</b>",
                    protect_content=True
                )
        if data.startswith("sendfiles"):
            chat_id = int("-" + file_id.split("-")[1])
            userid = message.from_user.id if message.from_user else None
            settings = await get_settings(chat_id)
            g = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start=allfiles_{file_id}")
            button = [[
                InlineKeyboardButton('📂 Dᴏᴡɴʟᴏᴀᴅ Nᴏᴡ 📂', url=g)
            ],[
                InlineKeyboardButton('⁉️ Hᴏᴡ Tᴏ Dᴏᴡɴʟᴏᴀᴅ ⁉️', url=await get_tutorial(chat_id))
            ]]
            k = await client.send_message(chat_id=message.from_user.id,text=f"<b>Get All Files in a Single Click!!!\n\n📂 ʟɪɴᴋ ➠ : {g}\n\n<i>Note: This message is deleted in 5 mins to avoid copyrights. Save the link to Somewhere else</i></b>", reply_markup=InlineKeyboardMarkup(button))
            await asyncio.sleep(300)
            await k.edit("<b>Your message is successfully deleted!!!</b>")
            return   
    
        elif data.startswith("short"):
            user = message.from_user.id
            chat_id = temp.SHORT.get(user)
            settings = await get_settings(chat_id)
            files_ = await get_file_details(file_id)
            files = files_[0]
            g = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start=file_{file_id}")
            button = [[
                InlineKeyboardButton('📂 Dᴏᴡɴʟᴏᴀᴅ Nᴏᴡ 📂', url=g)
            ],[
                InlineKeyboardButton('⁉️ Hᴏᴡ Tᴏ Dᴏᴡɴʟᴏᴀᴅ ⁉️', url=await get_tutorial(chat_id))
            ]]
            k = await client.send_message(chat_id=user,text=f"<b>📕Nᴀᴍᴇ ➠ : <code>{files.file_name}</code> \n\n🔗Sɪᴢᴇ ➠ : {get_size(files.file_size)}\n\n📂Fɪʟᴇ ʟɪɴᴋ ➠ : {g}\n\n<i>Note: This message is deleted in 20 mins to avoid copyrights. Save the link to Somewhere else</i></b>", reply_markup=InlineKeyboardMarkup(button))
            await asyncio.sleep(1200)
            await k.edit("<b>Your message is successfully deleted!!!</b>")
            return
        
        elif data.startswith("all"):
            files = temp.GETALL.get(file_id)
            if not files:
                return await client.send_message(chat_id=message.from_user.id, text='<b><i>No such file exist.</b></i>')
            filesarr = []
            for file in files:
                file_id = file.file_id
                files_ = await get_file_details(file_id)
                files1 = files_[0]
                title = ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files1.file_name.split()))
                size=get_size(files1.file_size)
                f_caption=files1.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                    except Exception as e:
                        logger.exception(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files1.file_name.split()))}"
                if not await db.has_premium_access(message.from_user.id):
                    if not await check_verification(client, message.from_user.id) and VERIFY == True:
                        btn = [[
                            InlineKeyboardButton("Verify", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start="))
                        ],[
                            InlineKeyboardButton("How To Open Link & Verify", url=VERIFY_TUTORIAL)
                        ]]
                        await client.send_message(
                            chat_id=message.from_user.id,
                            text="<b>You are not verified !\nKindly verify to continue !</b>",
                            protect_content=True,
                            reply_markup=InlineKeyboardMarkup(btn)
                        )
                        return
                if STREAM_MODE == True:
                    button = [[
                        InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=f'https://t.me/{SUPPORT_CHAT}'),
                        InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=CHNL_LNK)
                    ],[
                        InlineKeyboardButton("𝗕𝗢𝗧 𝗢𝗪𝗡𝗘𝗥", url="t.me/KingVJ01")
                    ],[
                        InlineKeyboardButton('🚀 Fast Download / Watch Online🖥️', callback_data=f'generate_stream_link:{file_id}') #Don't change anything without contacting me @KingVJ01
                    ]]
                else:
                    button = [[
                        InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=f'https://t.me/{SUPPORT_CHAT}'),
                        InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=CHNL_LNK)
                    ],[
                        InlineKeyboardButton("𝗕𝗢𝗧 𝗢𝗪𝗡𝗘𝗥", url="t.me/KingVJ01")
                    ]]
                msg = await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    protect_content=True if pre == 'filep' else False,
                    reply_markup=InlineKeyboardMarkup(button)
                )
                filesarr.append(msg)
            k = await client.send_message(chat_id = message.from_user.id, text=f"<b><u>❗️❗️❗️IMPORTANT❗️️❗️❗️</u></b>\n\nThis Movie Files/Videos will be deleted in <b><u>10 mins</u> 🫥 <i></b>(Due to Copyright Issues)</i>.\n\n<b><i>Please forward this ALL Files/Videos to your Saved Messages and Start Download there</i></b>")
            await asyncio.sleep(600)
            for x in filesarr:
                await x.delete()
            await k.edit_text("<b>Your All Files/Videos is successfully deleted!!!</b>")
            return
        elif data.startswith("files"):
            user = message.from_user.id
            if temp.SHORT.get(user)==None:
                await client.send_message(chat_id=message.from_user.id, text="<b>Please Search Again in Group</b>")
            else:
                chat_id = temp.SHORT.get(user)
            settings = await get_settings(chat_id)
            if settings['is_shortlink'] and not await db.has_premium_access(user):
                files_ = await get_file_details(file_id)
                files = files_[0]
                g = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start=file_{file_id}")
                button = [[
                    InlineKeyboardButton('📂 Dᴏᴡɴʟᴏᴀᴅ Nᴏᴡ 📂', url=g)
                ],[
                    InlineKeyboardButton('⁉️ Hᴏᴡ Tᴏ Dᴏᴡɴʟᴏᴀᴅ ⁉️', url=await get_tutorial(chat_id))
                ]]
                k = await client.send_message(chat_id=message.from_user.id,text=f"<b>📕Nᴀᴍᴇ ➠ : <code>{files.file_name}</code> \n\n🔗Sɪᴢᴇ ➠ : {get_size(files.file_size)}\n\n📂Fɪʟᴇ ʟɪɴᴋ ➠ : {g}\n\n<i>Note: This message is deleted in 20 mins to avoid copyrights. Save the link to Somewhere else</i></b>", reply_markup=InlineKeyboardMarkup(button))
                await asyncio.sleep(1200)
                await k.edit("<b>Your message is successfully deleted!!!</b>")
                return
        user = message.from_user.id
        files_ = await get_file_details(file_id)           
        if not files_:
            pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
            try:
                if not await db.has_premium_access(message.from_user.id):
                    if not await check_verification(client, message.from_user.id) and VERIFY == True:
                        btn = [[
                            InlineKeyboardButton("Verify", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start="))
                        ],[
                            InlineKeyboardButton("How To Open Link & Verify", url=VERIFY_TUTORIAL)
                        ]]
                        await client.send_message(
                            chat_id=message.from_user.id,
                            text="<b>You are not verified !\nKindly verify to continue !</b>",
                            protect_content=True,
                            reply_markup=InlineKeyboardMarkup(btn)
                        )
                        return
                if STREAM_MODE == True:
                    button = [[
                        InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=f'https://t.me/{SUPPORT_CHAT}'),
                        InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=CHNL_LNK)
                    ],[
                        InlineKeyboardButton("𝗕𝗢𝗧 𝗢𝗪𝗡𝗘𝗥", url="t.me/KingVJ01")
                    ],[
                        InlineKeyboardButton('🚀 Fast Download / Watch Online🖥️', callback_data=f'generate_stream_link:{file_id}') #Don't change anything without contacting me @KingVJ01
                    ]]
                else:
                    button = [[
                        InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=f'https://t.me/{SUPPORT_CHAT}'),
                        InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=CHNL_LNK)
                    ],[
                        InlineKeyboardButton("𝗕𝗢𝗧 𝗢𝗪𝗡𝗘𝗥", url="t.me/KingVJ01")
                    ]]
                msg = await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=file_id,
                    protect_content=True if pre == 'filep' else False,
                    reply_markup=InlineKeyboardMarkup(button)
                )
                filetype = msg.media
                file = getattr(msg, filetype.value)
                title = '@VJ_Bots  ' + ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), file.file_name.split()))
                size=get_size(file.file_size)
                f_caption = f"<code>{title}</code>"
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='')
                    except:
                        return
                await msg.edit_caption(
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(button)
                )
                btn = [[
                    InlineKeyboardButton("Get File Again", callback_data=f'delfile#{file_id}')
                ]]
                k = await client.send_message(message.from_user.id,"<b><u>❗️❗️❗️IMPORTANT❗️️❗️❗️</u></b>\n\nThis Movie File/Video will be deleted in <b><u>10 mins</u> 🫥 <i></b>(Due to Copyright Issues)</i>.\n\n<b><i>Please forward this File/Video to your Saved Messages and Start Download there</i></b>",quote=True)
                await asyncio.sleep(600)
                await msg.delete()
                await k.edit_text("<b>Your File/Video is successfully deleted!!!\n\nClick below button to get your deleted file 👇</b>",reply_markup=InlineKeyboardMarkup(btn))
                return
            except:
                pass
            return await message.reply('No such file exist.')
        files = files_[0]
        title = '@VJ_Bots  ' + ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files.file_name.split()))
        size=get_size(files.file_size)
        f_caption=files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption=f_caption
        if f_caption is None:
            f_caption = f"@VJ_Bots  {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files.file_name.split()))}"
        if not await db.has_premium_access(message.from_user.id):
            if not await check_verification(client, message.from_user.id) and VERIFY == True:
                btn = [[
                    InlineKeyboardButton("Verify", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start="))
                ],[
                    InlineKeyboardButton("How To Open Link & Verify", url=VERIFY_TUTORIAL)
                ]]
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="<b>You are not verified !\nKindly verify to continue !</b>",
                    protect_content=True,
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                return
        if STREAM_MODE == True:
            button = [[
                InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=f'https://t.me/{SUPPORT_CHAT}'),
                InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=CHNL_LNK)
            ],[
                InlineKeyboardButton("𝗕𝗢𝗧 𝗢𝗪𝗡𝗘𝗥", url="t.me/KingVJ01")
            ],[
                InlineKeyboardButton('🚀 Fast Download / Watch Online🖥️', callback_data=f'generate_stream_link:{file_id}') #Don't change anything without contacting me @KingVJ01
            ]]
        else:
            button = [[
                InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=f'https://t.me/{SUPPORT_CHAT}'),
                InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=CHNL_LNK)
            ],[
                InlineKeyboardButton("𝗕𝗢𝗧 𝗢𝗪𝗡𝗘𝗥", url="t.me/KingVJ01")
            ]]
        msg = await client.send_cached_media(
            chat_id=message.from_user.id,
            file_id=file_id,
            caption=f_caption,
            protect_content=True if pre == 'filep' else False,
            reply_markup=InlineKeyboardMarkup(button)
        )
        btn = [[
            InlineKeyboardButton("Get File Again", callback_data=f'delfile#{file_id}')
        ]]
        k = await client.send_message(message.from_user.id, "<b><u>❗️❗️❗️IMPORTANT❗️️❗️❗️</u></b>\n\nThis Movie File/Video will be deleted in <b><u>10 mins</u> 🫥 <i></b>(Due to Copyright Issues)</i>.\n\n<b><i>Please forward this File/Video to your Saved Messages and Start Download there</i></b>",quote=True)
        await asyncio.sleep(600)
        await msg.delete()
        await k.edit_text("<b>Your File/Video is successfully deleted!!!\n\nClick below button to get your deleted file 👇</b>",reply_markup=InlineKeyboardMarkup(btn))
        return

@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    r_j_check = [u.id for u in message.new_chat_members]
    if temp.ME in r_j_check:
        if not await db.get_chat(message.chat.id):
            total=await bot.get_chat_members_count(message.chat.id)
            r_j = message.from_user.mention if message.from_user else "Anonymous" 
            await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, r_j))       
            await db.add_chat(message.chat.id, message.chat.title)
        if message.chat.id in temp.BANNED_CHATS:
            # Inspired from a boat of a banana tree
            buttons = [[
                InlineKeyboardButton('Support', url=f'https://t.me/{SUPPORT_CHAT}')
            ]]
            reply_markup=InlineKeyboardMarkup(buttons)
            k = await message.reply(
                text='<b>CHAT NOT ALLOWED 🐞\n\nMy admins has restricted me from working here ! If you want to know more about it contact support..</b>',
                reply_markup=reply_markup,
            )

            try:
                await k.pin()
            except:
                pass
            await bot.leave_chat(message.chat.id)
            return
        buttons = [[
                    InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=GRP_LNK),
                    InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=CHNL_LNK)
                 ],[
                    InlineKeyboardButton("Bᴏᴛ Oᴡɴᴇʀ", url="t.me/KingVJ01")
                  ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=f"<b>Thankyou For Adding Me In {message.chat.title} ❣️\n\nIf you have any questions & doubts about using me contact support.</b>",
            reply_markup=reply_markup)
    else:
        settings = await get_settings(message.chat.id)
        if settings["welcome"]:
            for u in message.new_chat_members:
                if (temp.MELCOW).get('welcome') is not None:
                    try:
                        await (temp.MELCOW['welcome']).delete()
                    except:
                        pass
                temp.MELCOW['welcome'] = await message.reply_video(
                                                 video=(MELCOW_VID),
                                                 caption=(script.MELCOW_ENG.format(u.mention, message.chat.title)),
                                                 reply_markup=InlineKeyboardMarkup(
                                                                         [[
                                                                           InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=GRP_LNK),
                                                                           InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=CHNL_LNK)
                                                                        ],[
                                                                           InlineKeyboardButton("Bᴏᴛ Oᴡɴᴇʀ", url="t.me/KingVJ01")
                                                                         ]]
                                                 ),
                                                 parse_mode=enums.ParseMode.HTML
                )
                
        if settings["auto_delete"]:
            await asyncio.sleep(600)
            await (temp.MELCOW['welcome']).delete()

@Client.on_message(filters.command('leave') & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        chat = chat
    try:
        buttons = [[
            InlineKeyboardButton('Support Group',url="https://t.me/vj_bots"),
            InlineKeyboardButton("Bᴏᴛ Oᴡɴᴇʀ", url="t.me/KingVJ01")
        ],[
            InlineKeyboardButton('Use Me Here', url=f'https://t.me/{SUPPORT_CHAT}')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat,
            text='<b>Hello Friends, \nMy admin has told me to leave from group, so i go! If you wanna add me again contact my Support Group or My Owner</b>',
            reply_markup=reply_markup,
        )

        await bot.leave_chat(chat)
        await message.reply(f"left the chat `{chat}`")
    except Exception as e:
        await message.reply(f'Error - {e}')

@Client.on_message(filters.command('disable') & filters.user(ADMINS))
async def disable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat_ = int(chat)
    except:
        return await message.reply('Give Me A Valid Chat ID')
    cha_t = await db.get_chat(int(chat_))
    if not cha_t:
        return await message.reply("Chat Not Found In DB")
    if cha_t['is_disabled']:
        return await message.reply(f"This chat is already disabled:\nReason-<code> {cha_t['reason']} </code>")
    await db.disable_chat(int(chat_), reason)
    temp.BANNED_CHATS.append(int(chat_))
    await message.reply('Chat Successfully Disabled')
    try:
        buttons = [[
            InlineKeyboardButton('Support', url=f'https://t.me/{SUPPORT_CHAT}')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat_, 
            text=f'<b>Hello Friends, \nMy admin has told me to leave from group so i go! If you wanna add me again contact my support group.</b> \nReason : <code>{reason}</code>',
            reply_markup=reply_markup)
        await bot.leave_chat(chat_)
    except Exception as e:
        await message.reply(f"Error - {e}")

@Client.on_message(filters.command('enable') & filters.user(ADMINS))
async def re_enable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat_ = int(chat)
    except:
        return await message.reply('Give Me A Valid Chat ID')
    sts = await db.get_chat(int(chat))
    if not sts:
        return await message.reply("Chat Not Found In DB !")
    if not sts.get('is_disabled'):
        return await message.reply('This chat is not yet disabled.')
    await db.re_enable_chat(int(chat_))
    temp.BANNED_CHATS.remove(int(chat_))
    await message.reply("Chat Successfully re-enabled")

@Client.on_message(filters.command('stats') & filters.incoming)
async def get_ststs(bot, message):
    rju = await message.reply('Fetching stats..')
    total_users = await db.total_users_count()
    totl_chats = await db.total_chat_count()
    files = await Media.count_documents()
    size = await db.get_db_size()
    free = 536870912 - size
    size = get_size(size)
    free = get_size(free)
    await rju.edit(script.STATUS_TXT.format(files, total_users, totl_chats, size, free))

@Client.on_message(filters.command('invite') & filters.user(ADMINS))
async def gen_invite(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        return await message.reply('Give Me A Valid Chat ID')
    try:
        link = await bot.create_chat_invite_link(chat)
    except ChatAdminRequired:
        return await message.reply("Invite Link Generation Failed, Iam Not Having Sufficient Rights")
    except Exception as e:
        return await message.reply(f'Error {e}')
    await message.reply(f'Here is your Invite Link {link.invite_link}')

@Client.on_message(filters.command('ban') & filters.user(ADMINS))
async def ban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a user id / username')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("This is an invalid user, make sure ia have met him before.")
    except IndexError:
        return await message.reply("This might be a channel, make sure its a user.")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if jar['is_banned']:
            return await message.reply(f"{k.mention} is already banned\nReason: {jar['ban_reason']}")
        await db.ban_user(k.id, reason)
        temp.BANNED_USERS.append(k.id)
        await message.reply(f"Successfully banned {k.mention}")
    
@Client.on_message(filters.command('unban') & filters.user(ADMINS))
async def unban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a user id / username')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("This is an invalid user, make sure ia have met him before.")
    except IndexError:
        return await message.reply("Thismight be a channel, make sure its a user.")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if not jar['is_banned']:
            return await message.reply(f"{k.mention} is not yet banned.")
        await db.remove_ban(k.id)
        temp.BANNED_USERS.remove(k.id)
        await message.reply(f"Successfully unbanned {k.mention}")
    
@Client.on_message(filters.command('users') & filters.user(ADMINS))
async def list_users(bot, message):
    # https://t.me/GetTGLink/4184
    raju = await message.reply('Getting List Of Users')
    users = await db.get_all_users()
    out = "Users Saved In DB Are:\n\n"
    async for user in users:
        out += f"<a href=tg://user?id={user['id']}>{user['name']}</a>"
        if user['ban_status']['is_banned']:
            out += '( Banned User )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('users.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('users.txt', caption="List Of Users")

@Client.on_message(filters.command('chats') & filters.user(ADMINS))
async def list_chats(bot, message):
    raju = await message.reply('Getting List Of chats')
    chats = await db.get_all_chats()
    out = "Chats Saved In DB Are:\n\n"
    async for chat in chats:
        out += f"**Title:** `{chat['title']}`\n**- ID:** `{chat['id']}`"
        if chat['chat_status']['is_disabled']:
            out += '( Disabled Chat )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('chats.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('chats.txt', caption="List Of Chats")
