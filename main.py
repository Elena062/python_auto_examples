import requests
import random

# Переменные для использования в запросах
base_url = 'https://api.pokemonbattle.ru/v2/'
token = '5e985eaea3c82a0ea09236af7a143349'
header = {'Content-Type': 'application/json',
          'trainer_token': '5e985eaea3c82a0ea09236af7a143349'}

# Вспомогательные переменные
random_number = random.randint(1, 999)
max_pokemons = 'Максимум 5 живых покемонов'
max_pokeballs = 'Максимум 3 привязанных покемона к покеболу'
opponent_id = 1

# Body запроса для создания покемона
body_create = {
   "name": "Bulbazavr",
    "photo_id": random_number
}

# Ищем противника для битвы - покемона в покеболе с атакой 1
def find_opponent(): 
    response = requests.get(url=f'{base_url}pokemons',params={'in_pokeball':1, 'attack':7}, headers=header)
    if 'Покемоны не найдены' in response.text:                      
        return '0'
    else:                                                           #Ищем среди найденных покемонов "не наших"
        for i in response.json()["data"]:
            if i["trainer_id"] != '22830':
                return i["id"]
        return '0'

# Находим своего покемона с максимальным уровнем атаки
def my_stronger_pokemon():
    response = requests.get(url=f'{base_url}pokemons',params={'trainer_id':'22830', 'status': 1, 'sort':'desc_attack'}, headers=header)
    print('В поисках сильнейшего', response.text)
    return response.json()["data"][0]["id"]

# Находим своего покемона с минимальным уровнем атаки
def my_weakest_pokemon():
    response = requests.get(url=f'{base_url}pokemons',params={'trainer_id':'22830', 'status': 1, 'sort':'asc_attack'}, headers=header)
    print(response.text)
    print('Слабое звено:', response.json()["data"][0]["id"])
    return response.json()["data"][0]["id"]

# Находим своего покемона в покеболе с минимальным уровнем атаки
def my_weakest_pokeball():
    response = requests.get(url=f'{base_url}pokemons',params={'trainer_id':'22830', 'status': 1, 'in_pokeball':'1', 'sort':'asc_attack'}, headers=header)
    print(response.text)
    print('Кандидат на выселение:', response.json()["data"][0]["id"])
    return response.json()["data"][0]["id"]


# Отправляем покемона в нокаут
def knockout(pokemon_id):
    response = requests.post(url=f'{base_url}pokemons/knockout', headers=header, json={"pokemon_id": pokemon_id})
    print(response.text)
    return()

# Выгоняем покемона из покебола
def exit_pokeball(pokemon_id):
    response = requests.put(url = f'{base_url}trainers/delete_pokeball', headers=header, json={"pokemon_id": pokemon_id})    
    print('WARNING',response.text)
    return()

# Ловим покемона в покебол. Если все три покебола заняты, выселяем самого слабого покемона из покебола

def add_pokeball(pokemon_id):
    response = requests.post(url = f'{base_url}trainers/add_pokeball', headers=header, json={"pokemon_id": pokemon_id})
    if max_pokeballs in response.text:
        third_wheel = my_weakest_pokeball()                                                  #Находим кандидата на выселение
        exit_pokeball(pokemon_id=third_wheel)
        response = requests.post(url = f'{base_url}trainers/add_pokeball', headers=header, json={"pokemon_id": pokemon_id})
        print(response.text)
    return()

# Проверка, в покеболе ли покемон
def in_pokeball(pokemon_id):
    response = requests.get(url=f'{base_url}pokemons', params={'pokemon_id':pokemon_id}, headers=header)
    return response.json()["data"][0]["in_pokeball"]


# Функция проведения битвы
def fight_battle(attacking_id, opponent_id):
    body_battle = {
    "attacking_pokemon": attacking_id,
    "defending_pokemon": opponent_id
    }
    if in_pokeball(attacking_id)==0:
        add_pokeball(pokemon_id = attacking_id)
    response = requests.post(url = f'{base_url}battle', headers = header, json = body_battle)
    print(response.text)
    return response.json()['result']

# Создаём покемона, если у тренера уже 5 живых покемонов, находим соперника/ов и сражаемся, пока не проиграем)
# если соперников нет, отправляем в нокаут слабого покемона, и после этого наконец-то создаем покемона

response = requests.post(url = f'{base_url}pokemons', headers = header, json = body_create)
if max_pokemons in response.text:
    result = 'Твой покемон победил'
    while result == 'Твой покемон победил':
        opponent_id = find_opponent()
        if opponent_id == '0': 
            weakest_pokemon = my_weakest_pokemon()
            knockout(pokemon_id = weakest_pokemon)
            break
        else:
            attacking_id = my_stronger_pokemon()
            result = fight_battle(attacking_id=attacking_id, opponent_id=opponent_id)
    response = requests.post(url = f'{base_url}pokemons', headers = header, json = body_create)

print('Создан новый покемон с id=', response.json()['id'])

# Body запроса на изменение покемона
body_rename = {
    "pokemon_id": response.json()['id'],
    "name": "Palevozavr",
    "photo_id": random_number
}

# Меняем имя и фото покемона
response_rename = requests.put(url = f'{base_url}pokemons', headers = header, json = body_rename)
print(response_rename.json())

# Ловим покемона в покебол
add_pokeball(pokemon_id=response.json()['id'])
