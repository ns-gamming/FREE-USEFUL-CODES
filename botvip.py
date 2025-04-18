import telebot
import requests

# Thay token của bạn vào đây
BOT_TOKEN = "8011727027:AAG34c7MJo_6QTMb711tA2bM6Zv_ncAOHL4"
ALLOWED_GROUP_ID = [-1002627916538]  # Thay ID nhóm của bạn

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['videogai'])
def send_video(message):
    if message.chat.id not in ALLOWED_GROUP_ID:
        bot.reply_to(
            message,
            "Tham Gia Nhóm Của Chúng Tôi Để Bot Có Thể Trò Chuyện Với Bạn Dễ Dàng Hơn.\n"
            "Link Đây: [ https://t.me/checkinfo123 ]\n\n"
            "Lưu Ý, Bot Chỉ Hoạt Động Trong Những Nhóm Cụ Thể Thôi Nha!"
        )
        return
    
    wait_message = bot.reply_to(message, "Đang Tải Video, Vui Lòng Chờ...")

    api_url = "https://api.ffcommunity.site/randomvideo.php"

    try:
        response = requests.get(api_url)
        video_data = response.json()
        video_url = video_data.get("url")

        if video_url:
            bot.delete_message(message.chat.id, wait_message.message_id)
            bot.send_video(
                message.chat.id,
                video_url,
                caption="<b>Random Video By @cyberxthbot</b>",
                reply_to_message_id=message.message_id,
                parse_mode="HTML"
            )
        else:
            bot.reply_to(message, "Không tìm thấy video.")

    except Exception as e:
        bot.reply_to(message, f"Có lỗi xảy ra, thử lại sau!\nLỗi: {e}")

# Chạy bot
print("Bot is running...")
bot.polling(none_stop=True)