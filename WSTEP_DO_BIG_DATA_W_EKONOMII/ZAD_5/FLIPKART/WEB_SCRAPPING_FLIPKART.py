# -*- coding: utf-8 -*-
"""
Flipkart website - web scrapping

This is a base script file.
"""

from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup


driver = webdriver.Chrome("D:/chromedriver.exe")


products=[] #List to store name of the product
prices=[] #List to store price of the product
ratings=[] #List to store rating of the product
driver.get("https://www.flipkart.com/laptops/~buyback-guarantee-on-laptops-/pr?sid=6bo%2Cb5g&uniq")


content = driver.page_source
soup = BeautifulSoup(content, "lxml")


def main():

    for a in soup.findAll('a',href=True, attrs={'class':'_31qSD5'}):
        name=a.find('div', attrs={'class':'_3wU53n'})
        price=a.find('div', attrs={'class':'_1vC4OE _2rQ-NK'})
        rating=a.find('div', attrs={'class':'hGSR34'})
    
        products.append(name.text)
        prices.append(price.text)
        ratings.append(rating.text) 
    
       
    df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings})
    df.to_csv('D:/products.csv',index = False)
    print(df)

if __name__ == "__main__":
  main()