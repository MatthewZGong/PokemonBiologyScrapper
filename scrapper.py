import requests
from bs4 import BeautifulSoup
import json

URL_BULBAPEDIA = "https://bulbapedia.bulbagarden.net"
URL_POKEDEX = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
URL_BULBAPEDIA_ITEMS = "https://bulbapedia.bulbagarden.net/wiki/List_of_items_by_name"
pokemon_data = {}

def parse_pokemon_entry(href, pokemon_name, pokemon_number):
    page = requests.get(URL_BULBAPEDIA + href)
    results = BeautifulSoup(page.content, "html.parser")
    biology = results.find("span", id="Biology")
    parent_header = biology.parent.next_sibling
    biology_description = ""
    while(parent_header != None and parent_header.name != "h2" and parent_header.name != "h3"):
        if(parent_header.name == "p"):
            biology_description += parent_header.text 
            
        parent_header = parent_header.next_sibling
    pokemon_data[pokemon_name] = {
        "number": pokemon_number,
        "biology": biology_description
    }

    # print(parent_header.next_elements)
    # while




def parse_pokedex():
    page = requests.get(URL_POKEDEX)

    results = BeautifulSoup(page.content, "html.parser")

    generations = results.find_all("table", class_="roundy")
    number = ""
    for generation in generations:
        for entry in generation.find_all("tr"):
            columns = entry.find_all("td")
            if(columns == []):
                continue
            #alternative forms
            if(columns[0].find("a") != None):
                pokemon_tag = columns[1]
                pokemon_a = pokemon_tag.find("a")
                ref = pokemon_a.get("href")
                pokemon_name = pokemon_a.text
                form = " "+pokemon_tag.find("small").text
                
                pokemon_name += form
                parse_pokemon_entry(ref, pokemon_name, number)
            else:
                number_tag = columns[0]
                number = number_tag.text
                pokemon_tag = columns[1]
                pokemon_a = pokemon_tag.find("a")
                ref = pokemon_a.get("href")
                pokemon_name = pokemon_a.get("title")
                parse_pokemon_entry(ref, pokemon_name, number)
            print(number, pokemon_name)
            # break
        # break
    with open('pokemon_data.json', 'w') as json_file:
        json.dump(pokemon_data, json_file, indent=4)
        # poke = comp.find("a")
        # print(poke.text)
def parse_item_table(table, items_json): 
    for i,entry in enumerate(table.find_all("tr")):
        if(i == 0):
            continue
        columns = entry.find_all("td")
        if(len(columns) != 4):
            continue
        # print(columns)
        name = columns[1].text
        description = columns[3].text
        items_json[name] = description

    #
def parse_pokemon_item():
    page = requests.get(URL_BULBAPEDIA_ITEMS)
    results = BeautifulSoup(page.content, "html.parser")
    item_table_by_alphabet = results.find_all("table", class_="roundy")
    items_json = {}
    with open('items_data.json', 'w') as json_file:
        for i,table in enumerate(item_table_by_alphabet):
            # items_json = {}
            parse_item_table(table, items_json)
            print(chr(ord('A')+i))
        json.dump(items_json, json_file, indent=4)
            # break
            





    
#problems maybe 
#niodorino is a form of nidoranf

if __name__ == "__main__":
    # parse_pokedex()
    parse_pokemon_item()