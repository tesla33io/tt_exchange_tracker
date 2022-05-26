import asyncio

from aiogram.utils import executor

from modules.handlers.callbacks import dp
from modules.handlers.commands import dp
from modules.instances import dp, scheduler


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(60, repeat, coro, loop)


async def start():
    print('Bot started...')
    scheduler.start()
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(start())
    # loop = asyncio.get_event_loop()
    # executor.start_polling(dp, skip_updates=True, loop=loop)
