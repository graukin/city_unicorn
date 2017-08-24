#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import logging
import os
import sys

from telegram.parsemode import ParseMode
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from dbhelper import DBHelper
from geo import GeoZone,GeoPoint

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARN)
logger = logging.getLogger(__name__)

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
        logger.warn(msg_text[ndx+1:])
        db = DBHelper()
        res=db.get_names(msg_text[ndx+1:])
        bot.sendMessage(chat_id=update.message.chat_id, text=res)

def exact_command(bot, update):
    msg_text = update.message.text.strip()
    ndx = msg_text.find(' ')
    if ndx == -1:
        bot.sendMessage(chat_id=update.message.chat_id, text="exact WHAT?")
    else:
        logger.warn(msg_text[ndx+1:])
        db = DBHelper()
        res=db.get_exact_name(msg_text[ndx+1:])
        bot.sendMessage(chat_id=update.message.chat_id, text=res)
        arr=res.split(' ')
        print("lon=" + arr[-3] + ", lat=" + arr[-2])
        bot.sendLocation(chat_id=update.message.chat_id, longitude=float(arr[-3]), latitude=float(arr[-2]))

def bounds_command(bot, update):
    msg_text = update.message.text.strip()
    ndx = msg_text.find(' ')
    if ndx == -1:
        bot.sendMessage(chat_id=update.message.chat_id, text="incorrect")
    else:
        arr=msg_text[ndx+1:].split(' ')
        if len(arr) != 5:
            bot.sendMessage(chat_id=update.message.chat_id, text="incorrect: " + repr(length(arr)) + "parts")
        else:
            p1 = GeoPoint(float(arr[0]), float(arr[1]))
            p2 = GeoPoint(float(arr[2]), float(arr[3]))
            offset = int(arr[4])
            zone = GeoZone(p1, p2, offset)
            bot.sendLocation(chat_id=update.message.chat_id, longitude=zone.central.lon, latitude=zone.central.lat)

            db = DBHelper()
            res=db.get_zone(zone.bounds)
            bot.sendMessage(chat_id=update.message.chat_id, text=repr(zone.radius) + "\n" + res)

def help_command(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, 
                    text='<code>help</code> - print this message\n' +
                         '<code>hi</code> - bot will say something\n' +
                         '<code>grep</code> - search for smth in street name; case insensitive\n' +
                         '<code>exact</code> - search for exact street',
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
    dispatcher.add_handler(CommandHandler("exact", exact_command))
    dispatcher.add_handler(CommandHandler("bounds", bounds_command))

    dispatcher.add_error_handler(error)

    updater.idle()

