import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
#use pip install python-Telegram-bot==20.0
# Bot Token
BOT_TOKEN = "YOUR_BOT_TOKEN"

# API Fetch Function
def get_api_data(user_id):
    api_url = "https://keyherlyswar.x10.mx/Apidocs/getinfoff.php"
    response = requests.get(api_url, params={"id": user_id})

    if response.status_code == 200:
        data = response.json()
        message = (
            f"ACCOUNT INFO:\n"
f"┌ 👤 ACCOUNT BASIC INFO\n"
f"├─ Name: {data.get('Account Name', 'Not Found')}\n"
f"├─ UID: {data.get('Account UID', 'Not Found')}\n"
f"├─ Level: {data.get('Account Level', 'Not Found')} (Exp: {data.get('Account XP', 'Not Found')})\n"
f"├─ Region: {data.get('Account Region', 'Not Found')}\n"
f"├─ Likes: {data.get('Account Likes', 'Not Found')}\n"
f"├─ Honor Score: {data.get('Account Honor Score', 'Not Found')}\n"
f"├─ Celebrity Status: {data.get('Account Celebrity Status', 'Not Found')}\n"
f"├─ Evo Access Badge : {data.get('Account Evo Access Badge', 'Not Found')}\n"
f"├─ Title: {data.get('Equipped Title', 'Not Found')}\n"
f"└─ Signature: {data.get('Account Signature', 'Not Found')}\n\n"
f"┌ 🎮 ACCOUNT ACTIVITY\n"
f"├─ Most Recent OB: {data.get('Account Recent OB', 'Not Found')}\n"
f"├─ Fire Pass: {data.get('Account Booyah Pass', 'Not Found')}\n"
f"├─ Current BP Badges: {data.get('Account Booyah Pass Badges', 'Not Found')}\n"
f"├─ BR Rank: {data.get('BR Rank', 'Not Found')} ({data.get('BR Rank Points', 'Not Found')})\n"
f"├─ CS Points: {data.get('CS Rank Points', 'Not Found')}\n"
f"├─ Created At: {data.get('Account Create Time (GMT 0530)', 'Not Found')}\n"
f"└─ Last Login: {data.get('Account Last Login (GMT 0530)', 'Not Found')}\n\n"
f"┌ 👕 ACCOUNT OVERVIEW\n"
f"├─ Avatar ID: {data.get('Account Avatar Image', 'Not Found')}\n"
f"├─ Banner ID: {data.get('Account Banner Image', 'Not Found')}\n"
f"├─ Pin ID: {data.get('Account Pin Image', 'Not Found')}\n"
f"└─ Outfits: Graphically Presented Below! 😉\n\n"
f"┌ 🐾 PET DETAILS\n"
f"├─ Equipped?: {data.get('Equipped Pet Information', {}).get('Selected?', 'Not Found')}\n"
f"├─ Pet Name: {data.get('Equipped Pet Information', {}).get('Pet Name', 'Not Found')}\n"
f"├─ Pet Type: {data.get('Equipped Pet Information', {}).get('Pet Type', 'Not Found')}\n"
f"├─ Pet Exp: {data.get('Equipped Pet Information', {}).get('Pet XP', 'Not Found')}\n"
f"└─ Pet Level: {data.get('Equipped Pet Information', {}).get('Pet Level', 'Not Found')}\n\n"
f"┌ 🛡️ GUILD INFO\n"
f"├─ Guild Name: {data.get('Guild Information', {}).get('Guild Name', 'Not Found')}\n"
f"├─ Guild ID: {data.get('Guild Information', {}).get('Guild ID', 'Not Found')}\n"
f"├─ Guild Level: {data.get('Guild Information', {}).get('Guild Level', 'Not Found')}\n"
f"├─ Live Members: {data.get('Guild Information', {}).get('Guild Current Members', 'Not Found')}\n"
f"└─ Leader Info:\n"
f"    ├─ Leader Name: {data.get('Guild Leader Information', {}).get('Leader Name', 'Not Found')}\n"
f"    ├─ Leader UID: {data.get('Guild Leader Information', {}).get('Leader UID', 'Not Found')}\n"
f"    ├─ Leader Level: {data.get('Guild Leader Information', {}).get('Leader Level', 'Not Found')} (Exp: {data.get('Guild Leader Information', {}).get('Leader XP', 'Not Found')})\n"
f"    ├─ Leader Created At: {data.get('Guild Leader Information', {}).get('Leader Ac Created Time (GMT 0530)', 'Not Found')}\n"
f"    ├─ Leader Last Login: {data.get('Guild Leader Information', {}).get('Leader Last Login Time (GMT 0530)', 'Not Found')}\n"
f"    ├─ Leader Title: {data.get('Guild Leader Information', {}).get('Leader Title', 'Not Found')}\n"
f"    ├─ Leader Current BP Badges: {data.get('Guild Leader Information', {}).get('Leader BP Badges', 'Not Found')}\n"
f"    ├─ Leader BR Points: {data.get('Guild Leader Information', {}).get('Leader BR Points', 'Not Found')}\n"
f"    └─ Leader CS Points: {data.get('Guild Leader Information', {}).get('Leader CS Points', 'Not Found')}\n\n"
f"┌ 🗺️ PUBLIC CRAFTLAND MAPS\n"
f"Not Found\n\n"
        #f"add more"
        )
        return message
    else:
        return "Failed to fetch data. Please check the ID or try again later."

async def handle_get_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip()  
    if message.startswith("Get"):  #change Get with your command
        try:
            user_id = message.split(" ")[1]
            if user_id.isdigit(): 
                loading_message = await update.message.reply_text("⏳ Fetching account data, please wait...")
                
                
                data_message = get_api_data(user_id)
                
                
                await loading_message.edit_text(data_message)
            else:
                await update.message.reply_text("⚠️ Please enter a valid numeric ID after 'Get'.\nExample: Get 123456")
        except IndexError:
            await update.message.reply_text("⚠️ Please enter an ID after 'Get'.\nExample: Get 123456")

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handler for GET commands
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_command))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
