from bot_init import bot, dp
from aiogram import types, filters, Bot, Dispatcher, F
import os, time
from revork_file.counter.counter import Counter
from revork_file.revork.revork import RevorkFile


async def get_image_photo(message: types.Message, bot: Bot):
    image = await bot.get_file(message.photo[-1].file_id)
    name = str(time.strftime("%Y%m%d", time.localtime())) +\
        Counter().get_count_image() + '.jpg'
    await bot.download_file(image.file_path, f'revork_file/start/{name}')
    # Обработка объекта
    # await message.reply_document(types.FSInputFile(f'revork_file/start/{name}'))


async def get_image_doc(message: types.Message, bot: Bot):
    image = await bot.get_file(message.document.file_id)
    doc_name = message.document.file_name.split('.')
    name = str(time.strftime("%Y%m%d", time.localtime())) +\
        Counter().get_count_doc() + '.' +\
        doc_name[1]
    await bot.download_file(image.file_path, f'revork_file/start/{name}')
    RevorkFile(name).treatment()
    await message.reply_document(types.FSInputFile(f'revork_file/result/{name}'))



def register_handlers_get_file(dp: Dispatcher):
    dp.message.register(get_image_photo, F.photo)
    dp.message.register(get_image_doc, F.document)
