from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import logging
import sqlite3

conn = sqlite3.connect("events.db")
curs = conn.cursor()

logging.getLogger('selenium').setLevel(logging.WARNING)

options = webdriver.ChromeOptions()
options.add_argument('--headless') 
options.add_argument('--disable-gpu') 
options.add_argument('--no-sandbox') 
options.add_argument('--disable-dev-shm-usage')  
options.add_argument('start-maximized') 
options.add_argument("--log-level=3") 

driver = webdriver.Chrome(service=Service((ChromeDriverManager().install())), options=options)

allTitles = []
allLocations = []
allDates = []

def scrape_events(url):
    driver.get(url)
    time.sleep(1)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    titles = soup.find_all('a', attrs={'class': 'ember-view _variant-default_1jkwo3 _name_1jkwo3'})

    locations = soup.find_all('div', attrs={'class': '_variant-default_1jkwo3 _info_1jkwo3 _location_1jkwo3'})

    dates = soup.find_all('div', attrs={'class': '_variant-default_1jkwo3 _info_1jkwo3 _date_1jkwo3'})

    events = []
    for title, location, date in zip(titles, locations, dates):

        coordinates = Coordinates(location.get_text(strip=True))
       
        if coordinates != None:
            latitude = coordinates[0]
            longitude = coordinates[1]
        else:
            latitude = 1
            longitude = 1
            
        event_info = {
            'title': title.get_text(strip=True),
            'location': location.get_text(strip=True),
            'date': date.get_text(strip=True),
            'latitude': latitude,
            'longitude': longitude
            
        }
        events.append(event_info)
   
    return events

def Coordinates(location):
    key = "AIzaSyAKf94Hsy2SIdbPlJojSNTuW_xKuZJmBSw"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={key}"
    
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "OK":
        latitude = data["results"][0]["geometry"]["location"]["lat"]
        longitude = data["results"][0]["geometry"]["location"]["lng"]
        return latitude, longitude
   
allData = []

for i in range(10):
    url = f"https://www.fatsoma.com/discover?page={i}"
    events = scrape_events(url)
    print(i)
    allData.extend(events)

driver.quit()

for event in allData:
    curs.execute("INSERT INTO EVENTS(EventName, Location, EventDate, Latitude, Longitude) VALUES(?,?,?,?,?)", (event['title'], event['location'], event['date'], event['latitude'], event['longitude']))
   
conn.commit()

curs.close