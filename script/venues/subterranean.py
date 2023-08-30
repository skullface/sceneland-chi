import requests
from bs4 import BeautifulSoup 
import json

url_base = 'https://www.subt.net/?twpage='
url_pages = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

def should_skip_artist(artist_text):
  excluded_keywords = ['Draggy', 'Reggae Gold', '606 Open Mic', 'Emo Nite', 'Dance Party', 'Cleva Cyphers', 'Nexus 6']
  return any(keyword in artist_text for keyword in excluded_keywords)

all_shows_list = []

for url_page in url_pages:
  url_concat = url_base + str(url_page)
  session = requests.Session()
  page = session.get(url_concat, headers={'User-Agent': 'Mozilla/5.0'})
  soup = BeautifulSoup(page.content, 'html.parser')
  calendar = soup.find('div', class_='flexdisplay--artistevents')
  shows = calendar.find_all('div', class_='flexmedia--artistevents')

  for show in shows:
    all_shows_data = {}
    artist = show.find('span', class_='artisteventsname')
    date = show.find('span', class_='artisteventdate')
    link = show.find_all('a')[1]
    link_to_ticketweb = show.find_all('a')[2]

    artist_text = artist.text.strip()
    if should_skip_artist(artist_text):
      continue

    all_shows_data['artist'] = [artist_text]
    date = date.text.strip().replace('Mon ', '').replace('Tue ', '').replace('Wed ', '').replace('Thu ', '').replace('Fri ', '').replace('Sat ', '').replace('Sun ', '').replace(', 2023', '').replace(', 2024', '')
    date = date.replace('August ', '2023-08-').replace('September ', '2023-09-').replace('October ', '2023-10-').replace('November ', '2023-11-').replace('December ', '2023-12-').replace('January ', '2024-01-').replace('February ', '2024-02-').replace('March ', '2024-03-').replace('April ', '2024-04-').replace('May ', '2024-05-').replace('June ', '2024-06-').replace('July ', '2024-07-') + 'T20:00:00'
    all_shows_data['date'] = date.replace('-1T', '-01T').replace('-2T', '-02T').replace('-3T', '-03T').replace('-4T', '-04T').replace('-5T', '-05T').replace('-6T', '-06T').replace('-7T', '-07T').replace('-8T', '-08T').replace('-9T', '-09T')
    if link_to_ticketweb.text.strip() == 'Sold Out!':
      all_shows_data['sold_out'] = True
    all_shows_data['link'] = link.get('href')
    all_shows_data['venue'] = 'Subterranean'
    
    all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2)
print(all_shows_json)
