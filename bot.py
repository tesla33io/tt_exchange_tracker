import asyncio
import os

from aiogram.utils import executor
from aiogram import types

from modules.handlers.callbacks import dp
from modules.handlers.commands import dp
from modules.instances import dp, bot, scheduler, credentials


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(60, repeat, coro, loop)


async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()
    scheduler.remove_all_jobs()


async def start(dp):
    print('Start')
    scheduler.start()
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(start(dp))
