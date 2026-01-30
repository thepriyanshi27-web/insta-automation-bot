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

def get_smart_email(base_email):
    name, domain = base_email.split('@')
    return f"{name}+{random.randint(1000, 9999)}@{domain}"

@bot.message_handler(commands=['create'])
def ask_email(message):
    msg = bot.reply_to(message, "📧 **Request Initiated.** Please provide your Gmail address:")
    bot.register_next_step_handler(msg, start_process)

def start_process(message):
    base_email = message.text
    smart_email = get_smart_email(base_email)
    
    # Professional human details
    full_name = random.choice(["Vikram Malhotra", "Sana Verma", "Aryan Gupta"])
    user = f"{full_name.lower().replace(' ', '_')}_{random.randint(10, 999)}"
    pw = "Pass_" + "".join(random.choices(string.digits, k=6))
    
    cl = Client()
    bot.send_message(message.chat.id, f"⚙️ **Generating Credentials:**\n\n🔹 **Email:** `{smart_email}`\n🔹 **User:** `{user}`\n🔹 **Pass:** `{pw}`")

    try:
        # Latest stable function for OTP
        cl.account_register_email_send_code(smart_email)
        msg = bot.send_message(message.chat.id, "📩 **OTP Sent!** Please check your Gmail (including Spam) and enter the code:")
        bot.register_next_step_handler(msg, lambda m: finalize(m, cl, smart_email, user, pw, full_name))
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ **API Error:** {str(e)}\n\n_Note: If you see an AttributeError, please 'Clear Build Cache' on Render._")

def finalize(message, cl, email, user, pw, name):
    otp = message.text
    try:
        cl.account_register_email_verify_code(email, otp, user, pw, name)
        cookies = cl.get_cookies()
        bot.send_message(message.chat.id, f"✅ **Account Created!**\n\n🍪 **Cookies:**\n`{cookies}`")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ **Failed:** {str(e)}")

@app.route('/')
def home(): return "Status: Online"

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    bot.infinity_polling()
