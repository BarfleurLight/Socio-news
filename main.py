##!/usr/bin/python3
import asyncio
from bot_init import bot, dp, types
from aiogram import Bot

# from telegram.handlers import client, other, callback, fsm_add_database
from telegram.handlers import other, get_files

# client.register_handlers_client(dp)
# callback.register_callback_handlers(dp)
# fsm_add_database.register_handlers_fsm_add_database(dp)

get_files.register_handlers_get_file(dp)
other.register_handlers_other(dp)

from telegram.commands import client_commands


async def on_startup(bot: Bot):
    print("Start bot")
    await client_commands.set_all_commands(bot)


async def on_shutdown():
    print("Бот остановлен")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


