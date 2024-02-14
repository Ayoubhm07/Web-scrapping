from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.psychiatres
collection = db.psychiatres

data_to_insert = []

# Initialiser le numéro de page à 1
page_number = 1

while True:
    html_text = requests.get(f'https://www.dabadoc.com/tn/psychiatre/{page_number}').text
    soup = BeautifulSoup(html_text, 'html.parser')
    doctors = soup.find_all('div', class_='search_doc_row')
    if not doctors:
        break

    for doctor in doctors:
        doctor_name = doctor.find('h2', class_='blue-text h5').text.strip()
        doctor_profile = doctor.find('a', class_='btn btn-block btn-info btn-profile')['href'].strip()
        data_to_insert.append({"name": doctor_name, "profile_link": doctor_profile})
        print(f"Doctor Name : {doctor_name}")
        print(f"Profile Link : {doctor_profile}")

    page_number += 1

    collection.insert_many(data_to_insert)

print("Données insérées avec succès dans la base de données MongoDB.")
