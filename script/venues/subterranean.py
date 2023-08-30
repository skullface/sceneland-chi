import requests
from bs4 import BeautifulSoup 
import json
from datetime import datetime

url_base = 'https://www.subt.net/?twpage='
url_pages = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

def should_skip_artist(artist_text):
  excluded_keywords = ['Draggy', 'Reggae Gold', '606 Open Mic', 'Emo Nite', 'Dance Party', 'Cleva Cyphers', 'Nexus 6']
  return any(keyword in artist_text for keyword in excluded_keywords)

all_shows_list = []

for url_page in url_pages:
  url_concat = url_base + str(url_page)
  session = requests.Session()
  page = session.get(url_concat, headers={'User-Agent': 'Mozilla/5.0'})
  soup = BeautifulSoup(page.content, 'html.parser')
  calendar = soup.find('div', class_='flexdisplay--artistevents')
  shows = calendar.find_all('div', class_='flexmedia--artistevents')

  for show in shows:
    all_shows_data = {}
    artist = show.find('span', class_='artisteventsname')
    link = show.find_all('a')[1]
    link_to_ticketweb = show.find_all('a')[2]

    artist_text = artist.text.strip()
    if should_skip_artist(artist_text):
      continue
    all_shows_data['artist'] = [artist_text]

    date = show.find('span', class_='artisteventdate').text.strip()
    time = show.find('span', class_='artisteventshowtime').text.strip()
    parsed_date = datetime.strptime(date, '%a %B %d, %Y')
    parsed_time = datetime.strptime(time, '%I:%M %p').time()
    parsed_datetime = f'{parsed_date:%Y-%m-%d}T{parsed_time:%H:%M:%S}'
    all_shows_data['date'] = parsed_datetime

    if link_to_ticketweb.text.strip() == 'Sold Out!':
      all_shows_data['sold_out'] = True
    all_shows_data['link'] = link.get('href')
    all_shows_data['venue'] = 'Subterranean'
    
    all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2)
print(all_shows_json)
