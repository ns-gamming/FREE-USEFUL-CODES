import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, CallbackContext, filters

TOKEN = ""  # Your bot token
ADMIN_ID = 00000000000  # Your ID
ADMIN_NAME = ""  # Your name
ADMIN_USERNAME = ""  # Your username

# Initialize the bot
application = ApplicationBuilder().token(TOKEN).build()

# Create necessary directories
if not os.path.exists("data"):
    os.makedirs("data")

# Load JSON data
def load_json(filename):
    if os.path.exists(filename):
        with open(filename) as f:
            return json.load(f)
    return {}

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

zyzo = load_json("data/zyzo.json")
meca = load_json("data/members.json")

# Default values if not present
zyzo.setdefault("bot", "❎")
zyzo.setdefault("d7", "❎")
zyzo.setdefault("d6", "❎")
zyzo.setdefault("start", f"مرحبا بك في بوت التواصل الخاص ب {ADMIN_NAME}\nقم بارسال رسالتك وسوف يتم الرد عليك\nWelcome to your communication bot by {ADMIN_NAME}\nSend your message and you will be answered")

# Create empty lists if not present
meca.setdefault("members", [])
meca.setdefault("group", [])
zyzo.setdefault("ban", [])
zyzo.setdefault("admin", [])

# Start command
async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    from_id = update.message.from_user.id

    if from_id == ADMIN_ID:
        keyboard = [
            [InlineKeyboardButton("ايقاف / تشغيل " + zyzo.get("bot", "❎"), callback_data="bot3"),
             InlineKeyboardButton("التوجية " + zyzo.get("d7", "❎"), callback_data="d7")],
            [InlineKeyboardButton("الاشعارات " + zyzo.get("d6", "❎"), callback_data="d6")],
            [InlineKeyboardButton("رساله الترحيب (start)", callback_data="4")],
            [InlineKeyboardButton("قسم النسخة", callback_data="Open"),
             InlineKeyboardButton("نقل الملكية", callback_data="AddAdmin")],
            [InlineKeyboardButton("قسم الاذاعة", callback_data="10"),
             InlineKeyboardButton("قسم الاحصائيات", callback_data="1")],
            [InlineKeyboardButton("قسم الاشتراك الاجباري", callback_data="All Ch")],
            [InlineKeyboardButton("قسم المحظورين", callback_data="lastban"),
             InlineKeyboardButton("قسم الادمنية", callback_data="5")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("• اهلا بك في لوحه الأدمن الخاصه بالبوت\n- يمكنك التحكم في البوت الخاص بك من هنا\n⎯ ⎯ ⎯ ⎯", reply_markup=reply_markup)
    else:
        welcome_message = zyzo.get("start")
        keyboard = [[InlineKeyboardButton(ADMIN_NAME, url=f"https://t.me/{ADMIN_USERNAME}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

# Button callback
async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "bot3":
        zyzo["bot"] = "✅" if zyzo.get("bot") == "❎" else "❎"
        save_json(zyzo, "data/zyzo.json")
    elif data == "d7":
        zyzo["d7"] = "✅" if zyzo.get("d7") == "❎" else "❎"
        save_json(zyzo, "data/zyzo.json")
    elif data == "d6":
        zyzo["d6"] = "✅" if zyzo.get("d6") == "❎" else "❎"
        save_json(zyzo, "data/zyzo.json")
    elif data == "4":
        keyboard = [
            [InlineKeyboardButton("عرض رساله (start)", callback_data="startsho"),
             InlineKeyboardButton("مسح رساله (start)", callback_data="unset start")],
            [InlineKeyboardButton("تغير رساله (start)", callback_data="setstart")],
            [InlineKeyboardButton("رجوع", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("اهلا بك في قسم رساله(start)", reply_markup=reply_markup)
    elif data == "startsho":
        start_message = zyzo.get("start", "لا توجد رسالة ترحيب محددة.")
        await query.edit_message_text(f"⬇️رسالة الستارت هيه\n---------------\n {start_message}", parse_mode=ParseMode.MARKDOWN)
    elif data == "unset start":
        zyzo["start"] = None
        save_json(zyzo, "data/zyzo.json")
        await query.edit_message_text("تم حذف الاستارت", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
    elif data == "setstart":
        await query.edit_message_text("يمكنك الان ارسال رسالة الـstart ⏳\nلعرض الاسم : #name\nلعرض الايدي : #id\nلعرض المعرف : #user", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
        context.user_data["set_start"] = True
    elif data == "lastban":
        keyboard = [
            [InlineKeyboardButton(f"المحظورين ( {len(zyzo.get('ban', []))} )", callback_data="##")],
            [InlineKeyboardButton("حظر", callback_data="bannambar"), InlineKeyboardButton("الغاء حظر", callback_data="unbannambar")],
            [InlineKeyboardButton("عرض المحظورين", callback_data="lstesban")],
            [InlineKeyboardButton("مسح المحظورين", callback_data="dellastban")],
            [InlineKeyboardButton("رجوع", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("اليك قسم المحظورين.\n⎯ ⎯ ⎯ ⎯", reply_markup=reply_markup)
    elif data == "bannambar":
        await query.edit_message_text("حسنأ عزيزي ارسل ايدي العضو", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="lastban")]]))
        context.user_data["ban"] = True
    elif data == "unbannambar":
        await query.edit_message_text("حسنأ عزيزي ارسل ايدي العضو", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="lastban")]]))
        context.user_data["unban"] = True
    elif data == "lstesban":
        ban_list = zyzo.get("ban", [])
        if not ban_list:
            await query.edit_message_text("لايوجد محظور حاليأ", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="lastban")]]))
        else:
            ban_text = "\n".join([f"- [{user}](tg://user?id={id})" for user, id in ban_list])
            await query.edit_message_text(f"اليك قائمة المحظورين:\n{ban_text}", parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="lastban")]]))
    elif data == "dellastban":
        zyzo["ban"] = []
        save_json(zyzo, "data/zyzo.json")
        await query.edit_message_text("تم مسح قائمة المحظورين", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="lastban")]]))
    elif data == "Open":
        keyboard = [
            [InlineKeyboardButton("نسخة الاعضاء ➡️", callback_data="CopyMembers"),
             InlineKeyboardButton("جلب نسخة ✳", callback_data="OpenCopy")],
            [InlineKeyboardButton("نسخة الاعدادات ➡️", callback_data="CopySettings"),
             InlineKeyboardButton("جلب نسخة ✳", callback_data="Openstengs")],
            [InlineKeyboardButton("رفع نسخة 📤", callback_data="addfiles")],
            [InlineKeyboardButton("رجوع", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("اليك قسم النسخة للبوت 🗂\n⎯ ⎯ ⎯ ⎯", reply_markup=reply_markup)
    elif data == "OpenCopy":
        await application.bot.send_document(chat_id=ADMIN_ID, document=open("data/members.json", "rb"), caption="اليك النسخة الحتياطية للعضاء 🗂\nعدد الاعضاء ( {} )\n⎯ ⎯ ⎯ ⎯".format(len(meca["members"])))
    elif data == "Openstengs":
        await application.bot.send_document(chat_id=ADMIN_ID, document=open("data/zyzo.json", "rb"), caption="اليك النسخة الحتياطية الاعدادات 🗂\n⎯ ⎯ ⎯ ⎯")
    elif data == "addfiles":
        await query.edit_message_text("حسنأ عزيزي ارسل لي الملف المطلوب 📤\n⎯ ⎯ ⎯ ⎯", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
        context.user_data["addfiles"] = True
    elif data == "CopyMembers":
        await application.bot.send_document(chat_id=ADMIN_ID, document=open("data/members.json", "rb"), caption="اليك النسخة الحتياطية للعضاء 🗂\n⎯ ⎯ ⎯ ⎯")
    elif data == "CopySettings":
        await application.bot.send_document(chat_id=ADMIN_ID, document=open("data/zyzo.json", "rb"), caption="اليك النسخة الحتياطية الاعدادات 🗂\n⎯ ⎯ ⎯ ⎯")
    elif data == "back":
        await start(update, context)
    elif data == "AddAdmin":
        await query.edit_message_text("‼ ارسل الان ايدي المطور الجديد ✅", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data="back")]]))
        context.user_data["AddAdmin"] = True
    elif data == "1":
        total_members = len(meca["members"])
        total_groups = len(meca["group"])
        daily_interactions = sum(len(zyzo.get(day, [])) for day in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
        total_bans = len(zyzo["ban"])
        message = f"عدد المستخدمين الكلي: {total_members + total_groups}\nعدد الخاص: {total_members}\nعدد القنوات و الكروبات: {total_groups}\nعدد التفاعل اليومي: {daily_interactions}\nعدد المحظورين: {total_bans}"
        await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("تصفير الاحصائيات 🗑", callback_data="reset_stats")], [InlineKeyboardButton("الغاء ↪️", callback_data="back")]]))
    elif data == "reset_stats":
        await query.edit_message_text("هل أنت متأكد من أنك تريد تصفير الاحصائيات؟", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("نعم", callback_data="confirm_reset_stats")], [InlineKeyboardButton("لا", callback_data="back")]]))
    elif data == "confirm_reset_stats":
        meca["members"] = []
        meca["group"] = []
        save_json(meca, "data/members.json")
        await query.edit_message_text("تم تصفير الاحصائيات بنجاح", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
    elif data == "10":
        keyboard = [
            [InlineKeyboardButton("اذاعة للكل", callback_data="broadcast_all"),
             InlineKeyboardButton("اذاعة توجيه للكل", callback_data="forward_all")],
            [InlineKeyboardButton("اذاعة للخاص", callback_data="broadcast_private"),
             InlineKeyboardButton("اذاعة توجيه للخاص", callback_data="forward_private")],
            [InlineKeyboardButton("اذاعة كروبات", callback_data="broadcast_groups"),
             InlineKeyboardButton("اذاعة توجيه كروبات", callback_data="forward_groups")],
            [InlineKeyboardButton("رجوع", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("اختر نوع الإذاعة", reply_markup=reply_markup)
    elif data == "broadcast_all":
        await query.edit_message_text("أرسل الرسالة التي تريد إذاعتها للكل", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
        context.user_data["broadcast"] = "all"
    elif data == "forward_all":
        await query.edit_message_text("أرسل الرسالة التي تريد توجيهها للكل", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
        context.user_data["forward"] = "all"
    elif data == "broadcast_private":
        await query.edit_message_text("أرسل الرسالة التي تريد إذاعتها للخاص", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
        context.user_data["broadcast"] = "private"
    elif data == "forward_private":
        await query.edit_message_text("أرسل الرسالة التي تريد توجيهها للخاص", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
        context.user_data["forward"] = "private"
    elif data == "broadcast_groups":
        await query.edit_message_text("أرسل الرسالة التي تريد إذاعتها للكروبات", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
        context.user_data["broadcast"] = "groups"
    elif data == "forward_groups":
        await query.edit_message_text("أرسل الرسالة التي تريد توجيهها للكروبات", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
        context.user_data["forward"] = "groups"


# Handle messages
async def handle_message(update: Update, context: CallbackContext):
    message = update.message
    from_id = message.from_user.id

    if context.user_data.get("set_start"):
        zyzo["start"] = message.text
        save_json(zyzo, "data/zyzo.json")
        await message.reply_text("تم تغير رسالة الـstart", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
        context.user_data["set_start"] = False
        return

    if context.user_data.get("ban"):
        zyzo.setdefault("ban", []).append((message.from_user.username, from_id))
        save_json(zyzo, "data/zyzo.json")
        await message.reply_text(f"العضو - [{message.from_user.username}](tg://user?id={from_id})\nتم حـظـرهه بـنـجاح", parse_mode=ParseMode.MARKDOWN)
        context.user_data["ban"] = False
        return

    if context.user_data.get("unban"):
        zyzo["ban"] = [(user, uid) for user, uid in zyzo.get("ban", []) if uid != from_id]
        save_json(zyzo, "data/zyzo.json")
        await message.reply_text(f"العضو - [{message.from_user.username}](tg://user?id={from_id})\nتم الـغـاء حـظـرهه بـنـجاح", parse_mode=ParseMode.MARKDOWN)
        context.user_data["unban"] = False
        return

    if context.user_data.get("AddAdmin"):
        zyzo["admin"].append(message.text)
        save_json(zyzo, "data/zyzo.json")
        await message.reply_text("تمت إضافة الأدمن بنجاح", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
        context.user_data["AddAdmin"] = False
        return

    if context.user_data.get("broadcast"):
        if context.user_data["broadcast"] == "all":
            for member in meca["members"]:
                try:
                    await application.bot.send_message(chat_id=member, text=message.text)
                except Exception as e:
                    print(f"Error sending message to {member}: {e}")
            for group in meca["group"]:
                try:
                    await application.bot.send_message(chat_id=group, text=message.text)
                except Exception as e:
                    print(f"Error sending message to group {group}: {e}")
            await message.reply_text("تم إرسال الرسالة للجميع", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
        elif context.user_data["broadcast"] == "private":
            for member in meca["members"]:
                try:
                    await application.bot.send_message(chat_id=member, text=message.text)
                except Exception as e:
                    print(f"Error sending message to {member}: {e}")
            await message.reply_text("تم إرسال الرسالة لجميع الأعضاء", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
        elif context.user_data["broadcast"] == "groups":
            for group in meca["group"]:
                try:
                    await application.bot.send_message(chat_id=group, text=message.text)
                except Exception as e:
                    print(f"Error sending message to group {group}: {e}")
            await message.reply_text("تم إرسال الرسالة لجميع الكروبات", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
        context.user_data["broadcast"] = False
        return

    if context.user_data.get("forward"):
        if context.user_data["forward"] == "all":
            for member in meca["members"]:
                try:
                    await application.bot.forward_message(chat_id=member, from_chat_id=from_id, message_id=message.message_id)
                except Exception as e:
                    print(f"Error forwarding message to {member}: {e}")
            for group in meca["group"]:
                try:
                    await application.bot.forward_message(chat_id=group, from_chat_id=from_id, message_id=message.message_id)
                except Exception as e:
                    print(f"Error forwarding message to group {group}: {e}")
            await message.reply_text("تم توجيه الرسالة للجميع", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
        elif context.user_data["forward"] == "private":
            for member in meca["members"]:
                try:
                    await application.bot.forward_message(chat_id=member, from_chat_id=from_id, message_id=message.message_id)
                except Exception as e:
                    print(f"Error forwarding message to {member}: {e}")
            await message.reply_text("تم توجيه الرسالة لجميع الأعضاء", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
        elif context.user_data["forward"] == "groups":
            for group in meca["group"]:
                try:
                    await application.bot.forward_message(chat_id=group, from_chat_id=from_id, message_id=message.message_id)
                except Exception as e:
                    print(f"Error forwarding message to group {group}: {e}")
            await message.reply_text("تم توجيه الرسالة لجميع الكروبات", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
        context.user_data["forward"] = False
        return

    if from_id != ADMIN_ID:
        await application.bot.send_message(chat_id=ADMIN_ID, text=f"رسالة من {message.from_user.username}:\n{message.text}")
        await message.reply_text("تم ارسال رسالتك بنجاح ✅.\nYour message was sent successfully ✅", parse_mode=ParseMode.MARKDOWN)

async def handle_document(update: Update, context: CallbackContext):
    message = update.message
    if context.user_data.get("addfiles"):
        file = await context.bot.get_file(message.document.file_id)
        await file.download_to_drive(f"data/{message.document.file_name}")
        await message.reply_text(f"تم رفع الملف {message.document.file_name} بنجاح", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]]))
        context.user_data["addfiles"] = False

async def main():
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())