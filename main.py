import telebot
from instagrapi import Client
from flask import Flask
import threading
import os

# --- Render Free Plan Trick ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is Alive!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Flask ko background mein start karein taaki Render ise website samjhe
threading.Thread(target=run_flask).start()
# ------------------------------

bot = telebot.TeleBot('8533275704:AAHMcQjRpo_ROgiUvJIE6SwrEcyTAGOCDyE')
cl = Client()

@bot.message_handler(commands=['start', 'create'])
def ask_details(message):
    msg = bot.reply_to(message, "📧 Bhejiye: email,password,username")
    bot.register_next_step_handler(msg, process_reg)

def process_reg(message):
    try:
        e, p, u = message.text.split(',')
        cl.account_register_email_send_code(e)
        msg = bot.reply_to(message, "🔑 OTP bhejiye:")
        bot.register_next_step_handler(msg, lambda m: finalize(m, e, p, u))
    except:
        bot.reply_to(message, "❌ Format: email,pass,user")

def finalize(message, e, p, u):
    try:
        cl.account_register_email_verify_code(e, message.text)
        cl.account_create(u, p, e)
        bot.send_message(message.chat.id, f"✅ Account Done!\nUser: {u}")
    except Exception as err:
        bot.reply_to(message, f"❌ Fail: {str(err)}")

print("Bot starting...")
bot.polling()

