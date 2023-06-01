# webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# сторонние бибилотеки
import time
import os
import glob

# элементы вэбрайвера
driver = webdriver.Chrome(ChromeDriverManager().install())
opts = Options()
opts.add_experimental_option("detach", True)

def parse_photo():
    try:
        driver.get("https://insta-save.net/")
        time.sleep(2)
        print('get request')
        input_photo_link =driver.find_element_by_id("link")
        name_url = "https://www.instagram.com/p/CnjGN6jOMW2/"
        input_photo_link.send_keys(name_url)
        print('send link to input')
        time.sleep(2)
        driver.find_element_by_class_name("btn-download").click()
        print('downloading photo')
        time.sleep(2)
        photo_path = glob.glob('/Users/aleksandramirnova/Downloads/*.jpg')
        downloaded_photo = photo_path[-1]
        print(downloaded_photo)
        # photo_to_send = open(downloaded_photo, "rb")
        time.sleep(5)
        photo_to_remove = f'{downloaded_photo}'
        os.remove(photo_to_remove)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

parse_photo()