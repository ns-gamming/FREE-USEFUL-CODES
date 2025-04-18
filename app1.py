import os
import json
import binascii
import warnings
import requests
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warning
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# Encryption constants
AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'

# Bot Token
BOT_TOKEN = "7662882445:AAEDJX2RiFsoxjWBPksF4qEf3b-nXDRvHKM"

# Ensure folders exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("generated", exist_ok=True)

def get_token(password, uid):
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip"
    }

    data = f"password={password}&uid={uid}".encode()
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    hex_data = binascii.hexlify(encrypted_data).decode()

    payload = f"data={hex_data}"
    response = requests.post(url, data=payload, headers=headers, verify=False)
    
    if response.status_code == 200:
        try:
            token = json.loads(response.text).get("token")
            return {"token": token}
        except:
            return None
    else:
        return None

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a .json file with guest accounts to get tokens.")

# Handle uploaded .json file
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    user_id = update.message.from_user.id

    if not file.file_name.endswith(".json"):
        await update.message.reply_text("Please upload a valid .json file.")
        return

    # Save uploaded file
    upload_path = f"uploads/{user_id}_ids.json"
    telegram_file = await file.get_file()
    await telegram_file.download_to_drive(upload_path)

    tokens = []
    with open(upload_path, "r") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                info = data.get("guest_account_info", {})
                uid = info.get("com.garena.msdk.guest_uid")
                password = info.get("com.garena.msdk.guest_password")
                token = get_token(password, uid)
                if token:
                    tokens.append(token)
            except Exception as e:
                print(f"Error processing line: {e}")

    # Save tokens to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_path = f"generated/{user_id}_tokens_{timestamp}.json"
    with open(result_path, "w") as out_file:
        json.dump(tokens, out_file, indent=4)

    # Send back to user
    await update.message.reply_document(document=InputFile(result_path), filename="tokens.json")

# Bot setup
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()