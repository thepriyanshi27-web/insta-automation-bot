import telebot
import random
import string
import os
import time
import threading
from flask import Flask
from instagrapi import Client

# 1. Configuration
API_TOKEN = '8533275704:AAHMcQjRpo_ROgiUvJIE6SwrEcyTAGOCDyE'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "System Online"

def get_alias_email(email):
    name, domain = email.split('@')
    return f"{name}+{random.randint(1000, 9999)}@{domain}"

@bot.message_handler(commands=['create'])
def start_cmd(message):
    msg = bot.send_message(message.chat.id, "📧 **Step 1:** Please provide your Gmail address:")
    bot.register_next_step_handler(msg, process_request)

def process_request(message):
    email = message.text
    alias_email = get_alias_email(email)
    user = f"user_{random.randint(10, 999)}_{''.join(random.choices(string.ascii_lowercase, k=3))}"
    pw = "Secure_" + "".join(random.choices(string.digits, k=4))
    
    bot.send_message(message.chat.id, f"⚙️ **Step 2: Credentials Generated.**\n\n👤 **User:** `{user}`\n🔑 **Pass:** `{pw}`\n📧 **Alias:** `{alias_email}`")
    
    cl = Client()
    bot.send_message(message.chat.id, "🛰️ **Step 3: Attempting to bypass Instagram security...**")
    
    # Error-Proofing: Try all possible methods
    success = False
    methods = ['account_register_email_send_code', 'send_verification_code']
    
    for method_name in methods:
        method = getattr(cl, method_name, None)
        if method:
            try:
                method(alias_email)
                success = True
                break
            except Exception:
                continue

    if success:
        msg = bot.send_message(message.chat.id, "📩 **Step 4: OTP Sent.** Enter the 6-digit code from your Gmail:")
        bot.register_next_step_handler(msg, lambda m: finalize(m, cl, alias_email, user, pw))
    else:
        bot.send_message(message.chat.id, "⚠️ **System Busy:** Instagram is blocking the request. Please wait 15-20 minutes and try again.")

def finalize(message, cl, email, user, pw):
    otp = message.text
    bot.send_message(message.chat.id, "⌛ **Step 5: Verifying and extracting cookies...**")
    try:
        # Final registration attempt
        cl.account_register_email_verify_code(email, otp, user, pw, user)
        cookies = cl.get_cookies()
        bot.send_message(message.chat.id, f"✅ **Account Created!**\n\n🍪 **Cookies:**\n`{cookies}`")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ **Finalization Error:** {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))).start()
    bot.infinity_polling()
