from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep, time
from random import randint
import os


# time to cycle scraping
start_time = time()
requests = 0

# name/path/file
# for eng version
xlsx_path_eng = os.path.dirname(__file__) + r'\Movie 2000 - 2022.xlsx'
headers = {"Accept-Language": "en-US, en;q=0.5"}

# in range of 22 years
for year_url in reversed(range(2000, 2023)):

      # for pandas table columnse
      names = []
      genres = []
      years = []
      imdb_ratings = []
      metascores = []
      votes = []
      directors = []
      actors = []

      # if range of 200 movies
      for page in range(1, 152, 50):

            # build link for get
            # for eng version
            response = get(f'https://www.imdb.com/search/title/?release_date={year_url}-01-01,{year_url}-12-31&sort=num_votes,desc&start={page}&ref_=adv_nxt', headers = headers)  # , headers = headers

            sleep(randint(7, 15))
            requests += 1
            html_soup = BeautifulSoup(response.text, 'html.parser')
            movie_containers = html_soup.find_all('div', class_='lister-item mode-advanced')

            # control website response -
            # doesn't work in pycharm, but work in terminal
            elapsed_time = time() - start_time
            reg_elap = requests / elapsed_time
            print(f'Request: {requests}; Frequency: {reg_elap} requests/s')  # , end='\r'

            if response.status_code != 200:
                  print(f'Request: {requests}; Status code: {response.status_code}')

            for container in movie_containers:
                  if container.find('span', class_='metascore favorable') is not None:

                        # movie title
                        name = container.h3.a.text
                        names.append(name)

                        # year
                        # year = container.h3.find('span', class_='lister-item-year text-muted unbold').text
                        # years.append(year)

                        # imbd_ratings
                        imdb_rating = float(container.strong.text)
                        imdb_ratings.append(imdb_rating)

                        # metascore
                        metascore = int(container.find('span', class_='metascore favorable').text)
                        metascores.append(metascore)

                        # vote
                        vote = int(container.find('span', attrs={'name': 'nv'})['data-value'])
                        votes.append(vote)

                        # genre
                        # eng genre
                        genre = container.find('span', class_='genre').text
                        genres.append(genre)

                        # Director
                        # director = container.find('p', class_='').find('a').text
                        # directors.append(director)

      # for eng version
      movie_rat_eng = pd.DataFrame({
            'Metascore rating': metascores,
            'voted on IMDB': votes,
            'IMDB rating': imdb_ratings,
            'movie': names,
            'genre': genres,
            })

      # sort pd by meta and IMDB

      # for eng version
      s_movie_rat_eng = movie_rat_eng.sort_values(by=['Metascore rating', 'IMDB rating'], ascending=False)

      # entry in excel with sheet name each year
      # for eng version
      if os.path.exists(xlsx_path_eng):
            with pd.ExcelWriter(xlsx_path_eng, engine='openpyxl', mode='a') as writer:
                  s_movie_rat_eng.to_excel(writer, index=False, sheet_name=f'Movies {year_url}')
      else:
            with pd.ExcelWriter(xlsx_path_eng, engine='openpyxl', mode='w') as writer:
                  s_movie_rat_eng.to_excel(writer, index=False, sheet_name=f'Movies {year_url}')

# cycle time
print('Cycle time:', time() - start_time)

