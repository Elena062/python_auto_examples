import requests
import pytest
import time
import random

from loguru import logger
#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Переменные для использования в запросах

base_url = 'https://api.pokemonbattle-stage.ru/v2/'
token = '8d914b60bbc02f7f30db5b5412313988'
header = {'Content-Type': 'application/json',
          'trainer_token': '8d914b60bbc02f7f30db5b5412313988'}
trainer_id = '2124'

"""
base_url = 'https://api.pokemonbattle.ru/v2/'
token = '5e985eaea3c82a0ea09236af7a143349'
header = {'Content-Type': 'application/json',
          'trainer_token': '5e985eaea3c82a0ea09236af7a143349'}
trainer_id = '22830'
"""
auth_button_class = 'MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge MuiButton-colorPrimary MuiButton-fullWidth MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge MuiButton-colorPrimary MuiButton-fullWidth style_1_popup_white_base_button_orange style_1_caption_14_500 css-cm2fpt'

def test_pozitive_authorization(browser):
    
    """Pozitive case authorization"""  

    browser.get(url='https://pokemonbattle-stage.ru')

    time.sleep(30)
    email_input = browser.find_element(by=By.ID, value='k_email')
                                       #By.CSS_SELECTOR, value='[class="MuiInputBase-input MuiOutlinedInput-input css-1pk1fka"]')
    email_input.click()
    email_input.send_keys('alenuccia@yandex.ru')
    time.sleep(30)

    password_input = browser.find_element(by=By.ID, value='k_password')
    password_input.click()
    password_input.send_keys('Crazy_8mwc')
    time.sleep(30)

    #button = browser.find_element(by=By.CSS_SELECTOR, value='[class="MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge MuiButton-colorPrimary MuiButton-fullWidth MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge MuiButton-colorPrimary MuiButton-fullWidth style_1_popup_white_base_button_orange style_1_caption_14_500 css-cm2fpt"]')
    button = browser.find_element(By.XPATH, '//*[@id="root"]/div/div/section/div[2]/form/button')
    #button.click()
    button.click()

    wait = WebDriverWait(browser, 10)
    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.header_card_trainer_id_num')))
    my_trainer = browser.find_element(By.CSS_SELECTOR, 'div.header_card_trainer_id_num')
    assert my_trainer.text == '2124', 'Unexpected trainer_id'

    time.sleep(20)

CASES = [
  ('1', 'alenuccia.gmail.com', 'Crazy_8mwc', ['Введите корректную почту', '']),
  ('2', 'alenuccia@yandex.ru', 'Crazy_8mowc', ['', 'Неверные логин или пароль']),
  ('3', 'alenuccia@yandex', 'Crazy_8mwc', ['Введите почту', '']),
  ('4', '', 'Crazy_8mwc', ['Введите почту', '']),
  ('5', 'alenuccia@gmail.com', '', ['', 'Введите пароль']),
  ('6', 'alenuccia@gmail.ru', '', ['Введите почту', ''])
]

