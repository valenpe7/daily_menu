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
        page_content = requests.get('https://www.periferierestaurant.cz')
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
        page_content = requests.get('https://www.olivuvpivovar.cz/en')
        # page_content = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
        tree = html.fromstring(page_content.content)
        # self.menu = tree.xpath['//*[@id="main"]/div[2]/div/div[1]/div/div/p[1]/em[2]/text()[1])']
        self.menu = tree.xpath('//p//em//text()')
        # self.prices = tree.xpath['//*[@id="main"]/div[2]/div[1]/div[1]/div/div/p/em[3]/text()']
        self.prices = []
        menu_text = ['']
        price_list = []
        for item in self.menu:
            if "CZK" in item:
                item = item.replace(',-', '')
                item = item.replace(' ', '') + ',-'
                price_list.append(item.replace('CZK', ''))
                menu_text.append('')
            else:
                menu_text[-1] = menu_text[-1] + item
        self.menu = menu_text[0:len(price_list)]
        self.prices = price_list
        del tree, page_content, menu_text, price_list

    def scrape_clarafutura(self):
        self.name = "CLARA FUTURA"
        page_content = requests.get('https://www.clarafutura.cz/restaurant/')
        tree = html.fromstring(page_content.content)
        # self.menu = tree.xpath['id="wpv-view-layout-50294-TCPID50190"/text()[1])']
        ast = tree.xpath('//div[@id="page-container"]//tr/td/text()')
        n = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'].index(datetime.date.today().strftime("%A"))
        i = n * 8
        self.menu = []
        self.prices = []
        while i < (n + 1) * 8:
            self.menu.append(ast[i])
            self.prices.append(ast[i + 1].replace('-Kč', ''))
            i = i + 2
        del tree, page_content, ast, n, i

    def sort_prices_low_to_high(self):
        self.menu = [x for _, x in sorted(zip(self.prices, self.menu))]
        self.prices = sorted(self.prices)

    def print_menu(self):
        print(self.name)
        for i in range(len(self.prices)):
            print(i + 1, self.menu[i], ':', self.prices[i], 'CZK')

    def get_menu(self):
        return self.menu

    def get_prices(self):
        return self.prices

    def get_name(self):
        return self.name


if __name__ == '__main__':
    # output = sys.argv[1]
    # sys.stdout = open(output, "wt", encoding="utf-8")
    # sys.stdout = open("C:\\Users\\chao.lu\\Desktop\\menu.txt", "wt", encoding="utf-8")
    sys.stdout = open(os.path.expanduser("~/Desktop") + "/menu.txt", "wt", encoding="utf-8")

    print(datetime.date.today(), datetime.date.today().strftime("%A"), ':\n')
    scraper = menu_scraper()

    scraper.scrape_roubas()
    # scraper.sort_prices_low_to_high()
    scraper.print_menu()

    print('')

    scraper.scrape_periferie()
    # scraper.sort_prices_low_to_high()
    scraper.print_menu()

    print('')

    scraper.scrape_pivovar()
    # scraper.sort_prices_low_to_high()
    scraper.print_menu()

    print('')

    scraper.scrape_clarafutura()
    # scraper.sort_prices_low_to_high()
    scraper.print_menu()

    # os.startfile("output.txt", "print")
