import telebot
import random
import string
import os
from flask import Flask
import threading
from instagrapi import Client

# 1. Bot Configuration
API_TOKEN = '8533275704:AAHMcQjRpo_ROgiUvJIE6SwrEcyTAGOCDyE'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# 2. Gmail Alias Logic
def get_smart_email(base_email):
    if '@gmail.com' in base_email:
        name, domain = base_email.split('@')
        return f"{name}+{random.randint(100, 9999)}@{domain}"
    return base_email

# 3. Bot Handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🚀 **Welcome to Instagram Automation Bot.**\nPlease use the `/create` command to start the account registration process.")

@bot.message_handler(commands=['create'])
def ask_email(message):
    msg = bot.reply_to(message, "📧 **Request Initiated.**\nPlease provide your Gmail address to begin.")
    bot.register_next_step_handler(msg, start_process)

def start_process(message):
    base_email = message.text
    smart_email = get_smart_email(base_email)
    
    # Professional Profile Details
    first_names = ["Vikram", "Sana", "Aryan", "Riya", "Karan", "Anjali"]
    last_names = ["Sharma", "Malhotra", "Gupta", "Khan", "Verma"]
    full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
    user = f"{full_name.lower().replace(' ', '_')}_{random.randint(10, 999)}"
    pw = "Pass_" + "".join(random.choices(string.digits, k=6))
    
    cl = Client()
    bot.send_message(message.chat.id, f"⚙️ **Generating Account Credentials:**\n\n🔹 **Email:** `{smart_email}`\n🔹 **Username:** `{user}`\n🔹 **Password:** `{pw}`\n\n*Sending verification code to Instagram...*")

    try:
        cl.account_register_email_send_code(smart_email)
        msg = bot.send_message(message.chat.id, "📩 **Verification Code Sent.**\nPlease check your Gmail inbox and enter the 6-digit OTP below:")
        bot.register_next_step_handler(msg, lambda m: finalize(m, cl, smart_email, user, pw, full_name))
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ **System Error:** {str(e)}\n_Please try again after a few minutes._")

def finalize(message, cl, email, user, pw, name):
    otp = message.text
    bot.send_message(message.chat.id, "⏳ **Verifying OTP and Finalizing Account...**")
    try:
        cl.account_register_email_verify_code(email, otp, user, pw, name)
        cookies = cl.get_cookies()
        bot.send_message(message.chat.id, f"✅ **Account Successfully Created!**\n\n📌 **Session Cookies:**\n`{cookies}`\n\n_You can now use these cookies for your automation tasks._")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ **Verification Failed:** {str(e)}")

@app.route('/')
def home(): return "Service Status: Online"

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    bot.infinity_polling()
