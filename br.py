from telegram import Update, ChatMemberUpdated
from telegram.ext import Application, CommandHandler, ContextTypes, filters
import requests
from datetime import datetime, timedelta, time

# Your bot token
BOT_TOKEN = '7600224257:AAEgDh-D7vLNfUhAq2sCYcCBEGvwbNopCxU'

# Admin IDs who are allowed to use admin commands
ADMIN_IDS = [7318766583, 6330136564]

# Default values for user requests
user_data = {}
# Biến toàn cục để lưu thông tin promotion theo nhóm
group_promotions = {}
# Biến lưu thông tin số lượt/ngày và thời hạn sử dụng bot của các nhóm
allowed_groups_info = {}

# List of groups allowed to use the bot
allowed_groups = set([-1002285703339])  # Automatically allow this group

# Function to reset daily requests for all users
def reset_daily_requests():
    now = datetime.now()
    for user_id, data in user_data.items():
        if not data['vip']:
            data['daily_requests'] = 1
        elif data['expiry_date'] < now:
            data['vip'] = False
            data['daily_requests'] = 1

# Function to allow a group to use the bot
async def allow_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("You do not have permission to use this command.")
        return

    chat_id = update.effective_chat.id

    if len(context.args) != 2:
        await update.message.reply_text("Usage: /allow <daily_limit> <days>")
        return

    try:
        # Lấy số lượt và thời hạn từ tham số
        daily_limit = int(context.args[0])
        days = int(context.args[1])

        # Thêm nhóm vào danh sách allowed_groups
        allowed_groups.add(chat_id)

        # Cập nhật thông tin nhóm
        expiry_date = datetime.now() + timedelta(days=days)
        allowed_groups_info[chat_id] = {
            "daily_limit": daily_limit,
            "expiry_date": expiry_date,
            "remaining_today": daily_limit,  # Khởi tạo lượt sử dụng trong ngày
        }

        await update.message.reply_text(
            f"✅ This group is allowed to use the bot with the following settings:\n"
            f"- Daily Limit: {daily_limit} requests/day\n"
            f"- Valid for: {days} days (Expires on {expiry_date.strftime('%Y-%m-%d')})"
        )
    except ValueError:
        await update.message.reply_text("Please provide valid numbers for daily limit and days.")

# Command to check user's remaining daily requests and VIP status
async def check_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_info = user_data.get(user_id, None)

    if not user_info:
        # Initialize user as free user
        user_data[user_id] = {'likes': 0, 'daily_requests': 1, 'expiry_date': None, 'vip': False}
        user_info = user_data[user_id]

    # Free request status
    free_request_status = f"✅ {user_info['daily_requests']}/1" if user_info['daily_requests'] > 0 else "❌ 0/1"
    
    # VIP status and daily limits
    vip_status = "✅ Yes" if user_info['vip'] else "❌ NO"
    remaining_requests = f"✅ {user_info['likes']}/99" if user_info['vip'] else "❌ 0/0"

    # Reset time for daily requests (Sri Lanka Time)
    reset_time = "1:30 AM Sri Lankan Time"

    message = (
        f"📊 Daily Free Request: {free_request_status}\n"
        f"🔹 Likes Access: {vip_status}\n"
        f"🕒 Next Reset Time: {reset_time}\n\n"
        f"🔸 Admin Allowed Amount: {remaining_requests}\n"
        f"📅 Access Expires At: {user_info['expiry_date'].strftime('%d/%m/%Y') if user_info['vip'] else 'N/A'}"
    )

    await update.message.reply_text(message)

# Command to set promotion text for a group
async def set_promotion_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Kiểm tra xem người dùng có phải admin không
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("You do not have permission to use this command.")
        return

    chat_id = update.effective_chat.id

    if len(context.args) < 1:
        await update.message.reply_text("Usage: /setpromotion <text>")
        return

    # Lưu toàn bộ nội dung từ lệnh, giữ nguyên định dạng
    promotion_text = update.message.text.split(" ", 1)[1]
    group_promotions[chat_id] = promotion_text

    await update.message.reply_text(f"Promotion text has been set:\n{promotion_text}")
# Command to add VIP status to a user (only accessible by admins)
async def add_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("You do not have permission to use this command.")
        return

    try:
        user_id = int(context.args[0])
        amount = int(context.args[1])
        days = int(context.args[2])

        if user_id not in user_data:
            user_data[user_id] = {'likes': 0, 'daily_requests': 1, 'expiry_date': None, 'vip': False}

        # Update user VIP status
        user_data[user_id]['vip'] = True
        user_data[user_id]['likes'] = amount
        user_data[user_id]['expiry_date'] = datetime.now() + timedelta(days=days)

        await update.message.reply_text(
            f"✅ User ID {user_id} has been given {amount} requests per day for {days} days. VIP access granted."
        )
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /add <user_id> <amount> <days>")

