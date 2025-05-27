import pytest
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope='function')
def browser():
    #Open browser
    	# Описываем опции запуска браузера
    chrome_options = Options()
    chrome_options.add_argument("start-maximized") # открываем на полный экран
    chrome_options.add_argument("--disable-infobars") # отключаем инфо сообщения
    chrome_options.add_argument("--disable-extensions") # отключаем расширения
    chrome_options.add_argument("--disable-search-engine-choice-screen") # отключаем выбор движка для поиска
    #chrome_options.add_argument("--headless") # спец. режим "без браузера"
	
		# устанавливаем webdriver в соответствии с версией используемого браузера
    service = Service()
    # запускаем браузер с указанными выше настройками
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver                            #позволяет вызывать driver из других мест программы
    driver.quit()

@pytest.fixture(scope='function')
def knockout():
    HEADER = {'Content-Type':'application/json', 'trainer_token':'8d914b60bbc02f7f30db5b5412313988'}
    pokemons = requests.get(url = 'https://api.pokemonbattle-stage.ru/v2/pokemons', params = {'trainer_id':2124})
    for pokemon in pokemons.json()['data']:
        if pokemon['status'] != 0:
            requests.post(url='https://api.pokemonbattle-stage.ru/v2/pokemons/knockout',
                          headers = HEADER, json={"pokemon_id":pokemon['id']})

