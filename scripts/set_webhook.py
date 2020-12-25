import os

import httpx
from loguru import logger

telegram_token = os.getenv("TELEGRAM_TOKEN")
bot_url = input("Please enter bot url: ")
set_webhook_url = (
    f"http://api.telegram.org/bot{telegram_token}/setWebhook?url={bot_url}"
)
r = httpx.get(set_webhook_url)

if r.json()["ok"]:
    logger.info("Webhook configured!")
else:
    logger.info("Error, this is telegram's response")
    logger.info(r.json())
