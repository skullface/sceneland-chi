from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from bs4 import BeautifulSoup 
import json
import time
from datetime import datetime

url = 'https://www.msg.com/calendar?category=music,comedy&location=Chicago'
options = FirefoxOptions()
options.add_argument('--headless')
browser = webdriver.Firefox(options=options)
browser.implicitly_wait(10)
browser.get(url)
time.sleep(5)

soup = BeautifulSoup(browser.page_source, 'html.parser')
calendar = soup.find('ul', class_='rQ0EB')
shows = calendar.find_all('div', class_='_1dsyj')

all_shows_list = []

for show in shows:
  all_shows_data = {} 

  artist = show.find('h4', class_='_15kgw').text.strip()
  all_shows_data['artist'] = [artist]

  link = show.find_all('a')[1]
  all_shows_data['link'] = 'https://www.msg.com' + link.get('href')

  time = show.find('div', class_='_13Gu3').text.strip()
  if ',' in time:
    time_parts = time.split(', ')
    time_to_parse = time_parts[0]
  else:
    time_to_parse = time
  time = datetime.strptime(time_to_parse, '%I:%M %p').time()

  day = show.find('span', class_='_39Av2').text.strip()
  monthyear = show.find_all('span', class_='If5NT')[1].text.strip().replace("'", '')  
  day = datetime.strptime(day, '%d').day
  month, year = monthyear.split()
  month_number = datetime.strptime(month, '%b').month
  year = datetime.strptime(year, '%y').year
  date = f"{year:02d}-{month_number:02d}-{day:02d}"

  all_shows_data['date'] = date + 'T' + str(time)

  all_shows_data['venue'] = 'Chicago Theatre'
  all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2) 
print(all_shows_json)
