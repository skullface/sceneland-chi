from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from bs4 import BeautifulSoup 
import json
import time
from datetime import datetime

url = 'https://www.saltshedchicago.com/home#shows'
options = FirefoxOptions()
options.add_argument('--headless')
browser = webdriver.Firefox(options=options)
browser.implicitly_wait(15)
browser.get(url)
time.sleep(5)

soup = BeautifulSoup(browser.page_source, 'html.parser')
calendar = soup.find(id='block-yui_3_17_2_1_1668130854399_25742')
shows = calendar.find_all('div', class_='eb-item')

all_shows_list = []

def should_skip_artist(artist_text):
  excluded_keywords = ['Show Pack', 'SHOW PACK']
  return any(keyword in artist_text for keyword in excluded_keywords)

for show in shows:
  all_shows_data = {} 

  artist = show.find('div', class_='title').text.strip()
  
  if 'SOLD OUT - ' in artist:
    all_shows_data['sold_out'] = True

  if should_skip_artist(artist):
    continue
  all_shows_data['artist'] = [artist.replace('SOLD OUT - ', '').replace(' - ', ': ')]

  date = show.find('div', class_='date').text.strip()
  time = show.find('div', class_='start-time').text.strip()
  time = time.replace('Doors: ', '')

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
  time = datetime.strptime(time, '%I:%M%p').time()
  all_shows_data['date'] = str(date).split(' ', 1)[0] + 'T' + str(time)

  all_shows_data['venue'] = 'Salt Shed'
  all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2) 
print(all_shows_json)
