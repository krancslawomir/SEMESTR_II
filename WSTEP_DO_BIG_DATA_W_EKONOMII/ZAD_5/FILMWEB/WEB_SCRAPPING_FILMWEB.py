# -*- coding: utf-8 -*-
"""
Filmweb website - web scrapping

This is a base script file.
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd

def main():
         
    website = requests.get("https://www.filmweb.pl/film/Narodziny+gwiazdy-2018-542576")
    
    soup = BeautifulSoup(website.text, 'lxml')
    
    director_list=[] #List to store director name
    date_list=[] #List to store release date of the movie
    boxoffice_list=[] #List to store boxoffice of the movie
    rating_list=[] #List to store rating of movie
    
    #Find director
    director = str(soup.find("span", itemprop="name").text.replace(",", "."))
    print('Director name is: {}'.format(director))
    director_list.append(director)
    
    #Find release date
    date = str(soup.find("span", attrs={'class':'block'}).text.replace(",", "."))
    print('Release date is: {}'.format(date))
    date_list.append(date)
    
    #Find box office
    boxoffice = str(soup.find("div", attrs={'class':'boxoffice'}).text.replace(",", "."))
    print('Box office is: {}'.format(boxoffice))
    boxoffice_list.append(boxoffice)
    
    rating = float(soup.find("span", itemprop="ratingValue").text.replace(",", "."))
    print('Movie rating is: {}'.format(rating))
    rating_list.append(rating)


    df = pd.DataFrame({'Director Name':director_list,'Release date':date_list,'Box Office':boxoffice_list, "Movie rating":rating_list})
    df.to_csv('D:/movie.csv',index = False)
    
    
if __name__ == "__main__":
  main()