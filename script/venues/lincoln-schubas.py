import requests
from bs4 import BeautifulSoup 
import json
from datetime import datetime

session = requests.Session()
page = session.get('https://lh-st.com', headers={'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(page.content, 'html.parser')
calendar = soup.find('div', class_='tessera-card-deck')
shows = calendar.find_all('div', class_='tessera-show-card')

all_shows_list = []

for show in shows:
  all_shows_data = {} 

  headliners = show.find_all('h4', class_='card-title')
  openers = show.find('div', class_='tessera-additionalArtists')
  for headliner in headliners:
    headliner.text.strip()
  if openers:
    if openers.text.strip() == 'Guest':
      all_shows_data['artist'] = [headliner.text.strip()]
    else:
      all_shows_data['artist'] = [headliner.text.strip() + ', ' + openers.text.strip().replace(' + ', ', ')]
  else:
    all_shows_data['artist'] = [headliner.text.strip()]

  sold_out = show.find('div', class_='show-banner-tag')
  if sold_out:
    all_shows_data['sold_out'] = True

  link = show.find_all('a')[1]
  all_shows_data['link'] = link.get('href')

  date = show.find('span', class_='date').text.strip()
  current_date = datetime.now().date()
  year = current_date.year

  month, day = date.split()
  month_number = datetime.strptime(month, '%b').month

  if month_number < current_date.month:
    year = current_date.year + 1
  else:
    year = current_date.year

  date = date + ' ' + str(year)
  date = datetime.strptime(date, '%b %d %Y')

  time = show.find('div', class_='tessera-showTime').find('b').text.strip()
  time = datetime.strptime(time, '%I:%M%p').time()

  all_shows_data['date'] = str(date).split(' ', 1)[0] + 'T' + str(time)

  venue = show.find('span', class_='tessera-venue').text.strip()
  all_shows_data['venue'] = venue
  all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2) 
print(all_shows_json)
