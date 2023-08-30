import requests
from bs4 import BeautifulSoup 
import json
from datetime import datetime

session = requests.Session()
page = session.get('https://www.beatkitchen.com/calendar', headers={'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(page.content, 'html.parser')
calendar = soup.find('div', class_='tw-plugin-calendar-list')
shows = calendar.find_all('div', class_='tw-cal-event')

def should_skip_artist(artist_text):
  excluded_keywords = ['Extraordinary Popular Delusions', 'Bluegrass Brunch', 'Chicago Underground Comedy', 'CANCELLED', 'Splice Series']
  return any(keyword in artist_text for keyword in excluded_keywords)

all_shows_list = []
current_date = datetime.now()

for show in shows:
  all_shows_data = {} 
  artist = show.find('div', class_='tw-name')
  artist_text = artist.text.strip()
  if should_skip_artist(artist_text):
    continue
  all_shows_data['artist'] = [artist_text]

  link = show.find_all('a')[1]
  all_shows_data['link'] = link.get('href'.split('?', 1)[0])

  sold_out = show.find('a', class_='tw_soldout')
  if sold_out:
    all_shows_data['sold_out'] = True

  date = show.find('span', class_='tw-event-date').text.strip()
  date = datetime.strptime(date, '%B %d, %Y')
  if date < current_date:
    continue
  time = show.find('span', class_='tw-event-time').text.strip()
  time = datetime.strptime(time, '%I:%M %p').time()
  all_shows_data['date'] = str(date).split(' ', 1)[0] + 'T' + str(time)

  all_shows_data['venue'] = 'Beat Kitchen'

  all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2, default=str) 
print(all_shows_json)
