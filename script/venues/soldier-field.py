import requests
from bs4 import BeautifulSoup 
import json

session = requests.Session()
page = session.get('https://www.livenation.com/venue/KovZpZAF6tIA/soldier-field-events', headers={'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(page.content, 'html.parser')
calendar = soup.find('ul', class_='css-p47pw5')
shows = calendar.find_all('li', class_='css-re1cpl')

all_shows_list = []

for show in shows:
  all_shows_data = {} 
  artist = show.find('h3', class_='css-1ptng6s').text.strip()
  artist = artist.replace(' - Friday Ticket Only', '').replace(' - Sunday Ticket Only', '')
  link = show.find('a', class_='css-1yxfa6u')
  date = show.find('time')
  if '2 Day Ticket' not in artist:
    all_shows_data['artist'] = [artist]
    all_shows_data['link'] = link.get('href')
    all_shows_data['date'] = date.get('datetime')
    all_shows_data['venue'] = 'Soldier Field'
    all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2) 
print(all_shows_json)
