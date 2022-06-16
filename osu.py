import os
import requests
import json


client_id = os.environ['client_id']
client_secret = os.environ['auth_token']

API_URL = 'https://osu.ppy.sh/api/v2'
TOKEN_URL = 'https://osu.ppy.sh/oauth/token'


def get_mods(mods):
    if mods != []:
      return mods
    else:
      mods = 'No mod'
      return mods

def get_pp(pp):
    if pp != 'None':
      return pp
    else:
      pp = 'No pp'
      return pp

def check_passed(passed):
    if passed:
      passed = "Pass"
      return passed
    else:
      passed = "No Pass"
      return passed

def get_token():
    data = {
        'client_id': client_id,
        'client_secret':client_secret,
        'grant_type': 'client_credentials',
        'scope': 'public'
    }

    response = requests.post(TOKEN_URL, data=data)

    return response.json().get('access_token')

def check_user(user):
  
    token = get_token()

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(f'{API_URL}/users/{user}/', headers=headers)

    data = response.json()
  
    lu = user.lower()
  
    if data['username'].lower() == lu:
      check_user = True
      return check_user
    else:
      check_user = False
      return check_user

def get_osu_name(user):
  
    token = get_token()

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(f'{API_URL}/users/{user}/', headers=headers)

    data = response.json()
    
    osu_name = data['username'].lower()
  
    return osu_name

def get_user_id(user):
  
    token = get_token()

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(f'{API_URL}/users/{user}/', headers=headers)

    data = response.json()

    user = data['id']
  
    return user


def get_max_combo(beatmap):
    token = get_token()

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(f'{API_URL}/beatmaps/{beatmap}', headers=headers)

    data = response.json()

    return data['max_combo']

def data(user_id):
    data_response = []
  
    token = get_token()

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    params = {
        'limit': 1,
        'include_fails': 1
    }

    response = requests.get(f'{API_URL}/users/{user_id}/scores/recent', params=params, headers=headers)

    data = response.json()
  
    #Usuario
    avatar_url = data[0]['user']['avatar_url']
    username = data[0]['user']['username']
    country_code = data[0]['user']['country_code']

    #Estadisticas
    max_combo = data[0]['max_combo']
    beatmap_max_combo = get_max_combo(data[0]['beatmap']['id'])
    mode = data[0]['mode']
    mods = get_mods(data[0]['mods'])#sin mods es una lista vacia, fixear al hacer programa  
    pp = get_pp(str(data[0]['pp'])) #Ver de agregar una calculadora de pp max
    rank = data[0]['rank']
    score = str(("{:,}".format(data[0]['score'])))
    acc_result = str(('{:.2f}'.format(data[0]['accuracy'] * 100))) + '% acc'
    count_tree_hundred = data[0]['statistics']['count_300']
    count_hundred = data[0]['statistics']['count_100']
    count_fifty = data[0]['statistics']['count_50']
    count_misses = data[0]['statistics']['count_miss']

    #beatmap
    url = data[0]['beatmap']['url']
    title = data[0]['beatmapset']['title'] + ' ' + f"[{data[0]['beatmap']['version']}]"
    star_rating = str(data[0]['beatmap']['difficulty_rating'])
    cover = data[0]['beatmapset']['covers']['list']
    
    data_response = [
      avatar_url,
      username,
      country_code,
      max_combo, 
      beatmap_max_combo,
      mode,
      mods,
      pp,
      rank,
      score,
      acc_result,
      count_tree_hundred,
      count_hundred,
      count_fifty,
      count_misses,url,
      title,
      star_rating,
      cover]

    return data_response

