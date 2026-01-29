import telebot
from instagrapi import Client

# Aapka Telegram Bot Token
bot = telebot.TeleBot('8533275704:AAHMcQjRpo_ROgiUvJIE6SwrEcyTAGOCDyE')
cl = Client()

@bot.message_handler(commands=['create'])
def ask_details(message):
    msg = bot.reply_to(message, "📧 Bhejiye (Format: email,password,username):")
    bot.register_next_step_handler(msg, process_registration)

def process_registration(message):
    try:
        e, p, u = message.text.split(',')
        cl.account_register_email_send_code(e)
        msg = bot.reply_to(message, "🔑 Instagram ne OTP bheja hai. Wo yahan likhein:")
        bot.register_next_step_handler(msg, lambda m: finalize(m, e, p, u))
    except:
        bot.reply_to(message, "❌ Galat format! Please use: email,pass,user")

def finalize(message, e, p, u):
    try:
        cl.account_register_email_verify_code(e, message.text)
        cl.account_create(u, p, e)
        bot.send_message(message.chat.id, f"✅ Account Created!\n👤 User: {u}\n🍪 Cookies: {str(cl.get_cookies())}")
    except Exception as err:
        bot.reply_to(message, f"❌ Fail: {str(err)}")

print("Bot is ready...")
bot.polling()
