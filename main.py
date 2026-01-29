import telebot
import random
import string
from flask import Flask
import threading
import os

# 1. Aapka Telegram Bot Token
API_TOKEN = '8533275704:AAHMcQjRpo_ROgiUvJIE6SwrEcyTAGOCDyE'
bot = telebot.TeleBot(API_TOKEN)

# 2. Flask Setup (Render ko zinda rakhne ke liye)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# 3. Random Username aur Password Banane Wala Function
def generate_details():
    user = 'user_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    pw = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    return user, pw

# 4. Bot Commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Instagram Auto-Bot taiyar hai! 🤖\nAccount banane ke liye /create likhein.")

@bot.message_handler(commands=['create'])
def start_creation(message):
    msg = bot.reply_to(message, "Sirf apni **Email ID** bhejiye. Username aur Password bot khud bana lega!")
    bot.register_next_step_handler(msg, process_email)

def process_email(message):
    email = message.text
    user, pw = generate_details()
    
    # Bot details generate karke dikhayega
    bot.send_message(message.chat.id, f"✅ Details Generated:\n👤 Username: {user}\n🔑 Password: {pw}\n📧 Email: {email}")
    
    # Yahan Instagram OTP ka process shuru hoga (Instagrapi ke saath)
    bot.send_message(message.chat.id, "Wait... Instagram ko OTP bhej diya gaya hai. OTP milte hi yahan enter karein!")

# 5. Bot Start Karna
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("Bot is starting...")
    bot.infinity_polling()
