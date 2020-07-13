import requests
from bs4 import BeautifulSoup

# for finding key by value in a dict

def find_by_val(val, dict_):
    dict_copy = dict_
    for key, value in dict_copy.items():
        if value == val:
            del dict_copy[key]
            return key

# ------------------------ PlayerAuctions ------------------------

PA_data = {
    'sP_ids': {'Fairbanks': 8582, 'Earthshaker': 8583},
    'server_ids': {'Fairbanks': 8751, 'Earthshaker': 9005},
}

def get_PA_data(server, stack_size):
    url = f'https://www.playerauctions.com/wow-classic-gold/?SortField=cheapest-price&sPid={PA_data["sP_ids"][server]}&Serverid={PA_data["server_ids"][server]}&Quantity={stack_size}&PageIndex=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    page_offers = soup.find_all("div", {"class": "offer-price"})[2:]

    for offer in page_offers:
        print(offer.get_text()[2:8])

# get_PA_data('Earthshaker', 1000)

# ------------------------ iGVault ------------------------

iGVault_data = {
    'server_id': {'Fairbanks': 2111, 'Earthshaker': 2339},
    'faction_id': {'Fairbanks': 2236, 'Earthshaker': 2343}
}

# for getting a list of names for sorted prices (relevant for iGVault only)

def get_sorted_names(offers, sorted_prices):
    sorted_names = []
    for price in sorted_prices:
        sorted_names.append(find_by_val(price, offers))
    return sorted_names

def get_iGVault_data(server, quantity):
    url = f'https://www.igvault.com/c2c-index/list-get-other-sellers?game_id=1830&server_id={iGVault_data["server_id"][server]}&camp_id={iGVault_data["faction_id"][server]}&quantity={quantity}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    page_offers_price = soup.find_all("div", {"class": "offers-us"})
    page_offers_name = soup.find_all("div", {"class": "offers-name"})

    offers = dict(zip([i.select("strong")[0].text for i in page_offers_name], [float(i.select("strong")[0].text[:-4]) for i in page_offers_price]))
    sorted_offers = dict(zip([price for price in sorted(offers.values())], [name for name in get_sorted_names(offers, sorted(offers.values()))]))

    for offer in sorted_offers:
        print(offer, sorted_offers[offer])


get_iGVault_data('Earthshaker', 1000)