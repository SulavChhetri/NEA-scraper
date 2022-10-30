import csv
import requests
from bs4 import BeautifulSoup
import time
import schedule
from pathlib import Path
import os
ROOT_DIR = Path(__file__).parent.parent

file_path = os.path.join(ROOT_DIR, 'files')


def hourly_scrape():
    schedule.every().hour.do(scrape_and_insert_product)
    while True:
        schedule.run_pending()
        time.sleep(1)

def daily_scrape():
    schedule.every().second.do(scrape_and_insert_product)
    while True:
        schedule.run_pending()
        time.sleep(1)


def scrape(url):
    try:
        r = requests.get(url).text
        soup = BeautifulSoup(r, "html.parser")
        scraped_data_html = soup.find_all('ul', class_='pl-1 text-primary')
        energy_details_html = scraped_data_html[0]
        iex_html = scraped_data_html[1]
        energy_details = energy_details_html.find_all('h6')
        iex = iex_html.find_all('h6')
        enegry_details_list = [item.text for item in energy_details]
        iex_list = [item.text for item in iex]
        return enegry_details_list, iex_list
    except:
        hourly_scrape()


def scrape_and_insert_product():
    url = 'https://www.nea.org.np/'
    nested_scraped_details = scrape(url)
    if nested_scraped_details != None:
        scrape_into_csv(nested_scraped_details[0], nested_scraped_details[1])

def scrape_into_csv(energy_details, iex):
    energydict={}
    iexdict= {}
    with open(os.path.join(file_path, "energydetails.csv"), 'a') as file:
        writer = csv.writer(file)
        for item in energy_details:
            energy_details_items = item.split(" – ")
            energydict[energy_details_items[0]]=energy_details_items[1]

        # for i in range(len(energydict.keys())):
        #     item_value = list(energydict.values())[i].split()
        #     item_number = int(item_value[0])
        #     item_unit = item_value[1]
        #     value_list.append(item_number)
        #     header = list(energydict.keys())[i]+'('+item_unit+ ')'
        #     header_list.append(header)

        if file.tell() == 0:
            writer.writerow(energydict.keys())
        writer.writerow(energydict.values())

    with open(os.path.join(file_path, "iex.csv"), 'a') as file:
        writer = csv.writer(file)
        for item in iex:
            iex_items = item.split(' – ')
            iexdict[iex_items[0]]=iex_items[1]
        if file.tell() == 0:
            writer.writerow(iexdict.keys())
        writer.writerow(iexdict.values())


if __name__ == "__main__":
    daily_scrape()
    scrape_and_insert_product()
