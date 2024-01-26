#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import sys
import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telebot.credentials import bot_token
from document.parser import load_document, parse_document, get_row
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


indexed_para = []

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

def is_not_blank(s):
    return bool(s and not s.isspace())

async def post_row(update: Update, row, line) -> None:
    await update.message.reply_text("Совпадение " +  str(line))

    for para in row.type:
        if is_not_blank(para):
            await update.message.reply_text(para)
    text = ''
    paragraphs=0
    for para in row.text:
        if is_not_blank(para):
            paragraphs=paragraphs+1
            text += para + '\n'
            if len(text)>2048:
                await update.message.reply_text(text)
                text = ''

    if is_not_blank(text):
        print(len(text))
        print(paragraphs)
        await update.message.reply_text(text)

    text = ''
    for para in row.justification:
        if is_not_blank(para):
            text += para + '\n'
    if is_not_blank(text):
        await update.message.reply_text(text + '\n\n\n')

async def parse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text.isnumeric():
        await update.message.reply_text("Вывод строки : " + update.message.text)
        row = get_row(int(update.message.text))
        await post_row(update, row, 1)
    else:
        await update.message.reply_text("Поиск: " + update.message.text)
        rows = parse_document(update.message.text)
        await update.message.reply_text("Найдено: " + str(len(rows)) + " совпадений")
        line = 1
        for row in rows:
            await post_row(update, row, line)
            line += 1

    await update.message.reply_text("Поиск закончен ")



def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot_token).build()

    # Load document in memory
    filename=sys.argv[1]
    print(filename)
    load_document(filename)

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e. message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, parse))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
