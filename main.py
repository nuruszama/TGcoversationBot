"""
Simple Bot to reply to Telegram messages taken from the python-telegram-bot examples.
Deployed using heroku.
"""

import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

import os
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

ECHO, END = range (2)
"""replace token with the token you got from bot father corresponding to your bot"""
TOKEN = 'token'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! I am Sweety, the cutest 🐈 in the world. Happy to meet you')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help! I am happy to assist you. Right now, I am still learning')

def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    context.bot.send_message(chat_id=context.job.context, 
                             text='beep!')

def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Sorry, we can not go back to past!')
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, due, context=chat_id, name=str(chat_id))

        text = 'Timer successfully set!'
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)

def end(update, context):
    update.message.reply_text(
      'Happy that you send me a message 😀 I cannot completely text you back. I am still learning')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def incoming(update, context):
    """give you a welcome message when you text the bot. after that echo of your message is send to you."""
    update.message.reply_text('Hi, you send me')

    return ECHO

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("set", set_timer))
    dp.add_handler(CommandHandler("unset", unset))
    """when /help or /start is tiggered, bot replies with what we defined with start or help respectively"""

    # on noncommand i.e message - welcome message or starting of coversation
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, incoming)],
        states={
                ECHO: [MessageHandler(Filters.text, echo)],
                },
        Fallbacks=[MessageHandler(Filters.text, end)],
        )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    """replace link with the link to your app"""
    updater.bot.setWebhook('link' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_webhook is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
