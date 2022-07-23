from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import ForwardBot
from ForwardBot import Config

SCHEDULER = AsyncIOScheduler()


async def send_ping_message(chat_id=Config.PING_CHANNEL_ID):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    try:
      await ForwardBot.bot.send_message(chat_id=chat_id, text=f"msg_polling {current_time}")
    except BaseException as e:
        ForwardBot.LOGS.info(e)

SCHEDULER.add_job(send_ping_message, 'interval', minutes=30)
SCHEDULER.start()
