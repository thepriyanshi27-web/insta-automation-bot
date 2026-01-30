import telebot
import random
import string
import os
import time
import threading
from flask import Flask
from instagrapi import Client

# 1. Bot Setup
API_TOKEN = '8533275704:AAHMcQjRpo_ROgiUvJIE6SwrEcyTAGOCDyE'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# 2. Status Route
@app.route('/')
def home():
    return "Service is Online"

# 3. Email Alias Logic
def get_alias_email(email):
    name, domain = email.split('@')
    return f"{name}+{random.randint(1000, 9999)}@{domain}"

# 4. Professional Bot Commands
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🚀 **System Online.**\nUse `/create` to begin the registration process.")

@bot.message_handler(commands=['create'])
def start_cmd(message):
    msg = bot.send_message(message.chat.id, "📧 **Step 1:** Please provide your Gmail address:")
    bot.register_next_step_handler(msg, process_request)

def process_request(message):
    email = message.text
    if '@' not in email:
        bot.send_message(message.chat.id, "❌ Invalid email format. Please restart with `/create`.")
        return

    alias_email = get_alias_email(email)
    user = f"user_{random.randint(10, 999)}_{''.join(random.choices(string.ascii_lowercase, k=3))}"
    pw = "Secure_" + "".join(random.choices(string.digits, k=4))
    
    bot.send_message(message.chat.id, f"⚙️ **Step 2: Credentials Generated.**\n\n👤 **User:** `{user}`\n🔑 **Pass:** `{pw}`\n📧 **Alias:** `{alias_email}`")
    
    cl = Client()
    try:
        # Requesting OTP from Instagram
        cl.account_register_email_send_code(alias_email)
        msg = bot.send_message(message.chat.id, "📩 **Step 3: Verification Sent.** Please check your Gmail and enter the 6-digit OTP code below:")
        bot.register_next_step_handler(msg, lambda m: finalize(m, cl, alias_email, user, pw))
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ **Instagram Limitation:** {str(e)}\n\n_Tip: Wait 15 minutes and try again with the same email._")

def finalize(message, cl, email, user, pw):
    otp = message.text
    bot.send_message(message.chat.id, "⌛ **Step 4: Verifying and extracting cookies...**")
    try:
        cl.account_register_email_verify_code(email, otp, user, pw, user)
        cookies = cl.get_cookies()
        bot.send_message(message.chat.id, f"✅ **Account Successfully Created!**\n\n🍪 **Cookies:**\n`{cookies}`")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ **Finalization Error:** {str(e)}")

# 5. Threading to keep both Bot and Flask alive
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    bot.infinity_polling()
