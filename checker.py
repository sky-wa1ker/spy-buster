from tinydb import TinyDB, Query
import requests
import json


db = TinyDB('db.json')
nation = Query()
config = json.load(open('config.json'))
api_key = config['api_key']
min_score = config['min_score']
api_url = f"https://api.politicsandwar.com/graphql?api_key={api_key}"


unit_dict = {
    "Soldiers": "soldier_kills",
    "Tanks": "tank_kills",
    "Aircraft": "aircraft_kills",
    "Ships": "ship_kills",
    "Nukes": "nuke_kills",
    "Missiles": "missile_kills",
}

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


def find_spies(unit, count):
  potential_spies = []
  page_number = 1
  while True:
      response_data = get_data(page_number)
      page_data = response_data['data']['nations']['data']
      for live_spy in page_data:
          db_spy = db.search(nation.id == live_spy['id'])
          if db_spy:
            db_spy = db_spy[0]
            if (live_spy[unit_dict[unit]] - db_spy[unit_dict[unit]]) >= count:
              potential_spies.append(f'{live_spy["id"]} {live_spy["leader_name"]} of {live_spy["nation_name"]} has killed {(live_spy[unit_dict[unit]] - db_spy[unit_dict[unit]])} {unit} since we last checked.')
      if not page_data:
          break
      page_number += 1

      if not response_data['data']['nations']['paginatorInfo']['hasMorePages']:
          break
  return potential_spies