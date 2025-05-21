import requests
import pytest

# Переменные для использования в запросах
base_url = 'https://api.pokemonbattle.ru/v2/'
token = '5e985eaea3c82a0ea09236af7a143349'
header = {'Content-Type': 'application/json',
          'trainer_token': '5e985eaea3c82a0ea09236af7a143349'}
trainer_id = '22830'

def test_status_code_trainers():
    response = requests.get(url=f'{base_url}trainers', headers=header)
    assert response.status_code == 200

def test_my_trainer_name():
    response = requests.get(url=f'{base_url}trainers', params={'trainer_id':trainer_id}, headers=header)
    assert 'trainer_name' in response.text

@pytest.mark.parametrize('key, value', [('trainer_name', 'Crazy'), ('id', f'{trainer_id}')])
def test_parametrize(key, value):
    response_parametrize = requests.get(url=f'{base_url}trainers', params={'trainer_id': trainer_id})
    assert response_parametrize.json()['data'][0][key]==value
