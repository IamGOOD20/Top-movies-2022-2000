# Top-movies-2022-2000

Starting from the largest movie database in the world, I wrote a program that analyzes 200 the most watchable movies for every year for the past of 22 years (from 2000 to 2022). Films with more than 60 metascore get into the top. The program sorts and writes to the xlsx file in descending order of rating, based on the metascore and IMDB ratings.

# Imports:
    from requests import get
    from bs4 import BeautifulSoup
    import pandas as pd
    from time import sleep, time
    from random import randint
    import os
