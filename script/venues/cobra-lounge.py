import requests
from bs4 import BeautifulSoup
import json

headers = {
  'Accept-Encoding': 'gzip, deflate, sdch',
  'Accept-Language': 'en-US,en;q=0.8',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Referer': 'http://www.wikipedia.org/',
  'Connection': 'keep-alive',
}

params = (
  ('all_events', 'true'),
)

response = requests.get('https://api.dice.fm/venue_profiles/6663', headers=headers, params=params)
data = response.json()

all_shows_list = []

for show in data['sections'][0]['events']:
  all_shows_data = {} 
  all_shows_data['artist'] = [show['name'].replace(' / ', ', ').replace(' w/ ', ', ')]
  all_shows_data['link'] = show['social_links']['event_share']
  if show['status'] == "sold-out":
    all_shows_data['sold_out'] = True
  date = show['dates']['event_start_date']
  all_shows_data['date'] = date.split("-05:00", 1)[0].split("-06:00", 1)[0]
  all_shows_data['venue'] = show['venues'][0]['name']
  all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2) 
print(all_shows_json)
