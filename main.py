import telebot
import random
import string
import os
import time
from flask import Flask
import threading
from instagrapi import Client

# 1. Bot Configuration
API_TOKEN = '8533275704:AAHMcQjRpo_ROgiUvJIE6SwrEcyTAGOCDyE'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Gmail Alias Logic
def get_smart_email(base_email):
    name, domain = base_email.split('@')
    return f"{name}+{random.randint(1000, 9999)}@{domain}"

@bot.message_handler(commands=['create'])
def start_registration(message):
    bot.send_message(message.chat.id, "🤖 **Secure System Initialized.**")
    time.sleep(1)
    msg = bot.send_message(message.chat.id, "📧 **Step 1:** Please provide your Gmail address to begin the process:")
    bot.register_next_step_handler(msg, process_step_1)

def process_step_1(message):
    base_email = message.text
    smart_email = get_smart_email(base_email)
    
    # Professional human details
    first_names = ["Vikram", "Sana", "Aryan", "Riya", "Karan"]
    last_names = ["Malhotra", "Verma", "Gupta", "Sharma"]
    full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
    user = f"{full_name.lower().replace(' ', '_')}_{random.randint(10, 999)}"
    pw = "Secure_" + "".join(random.choices(string.digits, k=4))
    
    bot.send_message(message.chat.id, "⚙️ **Step 2: Configuring Profile Metadata...**")
    time.sleep(2)
    bot.send_message(message.chat.id, f"✅ **Configuration Complete:**\n\n👤 **Name:** {full_name}\n🆔 **Username:** `{user}`\n🔑 **Password:** `{pw}`\n📧 **Target Email:** `{smart_email}`")
    
    time.sleep(1)
    bot.send_message(message.chat.id, "🛰️ **Step 3: Sending Registration Signal to Instagram...**")
    
    cl = Client()
    try:
        # Stable registration method
        cl.account_register_email_send_code(smart_email)
        msg = bot.send_message(message.chat.id, "📩 **Step 4: Verification Dispatched.** Check your Gmail and enter the 6-digit OTP:")
        bot.register_next_step_handler(msg, lambda m: finalize(m, cl, smart_email, user, pw, full_name))
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ **System Busy:** Instagram is currently limiting requests. Please retry in 5-10 minutes.")

def finalize(message, cl, email, user, pw, name):
    otp = message.text
    bot.send_message(message.chat.id, "⌛ **Step 5: Verifying Credentials...**")
    time.sleep(3)
    try:
        cl.account_register_email_verify_code(email, otp, user, pw, name)
        cookies = cl.get_cookies()
        bot.send_message(message.chat.id, f"🎊 **Success! Registration Finalized.**\n\n🍪 **Session Cookies:**\n`{cookies}`")
    except Exception as e:
        bot.send_message(message.chat.id, "❌ **Error:** Verification failed. Ensure the OTP is correct.")

@app.route('/')
def home(): return "Professional System: Online"

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    bot.infinity_polling()
