# -*- coding: utf-8 -*-
"""
Stooq website - web scrapping

This is a base script file.
"""

from bs4 import BeautifulSoup
import requests

def main():
    
    while True:

        company = input("Please type company ID. Example ccc or pkn or wig20\t:")
        print('You picked {} company'.format(company))
        
        
        _id = {"s": company}
        website = requests.get("http://stooq.pl/q/", params=_id)
        soup = BeautifulSoup(website.text, 'lxml')
        
        
        #Find current rate
        find_rate = soup.find("span", id=f"aq_{company}_c2")
        rate = float(find_rate.text)
        print('Current rate for {} company is: {} zł'.format(company, rate))
        
        
        #Find company absolute change in percents[%]
        find_absolute_change = soup.find("span", id=f"aq_{company}_m2")
        absolute_change= float(find_absolute_change.text)
        print('Current absolute change for {} company is: {} %'.format(company, absolute_change))
        
        
        #Find company relative change in percents[%]
        find_relative_change = soup.find("span", id=f"aq_{company}_m3")
        relative_change = float(find_relative_change.text[1:-2])/100
        print('Current relative change for {} company is: {} %'.format(company, relative_change))
        
        
        #Find company transaction count
        transaction_count = soup.find(text="Transakcje").next_element.next_element
        transactions = int(transaction_count.text.replace(" ", ""))
        print('Current ransaction count for {} company is: {} '.format(company, transactions))
        
        while True:
          decision = input('Do you want check another company? (t/n) ')
          if decision == 't':
            break
          elif decision == 'n':
            print('Bye!')
            input('Type any key to close program ...')
            return
          else:
            print('Please type correct answer! (t/n)')

if __name__ == "__main__":
  main()