from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup
from aiogram import types

import requests

from modules.instances import dp

langs = InlineKeyboardMarkup()
langs.add(InlineKeyboardButton('🇬🇧 ENG', callback_data='lang_en'))
langs.add(InlineKeyboardButton('🇺🇦 UKR', callback_data='lang_ua'))


def available_pairs_get():
    """
    :return: keyboard
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Mobile Safari/537.36',
        'Accept': 'application/json', 'X-CSRFToken': 'JuluEg8rcghoUFA8zDVCjrpnJMVYlNzSJDJEvTdTFBD0LeiZutsGbFCljY2WIFyn'}
    request = requests.get('https://coinpay.org.ua/api/v1/pair', headers=headers).json()
    pairs = request['pairs']
    available_pairs = InlineKeyboardMarkup()
    for pair in pairs[:5]:
        available_pairs.add(InlineKeyboardButton(pair['name'].replace('_', ' - '), callback_data='pair__' + pair['name'].lower()))
    if len(pairs) > 5:
        available_pairs.add(
            InlineKeyboardButton('<<', callback_data='pairs_0'),
            InlineKeyboardButton('1/12', callback_data='none'),
            InlineKeyboardButton('>>', callback_data='pairs_5')
        )
    return available_pairs


@dp.callback_query_handler(lambda query: query.data.startswith('pairs'))
async def pagination_pairs(query: types.CallbackQuery):
    """
    :param query:
    :return: update message with available currency pairs
    """

    await query.answer()
    page = int(query.data.split('_')[1])
    available_pairs = InlineKeyboardMarkup()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Mobile Safari/537.36',
        'Accept': 'application/json', 'X-CSRFToken': 'JuluEg8rcghoUFA8zDVCjrpnJMVYlNzSJDJEvTdTFBD0LeiZutsGbFCljY2WIFyn'}
    request = requests.get('https://coinpay.org.ua/api/v1/pair', headers=headers).json()
    pairs = request['pairs']
    if page >= len(pairs):
        page = 0
    for pair in pairs[page:page + 5]:
        available_pairs.add(InlineKeyboardButton(pair['name'].replace('_', ' - '), callback_data='pair__' + pair['name'].lower()))
    available_pairs.add(
        InlineKeyboardButton('<<', callback_data=f'pairs_{"0" if page == 0 else page-5}'),
        InlineKeyboardButton(f'{int(page/5) + 1 if page > 0 else 1}/12', callback_data='none'),
        InlineKeyboardButton('>>', callback_data=f'pairs_{page+5}')
    )
    await query.message.edit_reply_markup(reply_markup=available_pairs)


update_interval = InlineKeyboardMarkup()
update_interval.add(InlineKeyboardButton('1', callback_data='ui_1'), InlineKeyboardButton('3', callback_data='ui_3'))
update_interval.add(InlineKeyboardButton('5', callback_data='ui_5'), InlineKeyboardButton('10', callback_data='ui_10'))


def control(lang, mode=False):
    """
    :param lang:
    :param mode: If False - stop tracking, if True - start tracking
    :return: keyboard
    """

    control_kb = InlineKeyboardMarkup()
    if not mode:
        control_kb.add(InlineKeyboardButton('🟥 Stop tracking' if lang == 'en' else '🟥 Зупинити відстежування', callback_data='ctrl_stop'))
        control_kb.add(InlineKeyboardButton('Change currency pair' if lang == 'en' else 'Змінити валютну пару', callback_data='ctrl_change_pair'))
        control_kb.add(InlineKeyboardButton('Change time interval' if lang == 'en' else 'Змінити часовий інтервал', callback_data='ctrl_change_interval'))
    else:
        control_kb.add(InlineKeyboardButton('🟢 Start tracking' if lang == 'en' else '🟢 Почати відстежування', callback_data='ctrl_start'))
        control_kb.add(InlineKeyboardButton('Change currency pair' if lang == 'en' else 'Змінити валютну пару', callback_data='ctrl_change_pair'))
        control_kb.add(InlineKeyboardButton('Change time interval' if lang == 'en' else 'Змінити часовий інтервал', callback_data='ctrl_change_interval'))
    return control_kb
