import requests
from bs4 import BeautifulSoup 
import json
from datetime import datetime

session = requests.Session()
page = session.get('https://concordmusichall.com/calendar/', headers={'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(page.content, 'html.parser')
calendar = soup.find('div', class_='calendar-write')
shows = calendar.find_all('article', class_='show')

all_shows_list = []

for show in shows:
  all_shows_data = {} 
  headliner = show.find('h1')
  opener = show.find('h2')
  if opener.text.strip() == '':
    all_shows_data['artist'] = [headliner.text.strip()]
  else:
    all_shows_data['artist'] = [headliner.text.strip()] + [opener.text.strip()]

  sold_out = show.find('div', class_='icon_sold-out')
  if sold_out:
    all_shows_data['sold_out'] = True

  link = show.find_all('a')[1]
  all_shows_data['link'] = link.get('href')
  
  date = show.find('p', class_='date').text.strip()
  time = show.find('p', class_='doors').text.strip()
  time = time.replace('Doors @ ', '')

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
  time = datetime.strptime(time, '%I:%M %p').time()
  all_shows_data['date'] = str(date).split(' ', 1)[0] + 'T' + str(time)

  all_shows_data['venue'] = 'Concord Music Hall'
  all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2) 
print(all_shows_json)
