from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.message import ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import link
from pyrogram import Client, filters

import asyncio
import time
import pyrogram
import texts

bot = Bot(token="5963968316:AAE-rH0bfq-VkP8vTuk44MK3-VN8PDXKrxw")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
app = Client(name="testeraccnt", api_id=26257452, api_hash="9396fe0e9240f506013bf96c52a313d7")
app.start()

class Form(StatesGroup):
    config = State()
    
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton('Настроить'),)

topics = [
    ("Incidents", texts.incidents, 21),
    ("Digital", texts.digital, 23),
    ("Media Sphere", texts.media_sphere, 19),
    ("Culture", texts.culture, 17),
    ("SPG and Hydrogen", texts.spg_and_hydrogen, 15),
    ("Industry", texts.industry, 13),
    ("Politics", texts.politics, 3),
    ("Business", texts.business, 10)
]

def contains_word(message_text, words):
    for word in words:
        if word.lower() in message_text.lower():
            return True
    return False


@dp.message_handler(text="check")
async def check(message: types.Message):
    await message.answer("Бот запущен!")


@app.on_message(filters=filters.chat(-1001099350027))
async def forward_message_to_group(client, message):
    if any(word.lower() in message.text.lower() for word in texts.blacklist):
        return
    for topic_name, topic_words, reply_to_message_id in topics:
        if contains_word(message.text, topic_words):
            keyboard = InlineKeyboardMarkup(2)
            keyboard.add(InlineKeyboardButton(text='К сообщению…', callback_data='link', url=f"https://t.me/rusbrief/{message.id}"), 
                      InlineKeyboardButton(text='🗑️', callback_data='trash'))
            await bot.send_message(-1001826083519, message.text, reply_to_message_id=reply_to_message_id, parse_mode='markdown', disable_web_page_preview = True, reply_markup=keyboard)
            break


@dp.callback_query_handler(text = 'trash')
async def trash(callback: types.CallbackQuery):
    await callback.message.delete()

# @dp.message_handler(text="lgf")
# async def lgf(message: types.Message):
#     markup = InlineKeyboardMarkup(1)
#     markup.add(InlineKeyboardButton(text='Добавить ключ. слова', callback_data='config'),
#                InlineKeyboardButton(text='Отмена', callback_data='cancel'))
#     await message.answer("Здесь можно настроить бота", reply_markup=markup)


# configbutton = ReplyKeyboardMarkup(resize_keyboard=True)
# configbutton.add(KeyboardButton('Настроить'), KeyboardButton('Отмена'))


# @dp.callback_query_handler(text = 'config')
# async def config(callback: types.CallbackQuery):
#     await callback.message.answer("Меню настроек")


executor.start_polling(dp, skip_updates=False)