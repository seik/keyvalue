import json
import os

from loguru import logger
from telegram import (
    Update,
    Bot,
)
from telegram.ext import Dispatcher, CommandHandler

OK_RESPONSE = {
    "statusCode": 200,
    "body": json.dumps("ok"),
}
ERROR_RESPONSE = {"statusCode": 400, "body": json.dumps("Oops, something went wrong!")}


def configure_telegram():
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    if not telegram_token:
        logger.error("The TELEGRAM_TOKEN must be set")
        raise NotImplementedError

    return Bot(telegram_token)


def set_up_dispatcher(dispatcher: Dispatcher) -> None:
    dispatcher.add_handler(CommandHandler("start", start))


bot = configure_telegram()
dispatcher = Dispatcher(bot, None, use_context=True)


def handler(event, context) -> dict:
    logger.info(f"Event: {event}")

    try:
        dispatcher.process_update(Update.de_json(json.loads(event.get("body")), bot))
    except Exception as e:
        logger.error(e)
        return ERROR_RESPONSE

    return OK_RESPONSE


def start(update: Update, context: dict) -> None:
    text = "Hello world!"
    bot.send_message(chat_id=update.effective_chat.id, text=text)


set_up_dispatcher(dispatcher)
