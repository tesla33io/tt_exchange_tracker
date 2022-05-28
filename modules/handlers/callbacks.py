from aiogram import types
from aiogram.types import ParseMode
import requests

import datetime
import pytz

from modules.instances import dp, bot, user, scheduler
from modules import messages
from modules import keyboards as kb

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Mobile Safari/537.36',
    'Accept': 'application/json', 'X-CSRFToken': 'JuluEg8rcghoUFA8zDVCjrpnJMVYlNzSJDJEvTdTFBD0LeiZutsGbFCljY2WIFyn'
}


@dp.callback_query_handler(lambda query: query.data.startswith('lang') or query.data == 'ctrl_change_pair')
async def select_currency_pair(query: types.CallbackQuery):
    await query.answer()
    user_data = user[query.from_user.id]
    lang = query.data.split('_')[1]
    user_data['lang'] = lang if query.data.startswith('lang') else user_data['lang']
    user[query.from_user.id].commit()
    await query.message.edit_text(text=messages.select_currency_pair[user_data['lang']],
                                  reply_markup=kb.available_pairs_get())


@dp.callback_query_handler(lambda query: query.data.startswith('pair__') or query.data == 'ctrl_change_interval')
async def select_update_interval(query: types.CallbackQuery):
    await query.answer()
    user_data = user[query.from_user.id]
    pair = query.data.split('__')[1]
    user_data['currency_pair'] = pair if query.data.startswith('pair__') else user_data['currency_pair']
    user_data.commit()
    await query.message.edit_text(
        text=messages.select_up_interval[user_data['lang']].format(pair.replace("_", " - ").upper()),
        reply_markup=kb.update_interval,
        parse_mode=ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda query: query.data.startswith('ui'))
async def start_tracking(query: types.CallbackQuery):
    await query.answer()
    now = datetime.datetime.now(tz=pytz.timezone("Europe/Kiev"))
    interval = query.data.split('_')[1]
    user_data = user[query.from_user.id]
    user_data['up_interval'] = interval
    request = requests.get('https://coinpay.org.ua/api/v1/exchange_rate', headers=headers).json()
    rates = request['rates']
    price = [rate['price'] for rate in rates if rate['pair'] == user_data['currency_pair'].upper()][0]
    user_data['last_price'] = price
    msg = await query.message.edit_text(text=messages.tracking[user_data['lang']].format(
        state='🟢',
        pair=user_data['currency_pair'].replace('_', ' - ').upper(),
        price=price,
        last_update=f'{str(now.date()).replace("-", ".")} - {str(now.time()).split(".")[0]}'),
        reply_markup=kb.control(user_data['lang'], False),
        parse_mode=ParseMode.MARKDOWN)
    job = scheduler.add_job(tracker_update, 'interval', seconds=60 * int(user_data['up_interval']),
                            args=(msg, query.from_user.id,))
    user_data['tracking_job_id'] = job.id
    user_data.commit()


async def tracker_update(msg: types.Message, user_id):
    now = datetime.datetime.now(tz=pytz.timezone("Europe/Kiev"))
    user_data = user[user_id]
    request = requests.get('https://coinpay.org.ua/api/v1/exchange_rate', headers=headers).json()
    rates = request['rates']
    price = [rate['price'] for rate in rates if rate['pair'] == user_data['currency_pair'].upper()][0]
    await msg.edit_text(text=messages.tracking[user_data['lang']].format(
        state='🟢',
        pair=user_data['currency_pair'].replace('_', ' - ').upper(),
        price=price,
        last_update=f'{str(now.date()).replace("-", ".")} - {str(now.time()).split(".")[0]}'),
        reply_markup=kb.control(user_data['lang'], False),
        parse_mode=ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda query: query.data.startswith('ctrl_'))
async def tracking_control(query: types.CallbackQuery):
    await query.answer()
    now = datetime.datetime.now(tz=pytz.timezone("Europe/Kiev"))
    user_data = user[query.from_user.id]
    request = requests.get('https://coinpay.org.ua/api/v1/exchange_rate', headers=headers).json()
    rates = request['rates']
    price = [rate['price'] for rate in rates if rate['pair'] == user_data['currency_pair'].upper()][0]
    if query.data == 'ctrl_stop':
        scheduler.pause_job(user_data['tracking_job_id'])
        await query.message.edit_text(text=messages.tracking[user_data['lang']].format(
            state='🟥',
            pair=user_data['currency_pair'].replace('_', ' - ').upper(),
            price=price,
            last_update=f'{str(now.date()).replace("-", ".")} - {str(now.time()).split(".")[0]}'),
            reply_markup=kb.control(user_data['lang'], True),
            parse_mode=ParseMode.MARKDOWN)
    else:
        scheduler.resume_job(user_data['tracking_job_id'])
        await query.message.edit_text(text=messages.tracking[user_data['lang']].format(
            state='🟢',
            pair=user_data['currency_pair'].replace('_', ' - ').upper(),
            price=price,
            last_update=f'{str(now.date()).replace("-", ".")} - {str(now.time()).split(".")[0]}'),
            reply_markup=kb.control(user_data['lang'], False),
            parse_mode=ParseMode.MARKDOWN)
