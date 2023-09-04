import requests
from bs4 import BeautifulSoup 
import json
from datetime import datetime

# Load the page
session = requests.Session()
page = session.get('https://colesbarchicago.com/', headers={'User-Agent': 'Mozilla/5.0'})

# Grab the container elements in the DOM
soup = BeautifulSoup(page.content, 'html.parser')
calendar = soup.find('div', class_='upcomingWidget')
shows = calendar.find_all('div', class_='eventMainWrapper')

all_shows_list = []

for show in shows:
  all_shows_data = {} 

  artist = show.find(id='eventTitle').text.strip()
  all_shows_data['artist'] = [artist]

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
  time = datetime.strptime(time, '%I%p').time()

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

  all_shows_data['date'] = str(date).split(' ', 1)[0] + 'T' + str(time)

  all_shows_data['venue'] = 'Salt Shed'
  all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2) 
print(all_shows_json)
