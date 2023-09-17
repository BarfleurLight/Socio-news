import os

from aiogram import Bot, types, Dispatcher
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('token'))
dp = Dispatcher()
