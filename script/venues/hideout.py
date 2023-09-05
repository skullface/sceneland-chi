import requests
from bs4 import BeautifulSoup 
import json
from datetime import datetime

# Load the page
session = requests.Session()
page = session.get('https://hideoutchicago.com', headers={'User-Agent': 'Mozilla/5.0'})

# Grab the container elements in the DOM
soup = BeautifulSoup(page.content, 'html.parser')
calendar = soup.find('div', class_='widgetGeneralView')
shows = calendar.find_all('div', class_='eventWrapper')

all_shows_list = []

for show in shows:
  all_shows_data = {} 

  headliner = show.find(id='eventTitle').text.strip().replace(' with Special Guests', '').replace(' with Special Guest', '')
  openers = show.find(id='evSubHead').text.strip()

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
  weekday, month, day, year = date.split()
  month_number = datetime.strptime(month, '%b').month
  date = datetime.strptime(date, '%a, %b %d, %Y')

  all_shows_data['date'] = str(date).split(' ', 1)[0] + 'T' + str(parsed_time)

  sold_out = show.find('span', class_='sold-out')
  if sold_out:
    all_shows_data['sold_out'] = True

  all_shows_data['venue'] = 'Hideout'
  all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2) 
print(all_shows_json)
