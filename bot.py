import requests
from telebot import TeleBot
from bs4 import BeautifulSoup
from telegram_bot_pagination import InlineKeyboardPaginator
from os import getenv

bot = TeleBot(getenv("BOT_API_KEY"))
words = []


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Для начала введите слова " "чтобы его перевести")


@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я твой персональный русско-японский словать!"
        "Попробую рассказать тебе как тут все работает! "
        "Для начала, пришли мне слово, которое хочешь перевести, "
        "а остальное сделаю я! Ты можешь вводить слова на русском, "
        "ромадзи, хирагане или катакан!",
    )


@bot.message_handler(
    content_types=[
        "photo",
        "audio",
        "sticker",
        "video",
        "video_note",
        "voice",
        "location",
        "contact",
    ]
)
def incorrect_handle_text(message):
    bot.send_message(message.chat.id, "Увы, так переводить я пока не умею...")


@bot.callback_query_handler(func=lambda call: call.data.split("#")[0] == "character")
def characters_page_callback(call):
    page = int(call.data.split("#")[1])
    bot.delete_message(call.message.chat.id, call.message.message_id)
    send_page(call.message, words, page)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    payload = {"q": message.text, "pg": "0", "dic_yarxi": "1", "sw": "2560"}
    # print(f'Перевод для слова: {message.text}\n')

    site = "http://www.jardic.ru/search/search_r.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Safari/537.36"
    }

    page = requests.get(site, params=payload, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    result = soup.findAll("td", {"width": "65%"})
    pages = 10

    try:
        # for i in range(10):
        #     bot.send_message(message.chat.id, result[i].text)
        #     # print(f'Перевод: {result[i].text}')

        global words
        words = [result[_].text for _ in range(pages)]

        send_page(message, words)

    except IndexError:
        bot.send_message(message.chat.id, "Увы, больше ничего нет...")
        # print('Увы, больше ничего нет...\n')


def send_page(message, lst, page=1):
    paginator = InlineKeyboardPaginator(
        len(lst), current_page=page, data_pattern="character#{page}"
    )

    bot.send_message(
        message.chat.id,
        lst[page - 1],
        reply_markup=paginator.markup,
        parse_mode="Markdown",
    )


bot.polling(none_stop=True, interval=0)
