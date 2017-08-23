#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import logging
import os
import sys
import sqlite3

from telegram.parsemode import ParseMode
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARN)
logger = logging.getLogger(__name__)

conn = sqlite3.connect(r"info_extractor/streets_NizhNov.db")

def hi_command(bot, update):
    user = update.message.from_user
    name = user.first_name
    if name is None:
        name = user.username
    msg = name + ', I\'m here to serve'
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)

def grep_command(bot, update):
    msg_text = update.message.text.strip()
    ndx = msg_text.find(' ')
    if ndx == -1:
        bot.sendMessage(chat_id=update.message.chat_id, text="grep WHAT?")
    else:
        c = conn.cursor()
        res=""
        for row in c.execute("SELECT name FROM streets WHERE name LIKE '%" + msg_text[ndx:] + "%'"):
            res=res+row
        bot.sendMessage(chat_id=update.message.chat_id, text=res)

def help_command(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, 
                    text='<code>/hi</code> - bot will say something',
                    text='<code>/grep</code> - search for smth in street name; case insensitive; ^ and $ are not supported',
                    parse_mode=ParseMode.HTML)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

if __name__ == '__main__':
    TOKEN=os.environ['bot_token']
    PORT = int(os.environ.get('PORT', '5000'))
    updater = Updater(TOKEN)
    logger.info('wake up')
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.setWebhook("https://city-punic.herokuapp.com/" + TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hi", hi_command))
    dispatcher.add_handler(CommandHandler("grep", grep_command))

    dispatcher.add_error_handler(error)

    updater.idle()

