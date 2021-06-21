"""Simple bot that can foward your messages to groups/channels and also replies to your message"""

import logging
from telegram import Update
from telegram.ext import (
    Updater, CommandHandler, ConversationHandler, MessageHandler,
    Filters, CallbackContext
    )
    
import os
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

"""replace token with the token you got from bot father corresponding to your bot"""
TOKEN = 'token'

TYPING_MESSAGE, TYPING_DESTINATION, GO = range(3)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

#Send a message when the command /start is issued.
def start(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "Hi! I'm tweety, a telegram bot")

#Send a message when the command /help is issued.
def help(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "Help! I can forward your text messages to your group \n"
        "\n"
        "Type or click /forward to use this feature")

def hi(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "Hey, How are you?")

def morning(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "Very Good Morning dear")

def night(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "Good Night")

def nice(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "Glad to hear that")

#Send a message when the command /forward is issued.
def forward(update, context) -> None:
    update.message.reply_text(
        "Give me the message you want to forward \n"
        "\n"
        "Type <Exit> to destroy forward command \n"
    )

    return TYPING_MESSAGE

#taking message to be forwarded as input
def fwd_msg(update, context) -> None:
    content = 'update.message.text'
    
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "Neat! Now tell me where to send this message \n"
        "\n"
        "Reply with chat id"
    )

    return TYPING_DESTINATION

#taking destination to which message is to be forwarded as input
def destination(update, context) -> None:
    destination = 'update.message.text'
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "I have recorded your message and chat id.\n\n"
        "Forwarding your message.....\n"
        "Done. Check forward destination"
    )

    return GO

#Sending the message to destination
def send(update, context) -> None:
    context.bot.send_message(chat_id=destination, text=content)

def exit(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "Destroyed entry to forward command\nuse /forward any time to use it again",
    )

    return ConversationHandler.END

#Log Errors caused by Updates.
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

#Start the bot.
def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(conv_handler)

    # procedure to forward messsage
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('forward', forward)],
        states={
            TYPING_MESSAGE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Exit$')),
                    fwd_msg,
                )
            ],
            TYPING_DESTINATION: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Exit$')),
                    destination,
                )
            ],
            GO: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Exit$')),
                    send,
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Exit$'), exit)],
    )

    dp.add_handler(conv_handler)
    
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text('^(hi|hello|hey|hola)$'), hi))
    dp.add_handler(MessageHandler(Filters.text('^(nice|well|awesome|cool)$'), nice))
    dp.add_handler(MessageHandler(Filters.text('^(mrng|morning)$'), morning))
    dp.add_handler(MessageHandler(Filters.text('^(night|good night|ni8|nyt)$'), night))

    
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
