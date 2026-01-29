import telebot
import random
import string
from flask import Flask
import threading
import os
from instagrapi import Client

# 1. Bot Setup
API_TOKEN = '8533275704:AAHMcQjRpo_ROgiUvJIE6SwrEcyTAGOCDyE'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
cl = Client()

@app.route('/')
def home():
    return "Bot is Alive!"

# 2. Random Details Generator
def generate_details():
    user = 'user_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    pw = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    return user, pw

# 3. Bot Logic
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Instagram Auto-Bot Ready! 🤖\nAccount ke liye /create likhein.")

@bot.message_handler(commands=['create'])
def ask_email(message):
    msg = bot.reply_to(message, "Apni **Fresh Email ID** bhejiye:")
    bot.register_next_step_handler(msg, send_insta_otp)

def send_insta_otp(message):
    email = message.text
    user, pw = generate_details()
    
    bot.send_message(message.chat.id, f"⏳ Instagram ko OTP request bhej raha hoon...\n👤 User: {user}\n🔑 Pass: {pw}")
    
    try:
        # Yeh line Instagram ko real OTP bhejne par majboor karegi
        cl.account_register_email_send_code(email)
        msg = bot.send_message(message.chat.id, "✅ OTP bhej diya gaya hai! Inbox check karke 6-digit code yahan likhein:")
        bot.register_next_step_handler(msg, lambda m: finalize_account(m, email, user, pw))
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}\nTip: New email use karein ya 5 min baad try karein.")

def finalize_account(message, email, user, pw):
    otp = message.text
    try:
        # Account create karna aur cookies nikalna
        result = cl.account_register_email_verify_code(email, otp, user, pw)
        cookies = cl.get_cookies()
        bot.send_message(message.chat.id, f"🎉 Account Ban Gaya!\n\n🍪 **Cookies:**\n`{cookies}`")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ OTP Verification Failed: {str(e)}")

# 4. Start
if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    bot.infinity_polling()
