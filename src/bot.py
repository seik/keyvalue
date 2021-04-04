import json
import os

import sentry_sdk
from loguru import logger
from sentry_sdk.integrations.serverless import serverless_function
from telegram import Bot, Update
from telegram.ext import CommandHandler, Dispatcher

from src import actions
from src.models import KeyValue

OK_RESPONSE = {
    "statusCode": 200,
    "body": json.dumps("ok"),
}
ERROR_RESPONSE = {"statusCode": 400, "body": json.dumps("Oops, something went wrong!")}

sentry_sdk.init(dsn=os.environ.get("SENTRY_DSN_URL"))


def configure_telegram():
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    if not telegram_token:
        logger.error("The TELEGRAM_TOKEN must be set")
        raise NotImplementedError

    return Bot(telegram_token)


def set_up_dispatcher(dispatcher: Dispatcher) -> None:
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("set", set_value))
    dispatcher.add_handler(CommandHandler("get", get_value))
    dispatcher.add_handler(CommandHandler("delete", delete_value))
    dispatcher.add_handler(CommandHandler("list", list_values))


bot = configure_telegram()
dispatcher = Dispatcher(bot, None, use_context=True)


@serverless_function
def handler(event, context: dict) -> dict:
    logger.info(f"Event: {event}")

    try:
        dispatcher.process_update(Update.de_json(json.loads(event.get("body")), bot))
    except Exception as e:
        logger.error(e)
        return ERROR_RESPONSE

    return OK_RESPONSE


def start(update: Update, context: dict) -> None:
    bot.send_message(chat_id=update.effective_chat.id, text="Biip boop, biip boop")


def set_value(update: Update, context: dict):
    message_text = " ".join(update.effective_message.text.split()[1:])

    # If reply to a message store that message text as value
    if update.effective_message.reply_to_message and len(message_text.split()) > 1:
        bot.sendMessage(
            update.message.chat_id, text="When replying to a message send only a key"
        )
        return
    elif update.effective_message.reply_to_message:
        message_text = (
            f"{message_text} {update.effective_message.reply_to_message.text}"
        )

    reply_message = actions.set_value(
        message_text=message_text,
        chat_id=str(update.effective_chat.id),
        user_id=str(update.effective_user.id),
    )

    bot.sendMessage(update.message.chat_id, text=reply_message, parse_mode="MarkdownV2")


def get_value(update: Update, context: dict):
    key_text = " ".join(update.effective_message.text.split()[1:])

    reply_message = actions.get_value(
        message_text=key_text,
        chat_id=str(update.effective_chat.id),
        user_id=str(update.effective_user.id),
    )

    bot.sendMessage(update.message.chat_id, text=reply_message)


def delete_value(update: Update, context: dict):
    key_text = " ".join(update.effective_message.text.split()[1:])

    reply_message = actions.delete_value(
        message_text=key_text,
        chat_id=str(update.effective_chat.id),
        user_id=str(update.effective_user.id),
    )

    bot.sendMessage(update.message.chat_id, text=reply_message, parse_mode="MarkdownV2")


def list_values(update: Update, context: dict):
    reply_message = actions.get_list(chat_id=str(update.message.chat_id))

    bot.sendMessage(update.effective_chat.id, text=reply_message)


set_up_dispatcher(dispatcher)

if not KeyValue.exists():
    KeyValue.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
