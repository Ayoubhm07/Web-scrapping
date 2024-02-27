from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.associations
collection = db.associations
data_to_insert = []

html_text = requests.get('https://autisme-professionnels-tunisie.tn/liste-categories/centres/').text
soup = BeautifulSoup(html_text, 'lxml')
centres = soup.find_all('div', class_='lp-grid6-top-container')
for centre in centres:
    # Localisation (élimination des espaces)
    centre_localisation = centre.find('div', class_='show').text.strip()

    # Lien du centre
    centre_lien = centre.find('a')['href']

    # Récupération de la page du centre
    page_centre = requests.get(centre_lien).text
    soup = BeautifulSoup(page_centre, 'lxml')

    # Détails du centre
    centre_details = soup.find('div', class_='col-md-8 col-sm-8 col-xs-12')
    centre_nom = centre_details.find('h1').text

    # Vérification du numéro de téléphone
    centre_number_verif = soup.find('li', class_='lp-listing-phone')
    if centre_number_verif is not None:
        centre_phone_number = centre_number_verif.find('a').find('span', class_='').text.strip()
    else:
        centre_phone_number = None

    # Ajout des données à la liste
    data_to_insert.append({
        "name": centre_nom,
        "phone_number": centre_phone_number,
        "localisation": centre_localisation,
        "profile_link": centre_lien
    })
    print(f'''
    Phone : {centre_phone_number}
    Centre: {centre_nom}
    Localisation : {centre_localisation} 
    Lien : {centre_lien}
    ''')
collection.insert_many(data_to_insert)
print("Données insérées avec succès dans la base de données MongoDB.")
