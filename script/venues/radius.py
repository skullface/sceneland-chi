from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from bs4 import BeautifulSoup 
import json
import time

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
  date = date.text.strip().replace('Aug ', '2023-08-').replace('Sep ', '2023-09-').replace('Oct ', '2023-10-').replace('Nov ', '2023-11-').replace('Dec ', '2023-12-').replace('Jan ', '2024-01-').replace('Feb ', '2024-02-').replace('Mar ', '2024-03-').replace('Apr ', '2024-04-').replace('May ', '2024-05-').replace('Jun ', '2024-06-').replace('Jul ', '2024-07-').replace('Mon, ', '').replace('Tue, ', '').replace('Wed, ', '').replace('Thu, ', '').replace('Fri, ', '').replace('Sat, ', '').replace('Sun, ', '').replace(', 2023', '').replace(', 2024', '') + 'T20:00:00'
  all_shows_data['date'] = date.replace('-1T', '-01T').replace('-2T', '-02T').replace('-3T', '-03T').replace('-4T', '-04T').replace('-5T', '-05T').replace('-6T', '-06T').replace('-7T', '-07T').replace('-8T', '-08T').replace('-9T', '-09T')

  all_shows_data['venue'] = 'Radius'
  all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2) 
print(all_shows_json)
