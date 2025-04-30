import sqlite3 
from prettytable import from_db_cursor


conn = sqlite3.connect("events.db")
curs = conn.cursor()

curs.execute("""
CREATE TABLE EVENTS(
        EventName VARCHAR(50),
        Location VARCHAR(50),
        EventDate VARCHAR(50),
        Latitude VARCHAR(50),
        Longitude VARCHAR(50)
);       
""")



conn.commit()