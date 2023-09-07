import requests
from bs4 import BeautifulSoup 
import json
from datetime import datetime
from collections import OrderedDict
import re

url_base = 'https://bottomlounge.com/?twpage='
url_pages = [0, 1, 2]

all_shows_list = []
 
for url_page in url_pages:
  url_concat = url_base + str(url_page)
  session = requests.Session()
  page = session.get(url_concat, headers={'User-Agent': 'Mozilla/5.0'})
  soup = BeautifulSoup(page.content, 'html.parser')
  calendar = soup.find('div', class_='tw-plugin-upcoming-event-list')
  shows = calendar.find_all('div', class_='tw-section')

  for show in shows:
    all_shows_data = {}

    headliner = show.find('div', class_='tw-name').text.strip()
    opener = show.find('div', class_='tw-opening-act').text.strip().replace('with ', '')
    artists_with_openers = [headliner + ', ' + opener]

    if 'TWO DAY TICKET' not in headliner:
      # Create a list to store unique artist names while maintaining order
      unique_artists_list = []

      # Process each entry in the list
      for entry in artists_with_openers:
        artists = entry.split(', ')  # Split by comma and space
        for artist in artists:
          artist = artist.strip()  # Remove leading/trailing spaces
          artist = artist.rstrip('.') # Remove trailing periods
          if artist:
            is_substring = False
            artist_lower = artist.lower()  # Convert to lowercase for case-insensitive check
            for existing_artist in unique_artists_list:
              existing_artist_lower = existing_artist.lower()  # Convert to lowercase
              # Use regular expressions to check for substring match ignoring spaces and special characters
              if re.search(r'\b' + re.escape(artist_lower) + r'\b', existing_artist_lower, re.IGNORECASE):
                is_substring = True
                break
            if not is_substring:
              unique_artists_list.append(artist)

      if opener == '':
        all_shows_data['artist'] = [headliner]
      else:
        all_shows_data['artist'] = unique_artists_list

    date = show.find('span', class_='tw-event-date').text.strip()
    time = show.find('span', class_='tw-event-time').text.strip()
 
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
    time = datetime.strptime(time, '%I:%M %p').time()
    all_shows_data['date'] = str(date).split(' ', 1)[0] + 'T' + str(time)

    link = show.find_all('a')[0]
    all_shows_data['link'] = link.get('href')

    all_shows_data['venue'] = 'Bottom Lounge'
    all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2)
print(all_shows_json)
