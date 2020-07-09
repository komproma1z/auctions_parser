import requests
from bs4 import BeautifulSoup

PA_data = {
    'sP_ids': {'Fairbanks': 8582, 'Earthshaker': 8583},
    'server_ids': {'Fairbanks': 8751, 'Earthshaker': 9005},
}

iGVault_data = {
    'server_id': {'Fairbanks': 2111, 'Earthshaker': 2339},
    'faction_id': {'Fairbanks': 2236, 'Earthshaker': 2343}
}

def get_PA_data(server, stack_size):
    url = f'https://www.playerauctions.com/wow-classic-gold/?SortField=cheapest-price&sPid={PA_data["sP_ids"][server]}&Serverid={PA_data["server_ids"][server]}&Quantity={stack_size}&PageIndex=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    page_offers = soup.find_all("div", {"class": "offer-price"})[2:]

    for offer in page_offers:
        print(offer.get_text()[2:8])

# get_PA_data('Earthshaker', 1000)

def get_iGVault_data(server, quantity):
    url = f'https://www.igvault.com/c2c-index/list-get-other-sellers?game_id=1830&server_id={iGVault_data["server_id"][server]}&camp_id={iGVault_data["faction_id"][server]}&quantity={quantity}'
    # url = f'https://www.igvault.com/WOW-Classic-Gold/Fairbanks-US/Alliance.html'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    page_offers_price = soup.find_all("div", {"class": "offers-us"})
    page_offers_name = soup.find_all("div", {"class": "offers-name"})

    offers = dict(zip([i.select("strong")[0].text for i in page_offers_name], [float(i.select("strong")[0].text[:-4]) for i in page_offers_price]))

    # print(offers.keys(), offers.values())

    for i in offers:
        print(i, offers[i])

    # for i in sorted(offers.values()):
    #     # print(i, offers[i])
    #     print(offers[i], i)


get_iGVault_data('Fairbanks', 1000)