async def reset_handler(context: ContextTypes.DEFAULT_TYPE) -> None:
    now = datetime.now()
    for chat_id, info in allowed_groups_info.items():
        if info["expiry_date"] > now:
            # Reset số lượt sử dụng cho nhóm trong ngày
            info["remaining_today"] = info["daily_limit"]
# Command to handle the like request
# Update the like_handler to include promotion
async def like_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if chat_id not in allowed_groups:
        await update.message.reply_text("This group is not allowed to use the bot.")
        return

    # Kiểm tra số lượt còn lại của nhóm
    group_info = allowed_groups_info.get(chat_id, None)
    if not group_info or group_info["remaining_today"] <= 0:
        await update.message.reply_text("The group has used all daily requests. Please wait until reset or Contact📞 @loiradimas to upgrade.")
        return

    # Kiểm tra số lượt còn lại của người dùng
    user_info = user_data.get(user_id, {'likes': 0, 'daily_requests': 1, 'vip': False})
    if user_info['daily_requests'] <= 0 and not user_info['vip']:
        await update.message.reply_text("You have exceeded your daily free request limit. Please Contact📞 @loiradimas to renew your access.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("Please provide a valid region and UID. Example: /like br 10000001")
        return

    region = context.args[0]
    uid = context.args[1]
    api_url = f"https://likes.api.freefireofficial.com/api/br/{uid}?key=luis_carlos"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        response_data = data.get("response", {})

        if response_data.get("status") == 3:
            await update.message.reply_text(f"UID {uid} has already received Max Likes for Today. Please Try a different UID.")
        elif "LikesGivenByAPI" in response_data:
            # Lấy thông tin từ API
            likes_before = response_data.get("LikesbeforeCommand", 0)
            likes_after = response_data.get("LikesafterCommand", 0)
            likes_given = response_data.get("LikesGivenByAPI", 0)
            player_name = response_data.get("PlayerNickname", "Unknown")
            player_level = response_data.get("PlayerLevel", "Unknown")

            # Cập nhật lượt sử dụng
            if user_info['vip']:
                user_info['likes'] -= 1
            else:
                user_info['daily_requests'] -= 1

            # Trừ lượt của nhóm
            group_info["remaining_today"] -= 1

            # Lấy nội dung quảng bá
            promotion = group_promotions.get(chat_id, "")
            promotion_text = f"\n\n{promotion}" if promotion else ""

            # Hiển thị kết quả
            result_message = (
                f"Player Name: {player_name}\n"
                f"Player UID: {uid}\n"
                f"Level: {player_level}\n"
                f"Likes before: {likes_before}\n"
                f"Likes after: {likes_after}\n"
                f"Likes given: {likes_given}{promotion_text}"
            )
            await update.message.reply_text(result_message)
        else:
            await update.message.reply_text("Player has reached max likes today!")
    else:
        await update.message.reply_text("An error occurred. Please check account region or try again later.")
 # Command to check remaining requests and days for a group
async def remain_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id

    # Kiểm tra nếu nhóm có trong danh sách được phép
    if chat_id not in allowed_groups_info:
        await update.message.reply_text("This group is not allowed to use the bot.")
        return

    group_info = allowed_groups_info[chat_id]
    now = datetime.now()

    # Tính số ngày còn lại
    remaining_days = (group_info["expiry_date"] - now).days
    if remaining_days < 0:
        await update.message.reply_text("The Daily Request Amount has been Over. Please Wait till Cycle Reset or Contact @Nishantsarkar10k to Upgrade Your Package!")
        return

    # Lấy thông tin số lượt còn lại
    remaining_requests = group_info.get("remaining_today", 0)
    daily_limit = group_info.get("daily_limit", 0)

    # Trả về kết quả theo mẫu
    message = (
        f"Remaining requests: {remaining_requests}/{daily_limit}\n"
        f"Remaining days: {remaining_days}"
    )
    await update.message.reply_text(message)
# Main function to run the bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Khởi tạo JobQueue
    job_queue = application.job_queue

    # Thêm các lệnh xử lý
    application.add_handler(CommandHandler("allow", allow_handler))
    application.add_handler(CommandHandler("check", check_handler))
    application.add_handler(CommandHandler("remain", remain_handler))
    application.add_handler(CommandHandler("add", add_handler))
    application.add_handler(CommandHandler("like", like_handler))
    application.add_handler(CommandHandler("setpromotion", set_promotion_handler))

    # Thêm Job để reset hàng ngày
    job_queue.run_daily(reset_handler, time=time(hour=1, minute=30))

    # Chạy bot
    application.run_polling()

if __name__ == '__main__':
    main()