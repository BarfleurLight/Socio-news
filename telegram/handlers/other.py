from bot_init import bot, dp
from aiogram import types, filters


async def get_start(message: types.Message):
    await message.answer('Привет я делаю ...')

async def echo_send(message: types.Message):
    await message.answer(message.text)


def register_handlers_other(dp):
    dp.message.register(get_start, filters.Command(commands=['start']))
    dp.message.register(echo_send)
