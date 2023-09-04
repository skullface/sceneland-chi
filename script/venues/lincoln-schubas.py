from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from bs4 import BeautifulSoup 
import json
import time
from datetime import datetime

url = 'https://lh-st.com'
options = FirefoxOptions()
options.add_argument('--headless')
browser = webdriver.Firefox(options=options)
browser.implicitly_wait(10)
browser.get(url)
time.sleep(5)

soup = BeautifulSoup(browser.page_source, 'html.parser')
calendar = soup.find('div', class_='tessera-card-deck')
shows = calendar.find_all('div', class_='tessera-show-card')

all_shows_list = []

for show in shows:
  all_shows_data = {} 

  headliners = show.find_all('h4', class_='card-title')
  openers = show.find('div', class_='tessera-additionalArtists')
  artists_list = []

  for headliner in headliners:
    headliner = headliner.text.strip()
    if 'Open Mic' in headliner:
      continue
    if openers and openers.text.strip() != 'Guest':
      opener = openers.text.strip().replace(' + ', ', ')
      artists_list.append(f"{headliner}, {opener}")
      all_shows_data['artist'] = artists_list
    else:
      artists_list.append(headliner)
      all_shows_data['artist'] = artists_list

  sold_out = show.find('a', class_='sold-out-button')
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
