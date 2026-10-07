import os
import asyncio
from telethon import TelegramClient

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
PHONE = os.environ["PHONE"]

GROUPS = os.environ.get("GROUP_IDS", "").split(",")
MESSAGE = os.environ.get("POST_TEXT", "")
INTERVAL_MINUTES = int(os.environ.get("INTERVAL_MINUTES", "10"))

SESSION = "/data/telegram"

client = TelegramClient(SESSION, API_ID, API_HASH)


async def post_to_groups():
    for group in GROUPS:
        group = group.strip()

        if not group:
            continue

        try:
            await client.send_message(group, MESSAGE)
            print(f"Gepostet in Gruppe {group}", flush=True)

        except Exception as e:
            print(f"Fehler in Gruppe {group}: {e}", flush=True)


async def main():
    await client.start(phone=PHONE)

    print("Telegram-Bot gestartet!", flush=True)

    await post_to_groups()

    while True:
        await asyncio.sleep(INTERVAL_MINUTES * 60)
        await post_to_groups()


asyncio.run(main())
