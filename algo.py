import pandas as pd
import sqlite3
import random
import numpy as np

db = sqlite3.connect('bird_database.db')
cursor = db.cursor()

birdlist = pd.read_json("./bird_data.json")
birdlist = birdlist[["Name", "Plumage colour(s)", "Beak Colour(s)", "Feet colour(s)", "Leg colour(s)", "Beak Shape 1", "Tail shape 1", "Size", "Habitat(s)"]]#"Pattern/ Markings", 

def getRandAdj(curr_bird, column_names):
    adjectives = None
    adj = None
    while not adjectives or not adj:
        if not len(column_names):
            return None, None, None
        new_feature = column_names[random.randint(0, len(column_names) - 1)]
        if not curr_bird[new_feature]:
            column_names = column_names.drop(new_feature)
            continue
        adjectives = curr_bird[new_feature].split(', ')
        adj = adjectives[random.randint(0, len(adjectives) - 1)].lower()
        if adj in curr_guess[new_feature]:
            adj = None
    curr_bird[new_feature] = ', '.join([a for a in curr_bird[new_feature].split(', ') if a.lower() != adj])
    if all(not curr_bird[feature] for feature in column_names):
        return None, None, None
    return adj, new_feature, column_names

def filterSql(curr_guess):
    query = "SELECT * FROM BirdInfo WHERE 1=1"
    params = []
    for key, value in curr_guess.items():
        if not value:
            continue
        conditions = []
        key = f"`{key}`"
        for item in value:
            conditions.append(f"{key} LIKE ?")
            params.append(f"%{item}%")      
        if conditions:
            query += f" AND ({' AND '.join(conditions)})"
    return cursor.execute(query, params).fetchall()


from collections import defaultdict
results = defaultdict(list)
not_found = defaultdict(list)
print('---------Simulation beggining------------')
for _ in range(1000000): 
    curr_guess = {
        "Plumage colour(s)": [],
        "Beak Colour(s)" : [],
        "Feet colour(s)" : [],
        "Leg colour(s)" : [],
        "Beak Shape 1" : [],
        "Tail shape 1" : [],
        # "Pattern/ Markings" : [],
        "Size" : [],
        "Habitat(s)" : [] 
    }
    current_bird = birdlist.loc[random.randint(0, 19)].copy()
    columns = birdlist.drop(columns='Name').columns
    Valid_list = birdlist
    iteration = 0
    while(len(Valid_list) > 1):
        adj, new_feature, columns = getRandAdj(current_bird, columns)
        if not adj:
            # print('------------Results---------------')
            # print(f"could not find match for {current_bird.iloc[0]} after {iteration} iterations")
            # names = [bird[0] for bird in Valid_list]
            # print(names)
            break
        curr_guess[new_feature].append(adj)
        prev_len = len(Valid_list)
        Valid_list = filterSql(curr_guess)
        iteration += 1
        # print(f"Iteration #{iteration}:\nAdded feature: {new_feature} --> {adj}\nCurrent list of features: {curr_guess}\nNumber of filter with that feature: {prev_len - len(Valid_list)}")
    if adj:
        # print('------------Results---------------')
        # print(f"Found {Valid_list[0][0]} after {iteration}")
        # print(f"List of features is {curr_guess}")
        if not results[current_bird.iloc[0]]:
            results[current_bird.iloc[0]] = [iteration]
        else:
            results[current_bird.iloc[0]].append(iteration)
    else:
        if not not_found[current_bird.iloc[0]]:
            not_found[current_bird.iloc[0]] = [[bird[0] for bird in Valid_list]]
        else:
            not_found[current_bird.iloc[0]].append([bird[0] for bird in Valid_list])
print('---------summary-----------')
for key, value in results.items():
    unfound = 0
    if not_found[key]:
        unfound = len(not_found[key])
    print(f"{key} was found {len(value) / (len(value) + unfound) * 100:.0f}% with an average of {np.mean(value):.1f} guess")

    