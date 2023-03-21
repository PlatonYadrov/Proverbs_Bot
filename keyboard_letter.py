from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

letter = ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К", "Л", "М", "Н",
          "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Э", "Ю", "Я"]
k = [KeyboardButton(text=letter[i]) for i in range(0, 28)]

buttons = ReplyKeyboardMarkup(resize_keyboard=True)

buttons.row(k[0], k[1], k[2], k[3], k[4]).add().row(k[5], k[6], k[7], k[8], k[9
    ]).add().row(k[10], k[11], k[12], k[13], k[14]).add().row(k[15], k[16], k[17],
    k[18], k[19]).add().row(k[20], k[21], k[22], k[23], k[24]).add().row(k[25], k[26], k[27]).add("<- Назад")
