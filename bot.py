import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

GROUP_IDS = os.environ.get("GROUP_IDS", "").split(",")
MESSAGE = os.environ.get("POST_TEXT", "")
INTERVAL_MINUTES = int(os.environ.get("INTERVAL_MINUTES", "10"))

SESSION_STRING = os.environ["SESSION_STRING"]

client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH
)


async def post_to_groups():
    dialogs = await client.get_dialogs()

    groups = {}

    for dialog in dialogs:
        if dialog.is_group:
            groups[str(dialog.id)] = dialog.entity

    for group_id in GROUP_IDS:
        group_id = group_id.strip()

        if not group_id:
            continue

        try:
            if group_id not in groups:
                print(f"Gruppe nicht gefunden: {group_id}", flush=True)
                continue

            await client.send_message(groups[group_id], MESSAGE)

            print(f"Gepostet in Gruppe {group_id}", flush=True)

        except Exception as e:
            print(f"Fehler in Gruppe {group_id}: {e}", flush=True)


async def main():
    await client.start()

    print("Telegram-Bot gestartet!", flush=True)

    await post_to_groups()

    while True:
        await asyncio.sleep(INTERVAL_MINUTES * 60)
        await post_to_groups()


asyncio.run(main())
