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

# 2. Gmail Alias Trick
def get_alias_email(email):
    name, domain = email.split('@')
    return f"{name}+{random.randint(1000, 9999)}@{domain}"

# 3. Routes & Bot Logic
@app.route('/')
def index():
    return "System Status: Online"

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🚀 **Instagram Automation System Online.**\nUse `/create` to start the registration process.")

@bot.message_handler(commands=['create'])
def ask_email(message):
    msg = bot.send_message(message.chat.id, "📧 **Step 1:** Please enter your Gmail address:")
    bot.register_next_step_handler(msg, start_process)

def start_process(message):
    base_email = message.text
    if '@' not in base_email:
        bot.send_message(message.chat.id, "❌ Invalid Email. Please try again.")
        return

    target_email = get_alias_email(base_email)
    f_name = random.choice(["Aryan", "Sana", "Vikram", "Riya"])
    l_name = random.choice(["Malhotra", "Verma", "Gupta"])
    user = f"{f_name.lower()}_{random.randint(100, 9999)}"
    pw = "Secure_" + "".join(random.choices(string.digits, k=4))
    
    bot.send_message(message.chat.id, f"⚙️ **Step 2: Profile Metadata Configured.**\n\n👤 **User:** `{user}`\n🔑 **Pass:** `{pw}`\n📧 **Email:** `{target_email}`")
    
    cl = Client()
    try:
        # Triggering OTP Request
        cl.account_register_email_send_code(target_email)
        msg = bot.send_message(message.chat.id, "📩 **Step 3: Verification Sent.** Please enter the 6-digit OTP from your Gmail:")
        bot.register_next_step_handler(msg, lambda m: finalize(m, cl, target_email, user, pw, f"{f_name} {l_name}"))
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ **Instagram Limitation:** {str(e)}\n\n_Please wait 10-15 minutes and try again._")

def finalize(message, cl, email, user, pw, name):
    otp = message.text
    bot.send_message(message.chat.id, "⌛ **Step 4: Verifying OTP and Extracting Session...**")
    try:
        cl.account_register_email_verify_code(email, otp, user, pw, name)
        cookies = cl.get_cookies()
        bot.send_message(message.chat.id, f"✅ **Account Created Successfully!**\n\n🍪 **Cookies:**\n`{cookies}`")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ **Finalization Failed:** {str(e)}")

# 4. Threading for Render
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    bot.infinity_polling()
