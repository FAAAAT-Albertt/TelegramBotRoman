import asyncio
import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from text import TRADE_CONDITIONS, TRADE_PAY, CALLBACK_MESSAGE, TRADE_INFO
from config import TOKEN, CONTACT_ID, DEV_ID
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


button1 = KeyboardButton("Информация о Trade with China")
button2 = KeyboardButton("Условия работы с Trade with China")
button3 = KeyboardButton("Бланк заказа в Trade with China")
button4 = KeyboardButton("Группа Trade with China VK")
button5 = KeyboardButton("Узнать актуальный курс")
button6 = KeyboardButton("Запросить обратную связь менеджера Trade with China")
but_admin = KeyboardButton("Назначить курс")
markup3 = ReplyKeyboardMarkup(resize_keyboard=True).add(button1).add(button2).add(button3).add(button4).add(button5).add(button6)
markup_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button1).add(button2).add(button3).add(button4).add(button5).add(button6).add(but_admin)

ib1 = InlineKeyboardButton(text='Excel форма', callback_data="xlsx")
ib2 = InlineKeyboardButton(text='Text форма', callback_data="blank")
ib3 = InlineKeyboardButton(text="VK", url="https://vk.com/tradewithchinaru")
ikb = InlineKeyboardMarkup(row_width=2).add(ib1, ib2)
ikb2 = InlineKeyboardMarkup(row_width=2).add(ib3)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if str(message.from_user.id) == CONTACT_ID:
        await message.answer(text="Добро пожаловать, Goody -> Не хулигань тут сильно!", reply_markup=markup_admin)
    else:
        await message.answer(text="Добро пожаловать в Trade with China, Ваш надежный партнер с Китаем 🇷🇺🇨🇳", reply_markup=markup3)
    await message.delete()

@dp.message_handler(text='Информация о Trade with China')
async def trade_info(message: types.Message):
    await message.answer(text=TRADE_INFO)

@dp.message_handler(text='Условия работы с Trade with China')
async def trade_cond(message: types.Message):
    await message.answer(text=TRADE_CONDITIONS)

@dp.message_handler(text='Бланк заказа в Trade with China')
async def trade_blank(message: types.Message):
    await message.answer(text=TRADE_PAY, reply_markup=ikb)

@dp.message_handler(text='Группа Trade with China VK')
async def trade_vk(message: types.Message):
    await message.answer(text="Trade with China Вконтакте ⬇️", reply_markup=ikb2)
@dp.message_handler(text='Узнать актуальный курс')
async def trade_price(message: types.Message):
    await message.answer(text=f"Актульный курс CNY/RUB -> {get_data()}")
    await message.delete()

@dp.message_handler(text='Запросить обратную связь менеджера Trade with China')
async def trade_goody(message: types.Message):
    await message.answer(text="Ваше обращение отправлено. В ближайшее время с Вами свяжется администратор Trade with China.")
    await message.delete()
    username = message.from_user.username
    await bot.send_message(chat_id=CONTACT_ID, text=f"@{username} <- запрос на обратную связь")


@dp.message_handler()
async def admin_panel(message: types.Message):
    if message.text == "Назначить курс":
        await message.answer(text="Назначь курс...")
    else:
        price = message.text
        #
        if (str(message.from_user.id) == CONTACT_ID) and ('0' in price or '1' in price or '2' in price or '3' in price or '4' in price or '5' in price or '6' in price or '7' in price or '8' in price or '9' in price or '.' in price) and (len(price) <= 5):
            with open('price.txt', "w+", encoding='utf-8') as file:
                file.write(price)


@dp.callback_query_handler()
async def callback_button(callback: types.CallbackQuery):
    if callback.data == "blank":
        return await callback.message.answer(text=CALLBACK_MESSAGE)
    elif callback.data == "xlsx":
        return await callback.message.answer_document(open('Blank_zakaza_TWC.xlsx', 'rb'))

def get_data():
    with open('price.txt', "r", encoding='utf-8') as file:
        price = file.read()

    return price

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
