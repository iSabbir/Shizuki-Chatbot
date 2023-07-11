import os
import json
import requests
from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, MessageHandler, Filters

# Replace TOKEN with your bot token
TOKEN = "BOT_TOKEN"
bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)

def handle_message(update, context):
    message = update.message.text
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    # Show typing status
    bot.send_chat_action(chat_id, "typing")

    # Get response from API
    response = requests.get(
        "http://api.safone.me/chatbot",
        params={"query": message, "user_id": user_id},
        headers={"accept": "application/json"}
    )

    if response.status_code == 200:
        data = response.json()
        answer = data["response"]
    else:
        answer = "Sorry, I'm unable to process your request right now."

    # Add custom text to the answer
    answer += "\n\n- Developed By @BDBOTS"

    # Create an inline keyboard button
    buy_bots_button = InlineKeyboardButton(text="Buy Bots", url="https://t.me/BDBOTS/122")
    keyboard = InlineKeyboardMarkup([[buy_bots_button]])

    # Send API response to the user
    bot.send_message(chat_id, answer, reply_markup=keyboard)

# Register the message handler
message_handler = MessageHandler(Filters.text & ~Filters.command, handle_message, pass_user_data=True)
updater.dispatcher.add_handler(message_handler)

# Start long polling
updater.start_polling()
updater.idle()
