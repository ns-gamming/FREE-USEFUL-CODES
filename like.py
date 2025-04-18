import asyncio
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

API_ID = 28460459  # Replace with your API ID
API_HASH = "5e3e62436e4907ca16d5ae109d462c2f"
BOT_TOKEN = "7801023113:AAFP9aFRZXM1H7Qob9srOAS5uK4Lajbg-PM"

ALLOWED_GROUPS = [-1002318264973, -1002433803398, -1002238556459]  # Add your allowed group IDs here
vip_users = [7586579505, 7156455211, 6839288964]  # Add VIP user Telegram IDs here
user_data = {}

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

bot = Client("ff_like_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def group_only(func):
    async def wrapper(client, message):
        if message.chat.id in ALLOWED_GROUPS:
            await func(client, message)
        else:
            await message.reply("⛔ This bot works only in authorized groups. Contact admin to get access.")
    return wrapper

@bot.on_message(filters.command("start"))
async def start(_, m: Message):
    await m.reply(
        f"👋 Welcome {m.from_user.mention}!\n\n"
        "Use this command to get Free Fire likes:\n"
        "`/like ind UID`\n\n"
        "Example:\n"
        "`/like ind 8431487083`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Join Jexar Empire", url="https://t.me/+7aydoSgDfHc5MGFl")]
        ]),
        quote=True
    )

@bot.on_message(filters.command("check"))
@group_only
async def check_status(_, m: Message):
    user_id = m.from_user.id
    today = get_today()
    used = user_data.get(user_id, {}).get("date") == today
    is_vip = user_id in vip_users
    status = "UNLIMITED (VIP)" if is_vip else ("1/1 ✅ Used" if used else "0/1 ❌ Not Used")

    await m.reply(
        f"**DEAR {m.from_user.mention}, YOUR STATUS**\n\n"
        f"**FREE REQUEST:** {status}\n"
        f"**OWNER:** @GODJEXAR",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Join Jexar Empire", url="https://t.me/+7aydoSgDfHc5MGFl")]
        ]),
        quote=True
    )

@bot.on_message(filters.command("like"))
@group_only
async def like_handler(_, m: Message):
    args = m.text.split()
    user_id = m.from_user.id
    today = get_today()

    if len(args) != 3:
        return await m.reply(
            "⚠️ Invalid command format.\n\nUse like this:\n`/like ind 8431487083`",
            quote=True
        )

    server, uid = args[1].lower(), args[2]

    if server != "ind":
        return await m.reply("⚠️ This bot only supports **India server (ind)**.", quote=True)

    is_vip = user_id in vip_users

    if not is_vip:
        if user_id in user_data and user_data[user_id].get("date") == today:
            used_uid = user_data[user_id].get("uid")
            if used_uid == uid:
                return await m.reply(
                    f"⛔ {m.from_user.mention}, likes already sent to this ID today!\nTry again tomorrow.",
                    quote=True
                )
            else:
                return await m.reply(
                    f"⛔ {m.from_user.mention}, you've already used your **1 Free Like** today!\nUpgrade to VIP for unlimited likes.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("💎 Buy VIP", url="https://t.me/GODJEXAR")]
                    ]),
                    quote=True
                )

    processing = await m.reply("⏳ Sending likes, please wait...", quote=True)
    await asyncio.sleep(3)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://ff-max-like.vercel.app/like?server_name=ind&uid={uid}") as resp:
                if resp.status != 200:
                    raise Exception("API Error")
                data = await resp.json()
    except Exception:
        return await processing.edit(f"❌ Error while contacting API.\nPlease try again later.")

    if data.get("LikesGivenByAPI") == 0:
        return await processing.edit(
            f"⚠️ {m.from_user.mention}, this UID has reached max likes today!\nTry again tomorrow or use another UID."
        )

    if not is_vip:
        user_data[user_id] = {"date": today, "uid": uid}

    await processing.edit(
        f"✅ **Like Sent Successfully!**\n\n"
        f"👤 **Player Name:** {data['PlayerNickname']}\n"
        f"🆔 **UID:** `{data['UID']}`\n"
        f"❤️ **Before Likes:** {data['LikesbeforeCommand']}\n"
        f"💖 **After Likes:** {data['LikesafterCommand']}\n"
        f"📈 **Likes Sent:** {data['LikesGivenByAPI']}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Join Jexar Empire", url="https://t.me/+7aydoSgDfHc5MGFl")]
        ])
    )

print("Bot is running...")
bot.run()