import datetime

from selenium import webdriver
import os
from bs4 import BeautifulSoup
import time
import pyautogui
import requests
from pydub import AudioSegment
import speech_recognition as sr
import re


def get_mp3_link(driver):
    while True:
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            audio = soup.find('audio')
            src = audio.attrs['src']
            return src
        except Exception as e:
            print('NO ATTRS SRC')
            reset_driver_to_get_mp3_link(driver)
            time.sleep(3)


def switch_frames(driver):
    driver.switch_to.default_content()
    frame = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(frame)


def reset_driver_to_get_mp3_link(driver):
    driver.delete_all_cookies()
    driver.refresh()
    time.sleep(2)
    print('Cookies deleted')
    driver.refresh()
    time.sleep(2)
    move_mouse()
    begin_verification()
    click_sound_icon()
    switch_frames(driver)


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
    pyautogui.moveTo(77, 531, 1, pyautogui.easeInBounce)
    pyautogui.moveTo(846, 506, 1, pyautogui.easeInBounce)
    pyautogui.moveTo(479, 200, 1, pyautogui.easeInBounce)
    pyautogui.moveTo(420, 818, 1, pyautogui.easeInBounce)


def refresh_cookies(driver):
    # old_cookie_split = old_cookies.split(';')
    driver_cookies = driver.get_cookies()
    new_cookie = ""
    for c in driver_cookies:
        new_cookie += '{0}={1}'.format(c['name'], c['value']) + '; '

    return new_cookie


def get_digits_from_page(driver):
    while True:
        # pyautogui.moveTo(601, 390, 2, pyautogui.easeInQuad)
        # pyautogui.click()
        mp3_link = get_mp3_link(driver)
        download_mp3(mp3_link, 'mp3audio')
        recognized_text = recognize_text_from_mp3('mp3audio')

        # print(recognized_text)
        recognized_text = recognized_text.replace('for', '4').replace('to', '2').replace('gate', '8')
        digits = re.findall(r'\d+', recognized_text)
        digits = "".join(digits)

        if len(digits) == 6:
            # print("Digits recognized successfully")
            return digits
        else:
            print("Wrong recognized digits, trying again...")
            if 'Zbyt wiele prób' in driver.page_source:
                driver.refresh()
                move_mouse()
                begin_verification()
                click_sound_icon()
                switch_frames(driver)
            flag = True
            while flag:
                btn = driver.find_element_by_class_name("geetest_refresh")
                is_btn_avl = btn.is_enabled() and btn.is_displayed()
                flag = not is_btn_avl
                time.sleep(0.8)

            # click button for new mp3
            pyautogui.moveTo(601, 390, 2, pyautogui.easeInQuad)
            pyautogui.click()
            pass


def init_driver():
    driver = webdriver.Chrome(executable_path=os.path.join(os.getcwd(), 'webDrivers', 'chromedriver.exe'))
    driver.get("https://allegro.pl/")
    time.sleep(2)
    driver.refresh()
    time.sleep(2)


def begin_verification():
    # Move to middle button to begin verification
    pyautogui.moveTo(452, 446, 1, pyautogui.easeInQuint)
    pyautogui.click()
    time.sleep(2)
    pyautogui.moveTo(173, 275, 2, pyautogui.easeInQuint)


def click_sound_icon():
    # Click sound icon
    pyautogui.moveTo(465, 571, 2, pyautogui.easeInQuint)
    pyautogui.click()
    time.sleep(2)


def start_process(driver):
    driver.refresh()
    time.sleep(1)

    # while True:
    #     time.sleep(2)
    #     pos = pyautogui.position()
    #     print(pyautogui.position())

    move_mouse()
    begin_verification()
    click_sound_icon()
    switch_frames(driver)


    # Get digits from sound file
    digits = get_digits_from_page(driver)

    # move to enter voice text
    pyautogui.moveTo(541, 500, 2, pyautogui.easeInQuad)
    pyautogui.click()
    pyautogui.write(digits, interval=0.3)
    # print('writing digits')

    # move and click OK
    pyautogui.moveTo(546, 568, 0.5, pyautogui.easeInQuad)
    pyautogui.click()
    # print('clicking ok and sleeping...')
    time.sleep(4)

# print('generating new cookies')
# new_cookies = refresh_cookies(driver)
# print('new cookies generated')
# driver.close()


# click middle verify button
# elem = driver.find_element_by_class_name('geetest_radar_tip_content')
# elem.click()

# soup = BeautifulSoup(driver.page_source, 'html.parser')
# iframe = soup.find('iframe')
# captcha_link = iframe.attrs['src']
# driver.get(captcha_link)
# driver.refresh()
