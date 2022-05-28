import asyncio
import os

from aiogram.utils import executor

from modules.handlers.callbacks import dp
from modules.handlers.commands import dp
from modules.instances import dp, bot, scheduler, credentials


WEBHOOK_HOST = 'https://ttecbot.herokuapp.com'
WEBHOOK_PATH = f'/{credentials["telegram"]["bot"]["token"]}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = '0.0.0.0'
print(os.getenv('PORT'))
WEBAPP_PORT = 8443


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(60, repeat, coro, loop)


async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()
    scheduler.remove_all_jobs()


async def start(dp):
    # asyncio.get_event_loop().stop()
    # await on_shutdown(dp)
    await bot.delete_webhook()

    # Close DB connection (if used)
    # await dp.storage.close()
    # await dp.storage.wait_closed()
    print('Bot started...')
    # scheduler.start()
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    print('webhook set')
    # executor.start_webhook(
    #     dispatcher=dp,
    #     webhook_path=WEBHOOK_PATH,
    #     skip_updates=True,
    #     host=WEBAPP_HOST,
    #     port=WEBAPP_PORT,
    # )
    # await dp.start_polling()


if __name__ == "__main__":
    scheduler.start()
    executor.set_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH
    )
    print('webhook set')
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
        on_startup=start
    )
    # asyncio.run(start())
    # loop = asyncio.get_event_loop()
    # executor.start_polling(dp, skip_updates=True, loop=loop)
