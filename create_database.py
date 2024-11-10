import pandas as pd
import sqlite3
import random

db = sqlite3.connect('bird_database.db')
cursor = db.cursor()

create_table_sql = """
CREATE TABLE IF NOT EXISTS BirdInfo (
    "Name" TEXT,
    "Plumage colour(s)" TEXT,
    "Beak Colour(s)" TEXT,
    "Feet colour(s)" TEXT,
    "Leg colour(s)" TEXT,
    "Beak Shape 1" TEXT,
    "Tail shape 1" TEXT,
    "Size" TEXT,
    "Habitat(s)" TEXT
);
"""
    # "Pattern/ Markings" TEXT,

cursor.execute(create_table_sql)
birdlist = pd.read_json("./bird_data.json")
birdlist = birdlist[["Name", "Plumage colour(s)", "Beak Colour(s)", "Feet colour(s)", "Leg colour(s)", "Beak Shape 1", "Tail shape 1", "Size", "Habitat(s)"]]#"Pattern/ Markings", 
birdlist.to_sql('BirdInfo', db, if_exists='append', index=False)