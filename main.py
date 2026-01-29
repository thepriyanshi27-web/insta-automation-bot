import telebot
import random
import string
import time
from flask import Flask
import threading
import os
from instagrapi import Client

# Bot Setup
API_TOKEN = '8533275704:AAHMcQjRpo_ROgiUvJIE6SwrEcyTAGOCDyE'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Gmail Dot Trick Function
def apply_dot_trick(email):
    name, domain = email.split('@')
    if 'gmail' not in domain: return email
    # Randomly ek dot add karna
    index = random.randint(1, len(name) - 1)
    return name[:index] + '.' + name[index:] + '@' + domain

# Random Bio/Name for Human touch
def get_human_details():
    names = ["Aryan Khan", "Sana Sheikh", "Rahul Verma", "Anjali Singh"]
    bios = ["Living my best life ✨", "Tech enthusiast | Explorer", "Coffee & Code ☕", "Dreamer 🌙"]
    return random.choice(names), random.choice(bios)

@bot.message_handler(commands=['create_multi'])
def start_multi(message):
    msg = bot.reply_to(message, "Apni Gmail ID bhejiye (Main isse multiple accounts banaunga):")
    bot.register_next_step_handler(msg, process_multi)

def process_multi(message):
    base_email = message.text
    cl = Client()
    
    # 1. Dot Trick Apply karna
    smart_email = apply_dot_trick(base_email)
    user = 'insta_user_' + ''.join(random.choices(string.ascii_lowercase, k=6))
    pw = 'Pass_' + ''.join(random.choices(string.digits, k=6))
    full_name, bio = get_human_details()

    bot.send_message(message.chat.id, f"🤖 **Creating Human-like Account:**\n📧 Email: `{smart_email}`\n👤 User: `{user}`\n🔑 Pass: `{pw}`")

    try:
        # OTP bhejna
        cl.account_register_email_send_code(smart_email)
        msg = bot.send_message(message.chat.id, "📩 OTP bhej diya gaya hai. Code likhein:")
        bot.register_next_step_handler(msg, lambda m: finalize_multi(m, cl, smart_email, user, pw, full_name, bio))
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}")

def finalize_multi(message, cl, email, user, pw, name, bio):
    otp = message.text
    try:
        # Account Banana
        cl.account_register_email_verify_code(email, otp, user, pw, name)
        
        # Human touch: Bio update karna
        time.sleep(2) # Thoda gap taaki bot na lage
        cl.account_edit(full_name=name, biography=bio)
        
        # Cookies nikalna
        cookies = cl.get_cookies()
        bot.send_message(message.chat.id, f"✅ Done! Account Real lag raha hai.\n\n🍪 **Cookies:**\n`{cookies}`")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Failed: {str(e)}")

@app.route('/')
def home(): return "Multi-Bot is Alive!"

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    bot.infinity_polling()
