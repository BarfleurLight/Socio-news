from bot_init import bot, dp
from aiogram import types, filters, Bot, Dispatcher, F


async def get_image(message: types.Message, bot: Bot):
    image = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(image.file_path, 'revork_file/image/temp/test.jpg')



def register_handlers_get_file(dp: Dispatcher):
    dp.message.register(get_image, F.photo)
