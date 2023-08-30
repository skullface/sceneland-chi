import requests
from bs4 import BeautifulSoup 
import json

url_base = 'https://www.reggieslive.com/page/'
url_pages = [1, 2, 3, 4]

all_shows_list = []
 
for url_page in url_pages:
  url_concat = url_base + str(url_page)
  session = requests.Session()
  page = session.get(url_concat, headers={'User-Agent': 'Mozilla/5.0'})
  soup = BeautifulSoup(page.content, 'html.parser')
  calendar = soup.find('div', id='middle')
  shows = calendar.find_all('article', class_='show')

  for show in shows:
    all_shows_data = {} 
    artists_elements = show.find('hgroup').findChildren(class_='band-title')
    artists_list = []
    for artist in artists_elements:
      if 'Open Mic' in artist.text.strip():
        ...
      elif 'SOX SUNDAYS' in artist.text.strip():
        ...
      elif 'Tabletop Fleapit' in artist.text.strip():
        ...
      elif 'Bingo with Tyler' in artist.text.strip():
        ...
      elif 'MR. BLOTTO' in artist.text.strip():
        ...
      elif 'MICHAEL JOHNSON' in artist.text.strip():
        ...
      elif 'MICHAEL ROBINSON' in artist.text.strip():
        ...
      elif 'TAILGATE PARTY' in artist.text.strip():
        ...
      elif 'ART SHOW' in artist.text.strip():
        ...
      else:
        all_shows_data['artist'] = artists_list
      artists_list.append(artist.text.strip())
    date = show.find('time')
    all_shows_data['date'] = date.get('datetime') + 'T20:00:00'
    link = show.find('a', class_='expandshow')
    all_shows_data['link'] = link.get('href')
    all_shows_data['venue'] = 'Reggie’s'
    all_shows_list.append(all_shows_data)

  all_shows_json = json.dumps(all_shows_list, indent=2)
  print(all_shows_json)
