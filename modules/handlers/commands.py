from aiogram import types

from modules.instances import dp, user, user_template
from modules import messages
from modules import keyboards as kb


@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    user[message.from_user.id] = user_template
    msg = await message.answer(messages.greeting, reply_markup=kb.langs)
    user[message.from_user.id]['message_id'] = msg.message_id
    user[message.from_user.id].commit()
