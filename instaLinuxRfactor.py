
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# telebot
import time
import telebot
from telebot import types
import os
import glob


# options
options = webdriver.ChromeOptions()

# user-agent
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")

# for ChromeDriver version 79.0.3945.16 or over
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_experimental_option("detach", True)
# headless mode
# options.add_argument("--headless")
options.headless = True

driver = webdriver.Chrome(
    executable_path="/home/insta_bot/chromedriver",
    options=options
)
# элементы бота
api = ''
bot = telebot.TeleBot(api)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,text='Hello!\nThe bot allows you to save videos from Instagram.',parse_mode="Markdown")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add(types.KeyboardButton('Send a videolink'))
    bot.send_message(message.chat.id, text=f'Lets get started, {message.from_user.first_name} send me a link', reply_markup=keyboard)

def parse_photo(message):
    try:
        driver.get("https://insta-save.net/")
        time.sleep(2)
        print('get request')
        input_photo_link =driver.find_element_by_id("link")
        name_url = message.text
        input_photo_link.send_keys(name_url)
        print('send link to input')
        time.sleep(2)
        driver.find_element_by_class_name("btn-download").click()
        print('downloading photo')
        time.sleep(2)
        photo_path = glob.glob('/home/insta_bot/*.jpg')
        downloaded_photo = photo_path[-1]
        print(downloaded_photo)
        photo_to_send = open(downloaded_photo, "rb")
        bot.send_photo(message.chat.id, photo_to_send, 'Done!')
        time.sleep(5)
        # photo_to_remove = f'{downloaded_photo}'
        # os.remove(photo_to_remove)
    except Exception as ex:
        print(ex)


@bot.message_handler(content_types=['text'])
def get_answer(message):
    if(message.text == 'Send a videolink'):
        msg = bot.send_message(message.chat.id,text='Type a videolink: ',parse_mode="Markdown", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, parse_photo)

bot.polling(none_stop=True)
