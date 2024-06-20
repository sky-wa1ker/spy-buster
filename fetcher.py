import requests
from tinydb import TinyDB
from datetime import datetime as dt
import json


db = TinyDB('db.json')
config = json.load(open('config.json'))
api_key = config['api_key']
min_score = config['min_score']
api_url = f"https://api.politicsandwar.com/graphql?api_key={api_key}"




def get_data(page_number):
    response = requests.post(api_url, json={"query":f"""
{{
  nations(min_score:{min_score}, vmode:false, first: 300, page:{page_number}){{
    paginatorInfo{{
      count
      currentPage
      firstItem
      hasMorePages
      lastItem
      total
      lastPage
    }}
    data{{
      id
      score
      nation_name
      leader_name
      last_active
      soldier_kills
      tank_kills
      aircraft_kills
      ship_kills
      nuke_kills
      missile_kills
    }}
  }}
}}
"""})
    return response.json()


all_data = []


def update_database():
  db.truncate()
  page_number = 1
  while True:
      response_data = get_data(page_number)
      page_data = response_data['data']['nations']['data']
      
      if not page_data:
          break

      all_data.extend(page_data)
      page_number += 1

      if not response_data['data']['nations']['paginatorInfo']['hasMorePages']:
          break
  db.insert_multiple(all_data)
  db.insert({"timestamp": dt.now().strftime("%d-%m-%Y %H:%M")})