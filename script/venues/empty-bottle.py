from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from bs4 import BeautifulSoup 
import json
import time

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
    date = date.text.strip().replace('Mon ', '').replace('Tue ', '').replace('Wed ', '').replace('Thu ', '').replace('Fri ', '').replace('Sat ', '').replace('Sun ', '')
    date = date.replace('August ', '2023-08-').replace('September ', '2023-09-').replace('October ', '2023-10-').replace('November ', '2023-11-').replace('December ', '2023-12-').replace('January ', '2024-01-').replace('February ', '2024-02-').replace('March ', '2024-03-').replace('April ', '2024-04-').replace('May ', '2024-05-').replace('June ', '2024-06-').replace('July ', '2024-07-') + 'T20:00:00'
    all_shows_data['date'] = date.replace('-1T', '-01T').replace('-2T', '-02T').replace('-3T', '-03T').replace('-4T', '-04T').replace('-5T', '-05T').replace('-6T', '-06T').replace('-7T', '-07T').replace('-8T', '-08T').replace('-9T', '-09T')

    venue = show.find('a', class_='event-venue')
    if venue:
      all_shows_data['venue'] = venue.text.strip().replace('At: ', '')
    else:
      all_shows_data['venue'] = 'Empty Bottle'

    all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2) 
print(all_shows_json)
