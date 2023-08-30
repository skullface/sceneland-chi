from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from bs4 import BeautifulSoup 
import json
import time
from datetime import datetime

url = 'https://www.radius-chicago.com/events'
options = FirefoxOptions()
options.add_argument('--headless')
browser = webdriver.Firefox(options=options)
browser.implicitly_wait(15)
browser.get(url)
load_more_button = browser.find_element('id', 'loadMoreEvents')
load_more_button.click()

soup = BeautifulSoup(browser.page_source, 'html.parser')
calendar = soup.find('div', class_='event_list')
shows = calendar.find_all('div', class_='entry')

all_shows_list = []

for show in shows:
  all_shows_data = {} 

  headliner = show.find('h3', class_='carousel_item_title_small')
  opener = show.find('h4', class_='supporting')
  if opener.text.strip() == '':
    all_shows_data['artist'] = [headliner.text.strip()]
  else:
    all_shows_data['artist'] = [headliner.text.strip()] + [opener.text.strip().replace(' | ', ', ')]

  link = headliner.find('a')
  all_shows_data['link'] = link.get('href')

  date = show.find('span', class_='date')
  date_text = date.text.strip()
  time = show.find('span', class_='time')
  time_text = time.text.strip()
  time_text = time_text.replace(' ', '').replace('Doors', '')
  time_text = ''.join(time_text.split())

  # Extract day, month, and year from date_text
  day_of_week, date_part = date_text.split(',', maxsplit=1)
  date_part = date_part.strip()
  date_part_cleaned = ' '.join(date_part.split())  # Remove extra spaces
  month, day, year = date_part_cleaned.split()
  
  # Convert month abbreviation to month number
  month_number = datetime.strptime(month, '%b').month

  # Construct the full date string
  full_date_text = f'{month} {day} {year}'

  # Parse the full_date_text and time_text into datetime objects
  parsed_date = datetime.strptime(full_date_text, '%b %d, %Y')
  parsed_time = datetime.strptime(time_text, '%I:%M%p').time()

  # Construct the desired output string
  parsed_datetime = f'{parsed_date:%Y-%m-%d}T{parsed_time:%H:%M:%S}'
  all_shows_data['date'] = parsed_datetime

  all_shows_data['venue'] = 'Radius'
  all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2) 
print(all_shows_json)
