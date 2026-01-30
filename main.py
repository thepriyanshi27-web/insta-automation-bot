import telebot
import random
import string
import os
import time
from flask import Flask
import threading
from instagrapi import Client

# 1. Bot Setup
API_TOKEN = '8533275704:AAHMcQjRpo_ROgiUvJIE6SwrEcyTAGOCDyE'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

def get_smart_email(base_email):
    name, domain = base_email.split('@')
    return f"{name}+{random.randint(1000, 9999)}@{domain}"

@bot.message_handler(commands=['create'])
def start_registration(message):
    bot.send_message(message.chat.id, "🤖 **Secure System Initialized.**")
    msg = bot.send_message(message.chat.id, "📧 **Step 1:** Please provide your Gmail address to begin:")
    bot.register_next_step_handler(msg, process_step_1)

def process_step_1(message):
    base_email = message.text
    smart_email = get_smart_email(base_email)
    
    # Professional Human Details
    full_name = random.choice(["Aryan Malhotra", "Sana Sharma", "Vikram Gupta", "Riya Verma"])
    user = f"{full_name.lower().replace(' ', '_')}_{random.randint(100, 999)}"
    pw = "Secure_" + "".join(random.choices(string.digits, k=4))
    
    bot.send_message(message.chat.id, "⚙️ **Step 2: Configuring Metadata...**")
    time.sleep(1)
    bot.send_message(message.chat.id, f"✅ **Config Ready:**\n\n👤 **User:** `{user}`\n🔑 **Pass:** `{pw}`\n📧 **Email:** `{smart_email}`")
    
    bot.send_message(message.chat.id, "🛰️ **Step 3: Dispatched OTP request to Instagram.**")
    
    cl = Client()
    success = False
    
    # Trying all possible methods to send OTP
    try:
        cl.account_register_email_send_code(smart_email)
        success = True
    except Exception:
        try:
            # Fallback method
            cl.send_verification_code(smart_email)
            success = True
        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ **Instagram server is busy.** Please wait 10 minutes and try again.\nSystem Info: {str(e)}")

    if success:
        msg = bot.send_message(message.chat.id, "📩 **Step 4: OTP Sent.** Please enter the 6-digit code from your Gmail:")
        bot.register_next_step_handler(msg, lambda m: finalize(m, cl, smart_email, user, pw, full_name))

def finalize(message, cl, email, user, pw, name):
    otp = message.text
    bot.send_message(message.chat.id, "⌛ **Step 5: Verifying and extracting Session Cookies...**")
    try:
        cl.account_register_email_verify_code(email, otp, user, pw, name)
        cookies = cl.get_cookies()
        bot.send_message(message.chat.id, f"🎊 **Success! Account Registered.**\n\n🍪 **Cookies:**\n`{cookies}`")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ **Failed:** Verification error. Please check the OTP.")

@app.route('/')
def home(): return "Bot Status: Online"

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    bot.infinity_polling()
