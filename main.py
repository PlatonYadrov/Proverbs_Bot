import requests
from bs4 import BeautifulSoup
# import lxml
from random import randint
import json

your_word_proverbs = []
dict_proverbs = dict()


def get_proverbs(bukva):
    global dict_proverbs
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0"
    }
    url = "https://ru.wikiquote.org/wiki/Русские_пословицы"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    letter = soup.find_all("h2")
    count = 0
    dict_proverbs = dict()
    for let in letter:
        key = "Пословицы и поговорки на " + let.text
        # print(key)
        proverbs = let.find_next().find_next().find_next().find_all()
        arr_proverbs = []
        for proverb in proverbs:
            if str(proverb)[1] == "l":
                arr_proverbs.append(proverb.text)
                # print(proverb.text)
                count += 1
        dict_proverbs[key] = arr_proverbs
        if let.text == "Я":
            # print(count)
            break
    try:
        bukva = bukva.upper()
        number = randint(0, len(dict_proverbs[f"Пословицы и поговорки на {bukva}"]))
        return dict_proverbs[f"Пословицы и поговорки на {bukva}"][number]
    except:
        pass
    return "Некорректный ввод"


def your_word_get_proverbs(your_word):
    global your_word_proverbs
    your_word_proverbs = []
    your_word = your_word[0].upper() + your_word[1:]
    your_word_more = your_word[0].lower() + your_word[1:]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                      " (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0"
    }
    url = "https://ru.wikiquote.org/wiki/Русские_пословицы"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    letter = soup.find_all("h2")
    count = 0
    dict_proverbs = dict()
    for let in letter:
        key = "Пословицы и поговорки на " + let.text
        proverbs = let.find_next().find_next().find_next().find_all()
        arr_proverbs = []
        for proverb in proverbs:
            if str(proverb)[1] == "l":
                if your_word in proverb.text or your_word_more in proverb.text:
                    your_word_proverbs.append(proverb.text)
                count += 1
        dict_proverbs[key] = arr_proverbs
        if let.text == "Я":
            break
    try:
        return your_word_proverbs
    except:
        pass
    return "Некорректный ввод"


def capi_picture():
    pictures_urls = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0"
    }
    urls = ["https://kartinkin.net/pics/29679-kapibara-oboi.html", "https://kartinkin.net/77968-kapibara-kartinki.html"]
    for url in urls:
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        cards = soup.find_all("div", class_="fotocontext")
        for card in cards:
            card = card.find("div", class_="otstupi")
            href = card.find("a")
            picture_url = href.get("href")
            pictures_urls.append(picture_url)

    rand_pictures = randint(0, len(pictures_urls))
    picture = pictures_urls[rand_pictures]

    p = requests.get(picture)
    out = open("capi.jpg", "wb")
    out.write(p.content)
    return out


def new_json(message, data):
    with open(f"{message}.json", "a", encoding="UTF-8-sig") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    return f"{message}.json"


def all_new_json():
    global dict_proverbs
    get_proverbs("и")
    with open("Все пословицы.json", "a", encoding="UTF-8-sig") as file:
        json.dump(dict_proverbs, file, indent=4, ensure_ascii=False)
    return "Все пословицы.json"


if __name__ == '__main__':
    # your_word = input()
    # print(your_word_get_proverbs(your_word))
    print(capi_picture())
