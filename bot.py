import telebot # Telegram Bot API Interface
from telebot import apihelper # API helper for easier usage

from chat import Chat
from rate_limiter import RateLimiter

import dotenv
dotenv.load_dotenv()
import os

print("BOT_TOKEN:", os.getenv("BOT_TOKEN"))
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))


chat = Chat()
limiter = RateLimiter()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))


@bot.message_handler(commands=["start"], chat_types=['private'])
def start(message):
    bot.reply_to(
        message,
        """Hello, esteemed user. I am Mahdi.
I will be available over the next few days to support the event by addressing your inquiries.
If you have any questions, please type the /ask command."""
    )

@bot.message_handler(commands=["ask"], chat_types=['private'])
def ask(message):
    bot.reply_to(
        message,
        f"Dear {message.from_user.first_name}, please let me know what inquiry you have."
    )
    chat.add_user(message.from_user.id)

@bot.message_handler(content_types=['text'], chat_types=['private'])
def get_response(message):
    if not chat.has_user(message.from_user.id):
        bot.reply_to(
            message,
            "If you have any questions, please begin by using the /ask command."
        )
        return
    if not limiter.access(message.from_user.id):
        bot.reply_to(
            message,
            "Please pose your question again in a few minutes. I am currently a bit overwhelmed by the volume of inquiries."
        )
        return
    if chat.count_message(message.from_user.id) > 5:
        bot.reply_to(
            message,
            "I seem to have lost track of our previous discussion. Would you kindly ask your question again, starting with the /ask command?"
        )
        return
    response = chat.chat(message.from_user.id, message.text)
    bot.reply_to(message, response)

@bot.message_handler(
    content_types=[
        'audio', 'document', 'animation', 'photo', 'sticker', 'video', 'voice'
    ],
    chat_types=['private'],
)
def unsupported_content(message):
    bot.reply_to(
        message,
        "Could you please provide text-only input? I am currently on a limited network."
    )

@bot.message_handler(
    content_types=[
        'text', 'audio', 'document', 'animation', 'photo', 'sticker', 'video', 'voice'
    ],
    chat_types=['group', 'supergroup', 'channel'],
)
def unsupported_chat(message):
    bot.reply_to(
        message,
        "To be honest, I feel a bit shy. Would you kindly continue our conversation in a private chat?"
    )

bot.polling()