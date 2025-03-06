from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests
import time

def get_likes(ind: str, uid: str) -> dict:
    url = f"https://freefire-virusteam.vercel.app/ind/likes?key=proAmine&uid={uid}"
    response = requests.get(url)
    return response.json()

def get_spam(ind: str, uid: str) -> dict:
    url = f"https://freefire-virusteam.vercel.app/ind/spamkb?key=proAmine&uid={uid}"
    response = requests.get(url)
    return response.json()

async def check_subscription(update: Update, context: CallbackContext) -> bool:
    user_id = update.message.from_user.id
    chat_id = "CHAT_ID"
    member = await context.bot.get_chat_member(chat_id, user_id)
    return member.status in ['member', 'administrator', 'creator']
    
def save_to_file(file_name: str, uid: str, count: int):
    try:
        with open(file_name, "a") as f:
            f.write(f"{uid}, {count}\n")
    except Exception as e:
        print(f"Error saving data: {e}")

async def like(update: Update, context: CallbackContext) -> None:
    if not await check_subscription(update, context):
        await update.message.reply_text("You need to subscribe to the channel @xxxx1_41 first to use the command. 🛑")
        return

    if len(context.args) != 2:
        if len(context.args) == 1:
            await update.message.reply_text("Error: `ind` is missing! Please provide both `ind` and `uid` to proceed. 📝")
        return  

    ind = context.args[0]
    uid = context.args[1]

    message = await update.message.reply_text("Please wait, processing your request... ⏳")

    for _ in range(3):
        try:
            response = get_likes(ind, uid)
            if "status" in response and response["status"] == "Success":
                data = response.get("UID Validated - API connected", {})
                likes = response.get("Likes details", {})

                likes_before = likes.get("Likes Before CMD")
                likes_after = likes.get("Likes After CMD")
                likes_given = likes.get("Likes Given By API")
                total_likes = likes_after - likes_before
                
                save_to_file("accsind.txt", uid, total_likes)
                
                message_text = (f"**UID Validated - API connected:** 💫\n"
                                f"UID: {data.get('UID')} 🆔\n"
                                f"Name: {data.get('Name')} 🏷️\n"
                                f"Level: {data.get('Level')} 🎮\n"
                                f"Region: {data.get('Region')} 🌍\n"
                                f"Time Sent: {data.get('Time Sent')} ⏰\n\n"
                                f"**Likes details:** 👍\n"
                                f"Likes Before CMD: {likes_before} 🔼\n"
                                f"Likes After CMD: {likes_after} 🔽\n"
                                f"Likes Given By API: {likes_given} ✅\n"
                                f"Total Likes Sent: {total_likes} 💖\n"
                                f"OWNER => @Nishantsarkar10k 🇮🇳") 
                
                await message.edit_text(message_text)
                await message.reply_text("Thank you for using the service! 👍")
                break
            else:
                error_message = response.get("status", "Unknown error")
                error_code = response.get("error_code", "Unknown")
                full_error_details = response
                await message.edit_text(f"Error: ☄ {error_message} (Error code: {error_code}) 😞\n"
                                        f"Full Error Details: {full_error_details} 🔍")
                await message.reply_text("Error occurred! 😞")
                break
        except Exception as e:
            error_code = str(e)
            await message.edit_text(f"An error occurred: {error_code}. Retrying... 🔄")
            await message.reply_text("Error occurred! 😞")
            time.sleep(2)

async def spam(update: Update, context: CallbackContext) -> None:
    if not await check_subscription(update, context):
        await update.message.reply_text("You need to subscribe to the channel @xxxx1_41 first to use the command. 🛑")
        return

    if len(context.args) != 2:
        if len(context.args) == 1:
            await update.message.reply_text("Error: `ind` is missing! Please provide both `ind` and `uid` to proceed. 📝")
        return 

    ind = context.args[0]
    uid = context.args[1]

    message = await update.message.reply_text("Please wait, processing your request... ⏳")
    
    for _ in range(3):
        try:
            response = get_spam(ind, uid)
            
            if "status" in response and response["status"] == "Success":
                data = response.get("UID Validated - API connected", {})
                
                save_to_file("spamind.txt", uid, 1)

                with open("spamind.txt", "r") as file:
                    count = sum(1 for line in file if line.startswith(f"{uid},"))

                message_text = (f"**UID Validated - API connected:** 💫\n"
                                f"UID: {data.get('UID')} 🆔\n\n"
                                f"Name: {data.get('Name')} 🏷️\n\n"
                                f"Level: {data.get('Level')} 🎮\n\n"
                                f"Region: {data.get('Region')} 🌍\n\n"
                                f"Spam request has been sent for this UID {count} times. 🎯")
                
                await message.edit_text(message_text)
                await message.reply_text("Spam request sent successfully! 👍")
                break
            else:
                error_message = response.get("status", "Unknown error")
                error_code = response.get("error_code", "Unknown")
                full_error_details = response
                await message.edit_text(f"Error: ☄ {error_message} (Error code: {error_code}) 😞\n"
                                        f"Full Error Details: {full_error_details} 🔍")
                await message.reply_text("Error occurred! 😞")
                break
        except Exception as e:
            error_code = str(e)
            await message.edit_text(f"An error occurred: {error_code}. Retrying... 🔄")
            await message.reply_text("Error occurred! 😞")
            time.sleep(2)

def main():
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    application.add_handler(CommandHandler("like", like))
    application.add_handler(CommandHandler("spam", spam))

    application.run_polling()

if __name__ == '__main__':
    main()
