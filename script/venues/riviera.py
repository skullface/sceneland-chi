import requests
from bs4 import BeautifulSoup 
import json
from datetime import datetime
import re

session = requests.Session()
page = session.get('https://www.jamusa.com/venues/riviera-theatre', headers={'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(page.content, 'html.parser')
calendar = soup.find('div', class_='m-eventList')
shows = calendar.find_all('div', class_='eventItem')

all_shows_list = []

for show in shows:
  all_shows_data = {} 

  headliner = show.find('h3', class_='title')
  openers = show.find('h4', class_='tagline')

  if openers:
    all_shows_data['artist'] = [headliner.text.strip() + ', ' + openers.text.strip()]
  else:
    all_shows_data['artist'] = [headliner.text.strip()]

  link = show.find_all('a')[1]
  all_shows_data['link'] = link.get('href')

  time = show.find('div', class_='time').text.strip()
  def extract_time(input_string):
    sections = input_string.split('/')
    for section in sections:
      section = section.strip()
      if section.startswith('Show: '):
        return section[len('Show: '):].strip()
  time = extract_time(time)
  time = datetime.strptime(time, '%I:%M %p').time()
  
  date = show.find('div', class_='date').get('aria-label')
  if ' to ' in date:
    continue
  else:
    date = datetime.strptime(date, '%B %d %Y')

  all_shows_data['date'] = date.strftime('%Y-%m-%d') + 'T' + str(time)
  
  all_shows_data['venue'] = 'Riviera Theatre'
  all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2) 
print(all_shows_json)
