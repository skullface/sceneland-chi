import requests
from bs4 import BeautifulSoup 
import json
from datetime import datetime
import re

session = requests.Session()
page = session.get('https://metrochicago.com/events', headers={'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(page.content, 'html.parser')
calendar = soup.find('div', class_='generalView')
shows = calendar.find_all('div', class_='eventWrapper')

all_shows_list = []

for show in shows:
  all_shows_data = {} 

  headliner = show.find(id='eventTitle').text.strip()
  openers = show.find(id='evSubHead').text.strip().replace(' * ', ', ')

  if openers:
    all_shows_data['artist'] = [headliner + ', ' + openers]
  else:
    all_shows_data['artist'] = [headliner]

  link = show.find_all('a')[1]
  all_shows_data['link'] = link.get('href')

  time = show.find('div', class_='eventDoorStartDate').text.strip()

  def extract_time(input_string):
    sections = input_string.split('//')
    for section in sections:
      section = section.strip()
      if section.startswith("Show: "):
        return section[len("Show: "):].strip()

  time = extract_time(time)

  def parse_time(input_string):
    formats_to_try = ['%I:%M%p', '%I%p']
    for time_format in formats_to_try:
      try:
        return datetime.strptime(input_string, time_format).time()
      except ValueError:
        pass
      
  parsed_time = parse_time(time)

  date = show.find(id='eventDate').text.strip().replace('Sept', 'Sep')

  current_date = datetime.now().date()
  year = current_date.year

  weekday, month, day = date.split()
  month_number = datetime.strptime(month, '%b').month

  if month_number < current_date.month:
    year = current_date.year + 1
  else:
    year = current_date.year

  date = date + ' ' + str(year)
  date = datetime.strptime(date, '%a, %b %d %Y')

  all_shows_data['date'] = str(date).split(' ', 1)[0] + 'T' + str(parsed_time)

  sold_out = show.find('span', class_='sold-out')
  if sold_out:
    all_shows_data['sold_out'] = True

  venue = show.find('a', class_='venueLink').text.strip()
  all_shows_data['venue'] = venue
  all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2) 
print(all_shows_json)
