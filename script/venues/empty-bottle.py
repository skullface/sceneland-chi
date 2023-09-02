from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from bs4 import BeautifulSoup 
import json
import time
from datetime import datetime

url = 'https://www.emptybottle.com/'
options = FirefoxOptions()
options.add_argument('--headless')
browser = webdriver.Firefox(options=options)
browser.implicitly_wait(10)
browser.get(url)
time.sleep(5)

soup = BeautifulSoup(browser.page_source, 'html.parser')
calendar = soup.find('div', id='block-aa5a2a92d674c2124233')
shows = calendar.find_all('div', class_='eb-item')

all_shows_list = []

for show in shows:
  artists_list = []
  sold_out = False
  artists_elements = show.find('ul', class_='performing').find_all('li')
  
  for artist in artists_elements:
    if '*SOLD OUT*' in artist.text.strip():
      sold_out = True
    
    artist_text = artist.text.strip()
    
    if artist_text == 'FREE MONDAY w':
      continue

    if any(keyword in artist_text for keyword in ['DAY PASS', 'Empty Bottle Yoga', 'Hard Country Honky Tonk', 'Fantasy Brunch']):
      continue
    artists_list.append(artist_text.replace('*SOLD OUT* ', '').replace(' - ', ': '))

  if artists_list:
    all_shows_data = {}
    all_shows_data['artist'] = artists_list

    if sold_out:
      all_shows_data['sold_out'] = True

    link = show.find('a', class_='buy-button')
    all_shows_data['link'] = link.get('href')

    date = show.find('div', class_='date')
    time = show.find('div', class_='start-time')
    date = date.text.strip()
    
    current_date = datetime.now().date()
    year = current_date.year

    month, day = date.split(maxsplit=2)[1:3]
    month_number = datetime.strptime(month, '%B').month

    if month_number < current_date.month:
      year = current_date.year + 1
    else:
      year = current_date.year
      
    date = date + ', ' + str(year)
    date = datetime.strptime(date, '%a %B %d, %Y')
    time = datetime.strptime(time.text.strip(), '%I:%M%p').time()
    all_shows_data['date'] = str(date).split(' ', 1)[0] + 'T' + str(time)

    venue = show.find('a', class_='event-venue')
    if venue:
      all_shows_data['venue'] = venue.text.strip().replace('At: ', '')
    else:
      all_shows_data['venue'] = 'Empty Bottle'

    all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2) 
print(all_shows_json)
