from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from bs4 import BeautifulSoup 
import json
import time
from datetime import datetime
import re

url = 'https://www.unitedcenter.com/events/?&F_m=9'
options = FirefoxOptions()
options.add_argument('--headless')
browser = webdriver.Firefox(options=options)
browser.implicitly_wait(10)
browser.get(url)
time.sleep(5)

soup = BeautifulSoup(browser.page_source, 'html.parser')
container = soup.find('div', class_='eventsTheme')
calendar = container.find_all('ul', class_='itemList')[0]
shows = calendar.find_all('ul', class_='itemList')

all_shows_list = []

def should_skip_artist(artist_text):
  excluded_keywords = ['Chicago Blackhawks', 'Chicago Bulls', 'CANCELLED']
  return any(keyword in artist_text for keyword in excluded_keywords)

for show in shows:
  all_shows_data = {} 

  artist = show.find('a', class_='eventLink')
  artist_text = artist.text.strip()
  if should_skip_artist(artist_text):
    continue

  date_string = artist.get('name')
  date_pattern = r'(\d{1,2}/\d{1,2}/\d{4})'
  date_extracted = re.search(date_pattern, date_string).group(1)
  date = datetime.strptime(date_extracted, '%m/%d/%Y')
  
  time_element = show.find('span', class_='duration').text.strip()
  if time_element:
    all_shows_data['artist'] = [artist_text]

    time_element = time_element.replace('(', '').replace(')', '')
    time = datetime.strptime(time_element, '%I:%M %p').time()
    all_shows_data['date'] = date.strftime('%Y-%m-%d') + 'T' + str(time)

    all_shows_data['link'] = 'https://www.unitedcenter.com' + artist.get('href')

    all_shows_data['venue'] = 'United Center'
    all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2) 
print(all_shows_json)
