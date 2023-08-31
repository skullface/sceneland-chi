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
    excluded_keywords = ['Open Mic', 'SOX SUNDAYS', 'Tabletop Fleapit', 'Bingo with Tyler', 'UNDERGROUND WONDER', 'Underground Wonder', 'WRESTLING', 'MR. BLOTTO', 'MICHAEL JOHNSON', 'MICHAEL ROBINSON', 'TAILGATE PARTY', 'ART SHOW']
    for artist in artists_elements:
      artist_text = artist.text.strip()
      # Check if artist text contains any excluded keyword
      if any(keyword in artist_text for keyword in excluded_keywords):
        continue
      artists_list.append(artist_text.replace(' / ', ', '))
    if artists_list:
        all_shows_data['artist'] = artists_list

    date = show.find('time')
    all_shows_data['date'] = date.get('datetime') + 'T20:00:00'
    link = show.find('a', class_='expandshow')
    all_shows_data['link'] = link.get('href')
    all_shows_data['venue'] = 'Reggie’s'
    all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2)
print(all_shows_json)
