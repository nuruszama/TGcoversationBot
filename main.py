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

TYPING_MESSAGE, TYPING_CHATID, SENDMSG = range(3)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

#Send a message when the command /start is issued.
def start(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "Hi {} ! I'm a telegram bot".format(user['first_name'])

#Send a message when the command /help is issued.
def help(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "Help! I can forward your text messages to your group \n"
        "\n"
        "Type or click /forward to use this feature")

#Replies with known telegram details
def about(update, context) -> None:
    user = update.message.from_user
    context.bot.send_message (chat_id = update.message.chat_id, text =
        "Username    : {}\nFirst Name  : {}\nLast Name  : {}\nUser Id         : {}"
        .format(user['username'], user['first_name'],user['last_name'], user['id']))

#To get the message id
def msg_id(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.message_id)

#To edit a message send by bot
def edit(update, context: CallbackContext) -> None:
    context.bot.editMessageText(chat_id=update.message.chat_id,
                                message_id=update.message.reply_to_message.message_id,
                                text="This message was edited")

#To delete messages with bot (bot should be admin to edit others messsage)
def delete_message(update, context):
    """deleting a message from the user message or self."""
    context.bot.delete_message(chat_id=update.message.chat_id,
                               message_id=update.message.reply_to_message.message_id
                               )

#pre-set natural responses without the usage of commands
def hi(update, context):
    user = update.message.from_user
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "Hey {}, How are you?".format(user['first_name']))
def morning(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "Very Good Morning dear")
def night(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "Good Night")
def here(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "I'm here..")
def nice(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "Glad to hear that")
def thanks_you_asked(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "Thank you so much for asking. I'm fine")

#Send a message when the command /forward is issued.
def forward(update, context) -> None:
    update.message.reply_text(
        "Give me the message you want to forward \n"
        "\n"
        "Type <Exit> to destroy forward command \n"
    )

    return TYPING_CHATID

#taking chat_id to which message is to be forwarded
def inputchatid(update: Update, context: CallbackContext):
    chatid = update.message.text
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "chat_id you gave me is [ " f"{chatid.lower()} ]. "
        "Now send me the message you want to forward"
    )

    return TYPING_MESSAGE

#taking message which is to be forwarded
def onetimemsg(update, context):
    msg = update.message.text
    chatid = context.inputchatid.chatid
    context.bot.send_message(chat_id=update.message.chat_id, text=
        "You said forward -  " f"{msg.lower()} to " f"{chatid.lower()}\n\n"
        "Forwarding your message.....\n"
        "Done. Check your forward destination"
    )

    return SENDMSG

#Sending the message to destination
def send(update, context):
    chatid = context.inputchatid.chatid
    msg = context.onetimemsg.msg
    context.bot.send_message(chat_id=inputchatid.id, text=onetimemsg.msg)

    return ConversationHandler.END

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
    dp.add_handler(CommandHandler("msg_id", msg_id))
    dp.add_handler(CommandHandler("about_me", about))
    dp.add_handler(CommandHandler("edit", edit))
    dp.add_handler(CommandHandler("delete", delete_message))
    dp.add_handler(conv_handler)

    # procedure to forward messsage
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('forward', forward)],
        states={
            TYPING_CHATID: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Exit$')),
                    inputchatid)
                ],
            TYPING_MESSAGE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Exit$')),
                    onetimemsg)
                ],
            SENDMSG: [
                MessageHandler(
                    Filters.text, send)
                ],
            },
        fallbacks=[MessageHandler(Filters.regex('^Exit$'), exit)]
    )

    dp.add_handler(conv_handler)
    
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.regex('^(hi|hello|hey|hola)$'), hi))
    dp.add_handler(MessageHandler(Filters.regex('^(fine|nice|well|awesome|cool)$'), nice))
    dp.add_handler(MessageHandler(Filters.regex('^(mrng|morning)$'), morning))
    dp.add_handler(MessageHandler(Filters.regex('^(night|good night|ni8|nyt)$'), night))
    dp.add_handler(MessageHandler(Filters.regex('How are you?'), thanks_you_asked))
    dp.add_handler(MessageHandler(Filters.regex('^(name|Name)$'), here))
    
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
