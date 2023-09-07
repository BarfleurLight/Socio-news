from bot_init import bot, dp
from aiogram import types, filters, Bot, Dispatcher, F
from revork_file.counter.counter import Counter
from revork_file.revork.revork import RevorkFile
from pathlib import Path
import os

START_DIR = Path("revork_file/start/")
RESULT_DIR = Path("revork_file/result/")


async def get_image_photo(message: types.Message, bot: Bot):
    image = await bot.get_file(message.photo[-1].file_id)
    name = Counter().get_name()
    await bot.download_file(image.file_path, START_DIR/name)
    # Обработка объекта
    result = RevorkFile([name, None]).treatment()
    await message.reply_document(
        types.FSInputFile(RESULT_DIR/result)
    )
    os.remove(RESULT_DIR / result)


async def get_doc(message: types.Message, bot: Bot):
    image = await bot.get_file(message.document.file_id)
    doc_name = message.document.file_name
    name = Counter().get_name(doc_name)
    await bot.download_file(image.file_path, START_DIR/name)
    result = RevorkFile([name, doc_name]).treatment()
    if '_(Не поддерживается)' in str(result):
        os.remove(RESULT_DIR / result)
        return await message.answer('Данный тип файлов пока не поддерживается(')
    await message.reply_document(
            types.FSInputFile(RESULT_DIR/result)
        )
    os.remove(RESULT_DIR/result)


def register_handlers_get_file(dp: Dispatcher):
    dp.message.register(get_image_photo, F.photo)
    dp.message.register(get_doc, F.document)
