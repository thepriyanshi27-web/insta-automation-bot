import telebot
from instagrapi import Client
from flask import Flask
import threading
import os
import random
import string

# --- Render Free Plan Trick ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

threading.Thread(target=run_flask).start()
# ------------------------------

bot = telebot.TeleBot('8533275704:AAHMcQjRpo_ROgiUvJIE6SwrEcyTAGOCDyE')
cl = Client()

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@bot.message_handler(commands=['create'])
def start_reg(message):
    msg = bot.reply_to(message, "📧 Bas apni Email ID bhejiye:")
    bot.register_next_step_handler(msg, process_email)

def process_email(message):
    email = message.text.strip()
    # Password aur Username khud se generate karna
    password = generate_random_string(12) 
    username = "bot_user_" + generate_random_string(5)
    
    bot.send_message(message.chat.id, f"⏳ Generating Details...\n👤 User: {username}\n🔑 Pass: {password}")
    
    try:
        # Instagram ko OTP bhejne ka order dena
        cl.account_register_email_send_code(email)
        msg = bot.reply_to(message, "🔑 Instagram ne OTP bheja hai. Wo yahan likhein:")
        bot.register_next_step_handler(msg, lambda m: finalize(m, email, password, username))
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

def finalize(message, email, password, username):
    otp = message.text.strip()
    try:
        bot.send_message(message.chat.id, "🔄 OTP verify ho raha hai aur account ban raha hai...")
        cl.account_register_email_verify_code(email, otp)
        cl.account_create(username, password, email)
        
        # Cookies nikal kar Markdown format mein dena
        cookies = cl.get_cookies()
        bot.send_message(message.chat.id, f"✅ Account Created!\n👤 User: `{username}`\n🔑 Pass: `{password}`\n🍪 Cookies:\n`{str(cookies)}`", parse_mode="Markdown")
    except Exception as err:
        bot.reply_to(message, f"❌ Failed: {str(err)}")

bot.polling()
