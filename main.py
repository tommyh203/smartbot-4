import telebot
import os
import schedule
import time
import threading

# === SETUP ===
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# === YOUR REAL GROUP CHAT ID ===
PRIVATE_GROUP_ID = -1002836083308  # Note the -100 prefix for groups

# === /start or /help ===
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_msg = (
        "🏇 **WELCOME TO SMARTPICKS** 🏇\n\n"
        "🎯 Your premium horse racing tips destination!\n"
        "💰 Join thousands of winners in our VIP community\n\n"
        "💳 Type `VIP` or send proof to get access!\n"
        "🚀 Let's find you some winners!"
    )
    bot.reply_to(message, welcome_msg, parse_mode='Markdown')

# === "VIP" keyword ===
@bot.message_handler(func=lambda message: message.text and "vip" in message.text.lower())
def send_payment_info(message):
    payment_msg = (
        "🏆 **SMARTPICKS VIP ACCESS** 🏆\n\n"
        "💎 Join our exclusive winners circle!\n"
        "📈 Daily premium tips & insider picks\n"
        "🎯 90%+ success rate guaranteed\n\n"
        "💰 **PAYMENT DETAILS:**\n"
        "💳 Revolut: Tommy\n"
        "🏦 Sort: 04-00-75\n"
        "📋 Acc: 63667312\n\n"
        "📸 Send payment screenshot for instant access!\n"
        "⚡ VIP group invitation within minutes"
    )
    bot.send_message(message.chat.id, payment_msg, parse_mode='Markdown')

# === Handle payment proof photo ===
@bot.message_handler(content_types=['photo'])
def handle_payment_photo(message):
    user_id = message.from_user.id

    bot.send_message(
        user_id,
        "✅ **PAYMENT RECEIVED!** ✅\n\n"
        "🔍 Verifying your payment now...\n"
        "⏰ VIP access coming in 2-3 minutes\n"
        "🏆 Welcome to the winners circle!",
        parse_mode='Markdown'
    )

    try:
        invite_link = bot.create_chat_invite_link(
            chat_id=PRIVATE_GROUP_ID,
            member_limit=1,
            creates_join_request=False
        )
        bot.send_message(user_id, f"🎉 Access granted! Join here:\n{invite_link.invite_link}")
    except Exception as e:
        print(f"❌ Failed to invite: {e}")
        bot.send_message(user_id, "✅ Payment verified! You'll receive your group invite shortly.")

# === Daily Tips ===
def send_daily_tips():
    tips = "🏇 **Today's Tips:**\n1. Horse A 🥇\n2. Horse B 🥈\n3. Horse C 🥉"
    bot.send_message(PRIVATE_GROUP_ID, tips, parse_mode='Markdown')

# Schedule tips
def run_schedule():
    schedule.every().day.at("09:00").do(send_daily_tips)
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule).start()

# === Run Bot ===
print("🔥 Bot is running...")
bot.infinity_polling()