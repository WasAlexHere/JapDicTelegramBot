import telebot
import requests
from bs4 import BeautifulSoup
import re

token = ''
bot = telebot.TeleBot(token)

#upd = bot.get_updates()
#print(upd)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Для начала введите слова чтобы его перевести')

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Я твой персональный русско-японский словать! '
                                      'Попробую рассказать тебе как тут все работает! '
                                      'Для начала, пришли мне слово, которое хочешь перевести, а остальное сделаю я! '
                                      'Ты можешь вводить слова на русском, ромадзи, хирагане или катакан!')

@bot.message_handler(content_types=['photo','audio','sticker','video','video_note','voice','location','contact'])
def handle_text(message):
    bot.send_message(message.chat.id, "Увы, так переводить я пока не умею...")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    payload = {'q': message.text, 'pg': '0', 'dic_jardic': '1', 'sw': '1920'}

    print("Перевод для слова:",message.text,"\n")

    site = 'http://www.jardic.ru/search/search_r.php'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

    page = requests.get(site, params=payload, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    result_word = soup.findAll("span", {"style": "color: #7F0000;"})
    result_kanji = soup.findAll("span", {"style": "color: #00007F;"})
    result_trans = soup.findAll("span", {"style": "color: #000000;"})

    try:
        for i in range(10):
            bot.send_message(message.chat.id, result_word[i].text + '( ' + result_kanji[i].text + ' )' + ' : ' + re.sub(r'•', ' ',
                                                                                            result_trans[i].text))
            print("Перевод:", result_word[i].text + '( ' + result_kanji[i].text + ' )' + ' : ' + re.sub(r'•', ' ',
                                                                                            result_trans[i].text),'\n')
            i += 1
    except IndexError:
        bot.send_message(message.chat.id, "Увы, больше ничего нет...")
        print("Увы, больше ничего нет...","\n")

bot.polling(none_stop=True,interval=0)