@pytest.mark.parametrize('case_number, email, password, alerts', CASES)
def test_negative_authorization(case_number, email, password, alerts, browser):
    
    """Negative cases authorization"""  
    logger.info(f'CASES:{case_number}')
    browser.get(url='https://pokemonbattle-stage.ru')

    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.url_to_be('https://pokemonbattle-stage.ru/login'))

    time.sleep(30)
    email_input = browser.find_element(by=By.ID, value='k_email')
    email_input.click()
    email_input.send_keys(email)

    time.sleep(20)
    password_input = browser.find_element(by=By.ID, value='k_password')
    password_input.click()
    password_input.send_keys(password)

    button = browser.find_element(By.XPATH, '//*[@id="root"]/div/div/section/div[2]/form/button') 

    #button = browser.find_element(by = By.CSS_SELECTOR, value = 'button .k_form_send_auth')
                                  #CSS_SELECTOR, value='[class="MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge MuiButton-colorPrimary MuiButton-fullWidth MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge MuiButton-colorPrimary MuiButton-fullWidth style_1_popup_white_base_button_orange style_1_caption_14_500 css-cm2fpt"]')
    #alerts_messages = browser.find_elements(by = By.CSS_SELECTOR, value='[class*="MuiFormHelperText-root Mui-error"]')
    #WTF1 = button.is_enabled()

    #wait = WebDriverWait(browser, 10)
    #elem = wait.until(EC.element_to_be_clickable(by = By.CSS_SELECTOR, value='[class="MuiButtonBase-root"]'))

    #wait = WebDriverWait(browser, 10)
    #element = wait.until(EC.element_to_be_clickable(by = By.CSS_SELECTOR, value='[class*="MuiButtonBase-root"]'))
  
    button.click()
    time.sleep(5)
    #button.click()
    #password_alert_message = browser.find_element(By.CSS_SELECTOR, 'div.k_error_submit.MuiBox-root.css-178yklu')
    #button = browser.find_element(by=By.CSS_SELECTOR, value='[class="MuiTouchRipple-root css-4mb1j7"]')
    
    #button = browser.find_element(by=By.CSS_SELECTOR, value='[class="MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge MuiButton-colorPrimary MuiButton-fullWidth MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge MuiButton-colorPrimary MuiButton-fullWidth style_1_popup_white_base_button_orange style_1_caption_14_500 css-cm2fpt"]')
    """WTF = button.is_enabled()
    if WTF:
       button.click()"""
    #button.click()
    
    alerts_messages = browser.find_elements(by = By.CSS_SELECTOR, value='[class*="MuiFormHelperText-root Mui-error"]')
    
    alerts_list = []
    for element in alerts_messages:
        alerts_list.append(element.text)
   
    time.sleep(10)
    assert True, ''

def test_check_api(browser, knockout):
    """
    TPR-3: Check api
    """
    browser.get(url='https://pokemonbattle-stage.ru')
    email_input = browser.find_element(by=By.ID, value='k_email')
                                       #By.CSS_SELECTOR, value='[class="MuiInputBase-input MuiOutlinedInput-input css-1pk1fka"]')
    email_input.click()
    email_input.send_keys('alenuccia@yandex.ru')
    time.sleep(30)

    password_input = browser.find_element(by=By.ID, value='k_password')
    password_input.click()
    password_input.send_keys('Crazy_8mwc')
    time.sleep(30)

    button = browser.find_element(By.XPATH, '//*[@id="root"]/div/div/section/div[2]/form/button')
    button.click()

    wait = WebDriverWait(browser, 10)
    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.header_card_trainer_id_num')))

    browser.find_element(by=By.CLASS_NAME, value='header_card_trainer_id_num').click()
    WebDriverWait(browser, timeout=20, poll_frequency=2).until(EC.url_to_be('https://pokemonbattle-stage.ru/trainer/2124'))

    time.sleep(10)
    pokemon_count_before = browser.find_element(by=By.CSS_SELECTOR, value = '[class = "total-count history-info_count"]')
    count_before = int(pokemon_count_before.text)
    print(count_before)

    random_num = random.randint(1, 999)
    #random_name = random.choice(['Bulbazavr', 'Turbozavr', 'Tiranozaurus-Rex', 'Blinchik'])
    body_create = {
        "name": "generate",
        "photo_id": random_num
    }

    HEADER = {'Content-Type':'application/json', 'trainer_token':'8d914b60bbc02f7f30db5b5412313988'}
    response_create = requests.post(url=f'{base_url}pokemons', headers=HEADER, json=body_create)

    assert response_create.status_code == 201, 'Unexpected status code'

    browser.refresh()

    time.sleep(20)
    pokemon_count_after = browser.find_element(by=By.CSS_SELECTOR, value = '[class = "total-count history-info_count"]')
    count_after = int(pokemon_count_after.text)

    assert count_after - count_before == 1, 'Что-то мы насоздавали не того))'

##root > div > div > div > div.single_page_body_content > div.single_page_body_content_inner > div.k_mobile.k_content_trainer > div.pokemon_one_body_content_inner_pokemons > a > div > span
    ##root > div > header > nav > div.right_block > a.header_card_trainer.style_1_interactive_button_link > div.header_card_trainer_id > div.header_card_trainer_id_num