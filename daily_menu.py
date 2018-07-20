import sys
import os
import re
import requests
import datetime
import string
from lxml import html

class menu_scraper:
    
    name = ""
    menu = []
    prices = []
    
    def __init__(self):
        pass
    
    def scrape_roubas(self):
        self.name = "U ROUBASE"
        page_content = requests.get('http://www.uroubase.cz')
        tree = html.fromstring(page_content.content)
        self.menu = tree.xpath('//*[@id="dailymenu"]/div/div/div/table/tr/td[1]/text()')
        self.prices = tree.xpath('//*[@id="dailymenu"]/div/div/div/table/tr/td/strong/text()')
        del tree, page_content
        # convert prices from string to float and remove zeros
        prices_float = []
        for item in self.prices:
            item = float(item.replace(',', '.'))
            if item != 0.0:
                prices_float.append(item)
        self.prices = prices_float
        del prices_float
    
    def scrape_periferie(self):
        self.name = "PERIFERIE"
        page_content = requests.get('https://www.periferierestaurant.cz/')
        tree = html.fromstring(page_content.content)
        self.menu = tree.xpath('//*[@class="col-md-5 daily-menu"]/div/div/table/tbody/tr/td[2]//text()')
        self.prices = tree.xpath('//*[@class="col-md-5 daily-menu"]/div/div/table/tbody/tr/td[3]//text()')
        del tree, page_content
        # extract digits from string and convert them to floats
        prices_float = []
        for item in self.prices:
            item = float(re.sub("\D", "", item))  
            prices_float.append(item)
        self.prices = prices_float
        del prices_float
        
    def scrape_pivovar(self):
        self.name = "OLIVUV PIVOVAR"
        self.menu = []
        self.prices = []
        
    def sort_prices_low_to_high(self):
        self.menu = [x for _, x in sorted(zip(self.prices, self.menu))]
        self.prices = sorted(self.prices)
        
    def print_menu(self):
        print(self.name)
        for i in range(len(self.menu)):
            print(i+1, self.menu[i], ':', self.prices[i], 'CZK')
        
    def get_menu(self):
        return self.menu
    
    def get_prices(self):
        return self.prices
    
    def get_name(self):
        return self.name

if __name__ == '__main__':
    
    #output = sys.argv[1]
    #sys.stdout = open(output, "wt", encoding="utf-8")
    sys.stdout = open("C:\\Users\\petr.valenta\\Desktop\\menu.txt", "wt", encoding="utf-8")
    
    print(datetime.date.today(), datetime.date.today().strftime("%A"), ':\n')
    scraper = menu_scraper()
    
    scraper.scrape_roubas()
    #scraper.sort_prices_low_to_high()
    scraper.print_menu()
        
    print('')
    
    scraper.scrape_periferie()
    #scraper.sort_prices_low_to_high()
    scraper.print_menu()
        
    print('')
    
    scraper.scrape_pivovar()
    #scraper.sort_prices_low_to_high()
    #scraper.print_menu()
    
    #os.startfile("output.txt", "print")