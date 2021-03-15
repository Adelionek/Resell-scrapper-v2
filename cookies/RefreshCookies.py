from selenium import webdriver
import os
from bs4 import BeautifulSoup
import time
import pyautogui
import requests
from pydub import AudioSegment
import speech_recognition as sr
import random
import re


def get_mp3_link(driver):
    # elem_music = driver.find_element_by_class_name('geetest_music')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    audio = soup.find('audio')
    return audio.attrs['src']


def recognize_text_from_mp3(file_name):
    src = "./{0}{1}".format(file_name, '.mp3')
    sound = AudioSegment.from_mp3(src)
    sound.export("./audio_wav.wav", format="wav")
    file_audio = sr.AudioFile("./audio_wav.wav")
    r = sr.Recognizer()

    with file_audio as source:
        audio_text = r.record(source)
        return r.recognize_google(audio_text)


def download_mp3(link, file_name):
    r = requests.get(link)
    with open('./' + file_name + '.mp3', 'wb') as filetowrite:
        filetowrite.write(r.content)
    # print('./' + file_name + '.mp3' + 'file saved')


def move_mouse():
    pyautogui.moveTo(965, 199, 3, pyautogui.easeInBounce)
    pyautogui.moveTo(1000, 1500, 2.5, pyautogui.easeInBounce)
    pyautogui.moveTo(100, 614, 2, pyautogui.easeInBounce)
    # pyautogui.moveTo(2000, 650, 3, pyautogui.easeInBounce)


def refresh_cookies(driver):
    # old_cookies = '_cmuid=ya2w2emp-eqeg-5gtr-qqyh-sdd2g1e803ns; cartUserId=ya2w2emp-eqeg-5gtr-qqyh-sdd2g1e803ns; _gcl_au=1.1.290244876.1615451823; _gid=GA1.2.982670149.1615451824; gdpr_permission_given=1; __gfp_64b=_TfK6Fsw6K1sYyDvp49C79fUpGdanuU.Zm1US_z7ivr.x7|1614090830; __gads=ID=7104603301891fce:T=1615476860:S=ALNI_MbHTZ0dDy2FDlY3x0M6uqzbkpdLgQ; _ga=GA1.1.408306465.1615451824; datadome=48XXTAx7aH_mqqd-D~cy-HhChpU5sZd1i~1xv7imK3SLxZfuoyTokc7Bnqkygab~Q4lC~I0SsC7H_wNUeZDBFIXchV8kucNUM1dzAWxjHM; _ga_2FTJ836HTM=GS1.1.1615488078.268.0.1615488122.16'
    # old_cookie_split = old_cookies.split(';')
    driver_cookies = driver.get_cookies()
    new_cookie = ""
    for c in driver_cookies:
        new_cookie += '{0}={1}'.format(c['name'], c['value']) + '; '

    return new_cookie


def get_digits_from_page(driver):
    mp3_link = get_mp3_link(driver)
    download_mp3(mp3_link, 'mp3audio')
    recognized_text = recognize_text_from_mp3('mp3audio')
    print(recognized_text)
    recognized_text = recognized_text.replace('for', '4').replace('to', '2').replace('gate', '8')
    digits = re.findall(r'\d+', recognized_text)
    digits = "".join(digits)
    print(digits)

    if len(digits) == 6:
        print("Digits recognized successfully")
        return digits
    else:
        print("Wrong recognized digits, trying again...")
        pyautogui.moveTo(1332, 758, 2, pyautogui.easeInQuad)
        pyautogui.click()
        time.sleep(9)
        get_digits_from_page(driver)

def start_process():

    driver = webdriver.Chrome(executable_path=os.path.join(os.getcwd(), 'webDrivers', 'chromedriver.exe'))
    driver.get("https://allegro.pl/")
    time.sleep(2)
    driver.refresh()
    time.sleep(2)

    move_mouse()

    # click middle verify button
    # elem = driver.find_element_by_class_name('geetest_radar_tip_content')
    # elem.click()
    pyautogui.moveTo(919, 894, 2, pyautogui.easeInQuint)
    pyautogui.click()
    time.sleep(3)

    move_mouse()

    # click sound icon
    # elem_voice = driver.find_element_by_class_name('geetest_voice')
    # elem_voice.click()
    pyautogui.moveTo(1032, 1140, 2, pyautogui.easeInQuint)
    pyautogui.click()
    time.sleep(2)

    driver.switch_to.default_content()
    frame = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(frame)

    digits = get_digits_from_page(driver)
    time.sleep(3)

    # move to enter voice text
    pyautogui.moveTo(1213, 996, 2, pyautogui.easeInQuad)
    pyautogui.click()

    pyautogui.write(digits, interval=0.5)
    print('writing digits')

    # move and click OK
    pyautogui.moveTo(1219, 1127, 2, pyautogui.easeInQuad)
    pyautogui.click()
    print('clicking ok and sleeping...')
    time.sleep(5)

    print('generating new cookies')
    new_cookies = refresh_cookies(driver)
    print('new cookies generated')
    driver.close()
    return new_cookies


# soup = BeautifulSoup(driver.page_source, 'html.parser')
# iframe = soup.find('iframe')
# captcha_link = iframe.attrs['src']
# driver.get(captcha_link)
# driver.refresh()
