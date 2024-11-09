import pandas as pd
import sqlite3
import random

db = sqlite3.connect('bird_database.db')
cursor = db.cursor()

# create_table_sql = """
# CREATE TABLE IF NOT EXISTS BirdInfo (
#     "Name" TEXT,
#     "Plumage colour(s)" TEXT,
#     "Beak Colour(s)" TEXT,
#     "Feet colour(s)" TEXT,
#     "Leg colour(s)" TEXT,
#     "Beak Shape 1" TEXT,
#     "Tail shape 1" TEXT,
#     "Pattern/ Markings" TEXT,
#     "Size" TEXT,
#     "Habitat(s)" TEXT
# );
# """

# cursor.execute(create_table_sql)
birdlist = pd.read_json("./bird_data.json")
birdlist = birdlist[["Name", "Plumage colour(s)", "Beak Colour(s)", "Feet colour(s)", "Leg colour(s)", "Beak Shape 1", "Tail shape 1", "Pattern/ Markings", "Size", "Habitat(s)"]]
# birdlist.to_sql('BirdInfo', db, if_exists='append', index=False)
curr_guess = {
    "Plumage colour(s)": [],
    "Beak Colour(s)" : [],
    "Feet colour(s)" : [],
    "Leg colour(s)" : [],
    "Beak Shape 1" : [],
    "Tail shape 1" : [],
    "Pattern/ Markings" : [],
    "Size" : [],
    "Habitat(s)" : [] 
}
curr_bird = birdlist.loc[random.randint(0, 21)]
column_names = birdlist.drop(columns='Name').columns
print(curr_bird)
Valid_list = birdlist

def getRandAdj(curr_bird, column_names):
    adjectives = None
    adj = None
    while not adjectives or not adj:
        new_feature = column_names[random.randint(0, len(column_names) - 1)]
        if not curr_bird.loc[new_feature]:
            continue
        adjectives = curr_bird.loc[new_feature].split(', ')
        adj = adjectives[random.randint(0, len(adjectives) - 1)]
        adj = adj.lower()
        if adj in curr_guess[new_feature]:
            adj = None
    curr_bird[new_feature] = ', '.join([a for a in curr_bird[new_feature].split(', ') if a.lower() != adj])
    if all(not curr_bird.loc[feature] for feature in column_names):
        return None, None
    return adj, new_feature

def filterSql(curr_guess):
    query = "SELECT * FROM BirdInfo WHERE 1=1"
    params = []
    for key, value in curr_guess.items():
        if not len(value):
            continue
        conditions = []
        key = f"`{key}`"
        for item in value:
            conditions.append(f"{key} LIKE ?")
            params.append(f"%{item}%")
        
        query += f" AND ({' OR '.join(conditions)})"
    return cursor.execute(query, params).fetchall()



iteration = 0

while(len(Valid_list) > 1):
    adj, new_feature = getRandAdj(curr_bird, column_names)
    if not adj:
        print(f"could not find match after {iteration} iterations")
        exit(1)
    curr_guess[new_feature].append(adj)
    Valid_list = filterSql(curr_guess)
    iteration += 1
print(Valid_list[0])
    