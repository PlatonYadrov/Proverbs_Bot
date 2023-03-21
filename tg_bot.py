import os
from time import sleep
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from config import token
from keyboard_letter import letter, buttons
from main import get_proverbs, your_word_get_proverbs, new_json, all_new_json, capi_picture

bot = Bot(token=token)
dp = Dispatcher(bot)

string = ""
f = ""
usernames = []
flag = 0


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    global usernames
    usernames.append(message["from"]["username"])
    b0 = KeyboardButton(text="Ввести букву, с которой начинается пословица")
    b1 = KeyboardButton(text="Ввести слово, которое есть в пословице")
    b2 = KeyboardButton(text="Все пословицы")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(b0).add(b1).add(b2)
    first_message = "Привет! Этот бот сделан для того, чтобы молодое поколение не забывало " \
                    "народные изречение, складывающиеся веками.\n" \
                    "Коротко об управлении:\n" \
                    "/start для перезапуска\n" \
                    "/chat_stats для просмотра статистики\n" \
                    "/capi для просмотра случайной фотографии капибары"
    await message.answer(first_message)

    await message.answer("Выберете действие", reply_markup=keyboard)


@dp.message_handler(commands=["chat_stats"])
async def chat_stats(message: types.Message):
    b0 = KeyboardButton(text="Ввести букву, с которой начинается пословица")
    b1 = KeyboardButton(text="Ввести слово, которое есть в пословице")
    b2 = KeyboardButton(text="Все пословицы")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(b0).add(b1).add(b2)
    info = message
    print(info)
    username = info["from"]["username"]
    first_name = info["from"]["first_name"]
    chat_id = info["chat"]["id"]
    typ = info["chat"]["type"]
    all_message = info["message_id"]
    language_code = info["from"]["language_code"]
    print_info = f"first_name: {first_name}\n" \
                 f"username: {username}\n" \
                 f"chat_id: {chat_id}\n" \
                 f"language_code: {language_code}\n" \
                 f"type: {typ}\n" \
                 f"all_message: {all_message}"
    await message.answer(print_info, reply_markup=keyboard)


@dp.message_handler(commands=["capi"])
async def capi(message: types.Message):
    capi_picture()
    photo = open('capi.jpg', 'rb')
    await message.answer("Фотографируем...")
    sleep(3)

    await bot.send_photo(chat_id=message.chat.id, photo=photo)


@dp.message_handler(Text(equals="Ввести букву, с которой начинается пословица"))
async def desired_letter(message: types.Message):
    # print(usernames)
    await message.answer("Нажмите на букву", reply_markup=buttons)


@dp.message_handler(Text(equals=letter))
async def desired_letter(message: types.Message):
    await message.answer(get_proverbs(message.text))


@dp.message_handler(Text(equals="<- Назад"))
async def back(message: types.Message):
    b0 = KeyboardButton(text="Ввести букву, с которой начинается пословица")
    b1 = KeyboardButton(text="Ввести слово, которое есть в пословице")
    b2 = KeyboardButton(text="Все пословицы")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(b0).add(b1).add(b2)
    await message.answer("Выберете действие", reply_markup=keyboard)


@dp.message_handler(Text(equals="Нет."))
async def back_no(message: types.Message):
    b0 = KeyboardButton(text="Ввести букву, с которой начинается пословица")
    b1 = KeyboardButton(text="Ввести слово, которое есть в пословице")
    b2 = KeyboardButton(text="Все пословицы")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(b0).add(b1).add(b2)
    await message.answer("Выберете действие", reply_markup=keyboard)


@dp.message_handler(Text(equals="Все пословицы"))
async def back_no(message: types.Message):
    b0 = KeyboardButton(text="Ввести букву, с которой начинается пословица")
    b1 = KeyboardButton(text="Ввести слово, которое есть в пословице")
    b2 = KeyboardButton(text="Все пословицы")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(b0).add(b1).add(b2)
    await message.answer("Подождите...", reply_markup=keyboard)

    f = all_new_json()
    await message.reply_document(open(f, 'rb'))
    os.remove(f)


@dp.message_handler(Text(equals="Ввести слово, которое есть в пословице"))
async def word(message: types.Message):
    global flag
    info = message
    all_message = info["message_id"]
    if all_message > 100000 and flag == 0:
        await message.answer("Вы уже набрали 0 сообщений в этом боте!")
        await message.answer("Продолжайте в том же духе. Для поднятия настроения...")
        capi_picture()
        photo = open('capi.jpg', 'rb')
        flag = 1

        await bot.send_photo(chat_id=message.chat.id, photo=photo)

    await message.answer("Введите слово")


@dp.message_handler()
async def your_word(message: types.Message):
    global string, f
    string = ""
    word = message.text
    b0 = KeyboardButton(text="Да ->")
    b1 = KeyboardButton(text="Нет.")
    b2 = KeyboardButton(text="<- Назад")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row(b0, b1, b2)
    if message.text != "Да ->" and message.text != "Нет." and message.text != "<- Назад":
        f = new_json(word, your_word_get_proverbs(message.text))
        if len(your_word_get_proverbs(message.text)) > 0:
            if len(your_word_get_proverbs(message.text)) > 100:
                await message.answer("Много пословиц, держи json")
                await message.reply_document(open(f, 'rb'))
                os.remove(f)
            else:
                for your in your_word_get_proverbs(message.text):
                    string += your + "\n"
                await message.answer(string)

                await message.answer("Хотите сохранить пословицы в файл?", reply_markup=keyboard)
        else:
            await message.answer("Ничего не найдено")
            os.remove(f)
    elif message.text == "Да ->":
        await message.reply_document(open(f, 'rb'))
        os.remove(f)
    elif message.text == "Нет.":
        back_no()
        os.remove(f)
    else:
        back()
        os.remove(f)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
