import telebot
import random
import string
import time
import os
from flask import Flask
import threading
from instagrapi import Client

# 1. Setup
API_TOKEN = '8533275704:AAHMcQjRpo_ROgiUvJIE6SwrEcyTAGOCDyE'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# 2. Gmail Trick Logic (Ek email, hazar account)
def get_smart_email(base_email):
    name, domain = base_email.split('@')
    if 'gmail' in domain:
        # Instagram trick: shivigupta537+anynumber@gmail.com
        return f"{name}+{random.randint(11, 999)}@{domain}"
    return base_email

# 3. Human Details (Taaki account real lage)
def get_random_human():
    first_names = ["Rahul", "Sonia", "Amit", "Priya", "Vikram", "Sneha"]
    last_names = ["Gupta", "Sharma", "Verma", "Singh", "Khan"]
    bios = ["Explorer 🌍 | Techie 💻", "Living life one day at a time ✨", "Coffee Lover ☕", "Dream Big 🌙"]
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    user = f"{name.lower().replace(' ', '_')}_{random.randint(100, 999)}"
    return name, user, random.choice(bios)

@bot.message_handler(commands=['create'])
def ask_email(message):
    msg = bot.reply_to(message, "Apni Gmail ID bhejiye (Main isse multiple accounts banaunga):")
    bot.register_next_step_handler(msg, start_process)

def start_process(message):
    base_email = message.text
    smart_email = get_smart_email(base_email)
    full_name, user, bio = get_random_human()
    pw = "Pass_" + "".join(random.choices(string.digits, k=6))
    
    cl = Client()
    bot.send_message(message.chat.id, f"🤖 **Creating Human-like Account:**\n📧 Trick Email: `{smart_email}`\n👤 Username: `{user}`\n🔑 Password: `{pw}`")

    try:
        # Corrected Instagrapi Function
        cl.send_verification_code(smart_email)
        msg = bot.send_message(message.chat.id, "📩 Instagram ne usi Gmail par OTP bheja hai. Enter karein:")
        bot.register_next_step_handler(msg, lambda m: finalize(m, cl, smart_email, user, pw, full_name))
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}")

def finalize(message, cl, email, user, pw, name):
    otp = message.text
    try:
        # Account register karna
        cl.account_register_verify_code(email, otp, user, pw, name)
        cookies = cl.get_cookies()
        bot.send_message(message.chat.id, f"✅ Done! Ek hi email se naya account ban gaya.\n\n🍪 **Cookies:**\n`{cookies}`")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Failed: {str(e)}")

@app.route('/')
def home(): return "Bot is Alive!"

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    bot.infinity_polling()
