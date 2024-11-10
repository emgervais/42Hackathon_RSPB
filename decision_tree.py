import pandas as pd
from collections import Counter
import math
from typing import List, Dict, Set
import sys
import random
from collections import defaultdict
import numpy as np

class BirdIdentifier:
    def __init__(self, birds_df):
        self.birds_df = birds_df
        self.birds = birds_df.to_dict('records')
        self.curr_bird = None
        self.features = [
            "Plumage colour(s)", "Beak Colour(s)", "Feet colour(s)", 
            "Leg colour(s)", "Beak Shape 1", "Tail shape 1", 
            "Size", "Habitat(s)"
        ]

    def can_feature_split_further(self, current_birds, feature):
        possible_values = self.get_possible_values(current_birds, feature)
        current_size = len(current_birds)
        
        for value in possible_values:
            filtered_birds = self.filter_birds(current_birds, feature, value)
            if len(filtered_birds) < current_size and len(filtered_birds) > 0:
                return True
        return False
    
    def find_best_feature(self, current_birds, used_features):
        best_score = float('inf')
        best_feature = None
        
        for feature in self.features:
            if feature not in used_features:
                if not self.can_feature_split_further(current_birds, feature):
                    continue
                    
                possible_values = self.get_possible_values(current_birds, feature)
                if not possible_values:
                    continue
                
                total_remaining = 0
                max_group_size = 0
                for value in possible_values:
                    matching_birds = self.filter_birds(current_birds, feature, value)
                    group_size = len(matching_birds)
                    total_remaining += group_size
                    max_group_size = max(max_group_size, group_size)
                
                avg_remaining = total_remaining / len(possible_values)
                score = avg_remaining + max_group_size
                
                if score < best_score:
                    best_score = score
                    best_feature = feature
        
        if not best_feature:
            for feature in self.features:
                if (feature not in used_features and 
                    self.can_feature_split_further(current_birds, feature)):
                    return feature
                    
        return best_feature

    def filter_birds(self, current_birds, feature, value):
        return [bird for bird in current_birds 
                if pd.isna(bird.get(feature)) or value in bird.get(feature, '')]

    def get_possible_values(self, birds_subset, feature):
        values = set()
        for bird in birds_subset:
            if feature in bird and not pd.isna(bird[feature]):
                bird_values = set(v.strip() for v in bird[feature].split(','))
                values.update(bird_values)
        return values

    def identify_bird(self, auto=False):
        current_birds = self.birds.copy()
        used_features = set()
        if auto:
            self.curr_bird = self.birds_df.loc[random.randint(0, 19)].copy()
            # print(f"Bird to guess: {self.curr_bird.iloc[0]}")
        it = 0
        while len(current_birds) > 1:
            best_feature = self.find_best_feature(current_birds, used_features)
            possible_values = self.get_possible_values(current_birds, best_feature)
            if not best_feature:
                break
            feature_display = best_feature.replace('(s)', '').strip()
            if auto == False:
                value = self.get_input(possible_values, feature_display)
            else:
                value = self.get_automatic(best_feature, possible_values)
            current_birds = self.filter_birds(current_birds, best_feature, value)
            used_features.add(best_feature)
            # print(f"{best_feature} : {value}")
            # print(f"\nRemaining birds: {len(current_birds)}")
            it += 1
            # if len(current_birds) <= 5:
            #     print("Possible matches:")
            #     for bird in current_birds:
            #         print(f"- {bird['Name']}")
        
        return current_birds, it
    
    def get_input(self, possible_values, feature_display):
        print(f"\nWhat is the bird's {feature_display}?")

        sorted_values = sorted(possible_values)
        for i, value in enumerate(sorted_values, 1):
            print(f"{i}. {value}")
        while True:
            try:
                choice = input("\nEnter the number of your choice: ").strip()
                if choice.lower() == 'q':
                    exit(0)
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(sorted_values):
                    value = sorted_values[choice_idx]
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        return value
    def get_automatic(self, feature, possible):
        values = self.curr_bird.loc[feature]
        if not values:
            return random.choice(list(possible))
        values = values.split(', ')
        return values[random.randint(0, len(values) - 1)]

def run_bird_identifier():
    try:
        sample_birds = pd.read_json("./bird_data.json")
        sample_birds = sample_birds[[
            "Name", "Plumage colour(s)", "Beak Colour(s)", 
            "Feet colour(s)", "Leg colour(s)", "Beak Shape 1", 
            "Tail shape 1", "Size", "Habitat(s)"
        ]]
        
        identifier = BirdIdentifier(sample_birds)
        if '-a' in sys.argv:
            loop_search(identifier)
        else:
            results, _ = identifier.identify_bird()
        
            if results:
                print("\nFinal matches:")
                for bird in results:
                    print(f"- {bird['Name']}")
            else:
                print("\nNo matches found or identification canceled.")
            
    except FileNotFoundError:
        print("Error: Could not find bird_data.json file.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def loop_search(identifier):
    summary = defaultdict(list)
    not_found = defaultdict(list)
    print('----------Simulation start--------------')
    for _ in range(1000000):
        results, iterations = identifier.identify_bird(True)
        guessed_bird = identifier.curr_bird.iloc[0]
        # print('----------results---------')
        # print(f"Try tho guess {guessed_bird}")
        if len(results) > 1:
            # print(f"Couldn't end with a match in {iterations} iterations. Final matches:\n {[bird['Name'] for bird in results]}")
            if not not_found[guessed_bird]:
                not_found[guessed_bird] = [[bird['Name'] for bird in results]]
            else:
                not_found[guessed_bird].append([bird['Name'] for bird in results])
        else:
            # print(f"Found match for {results[0]['Name']} in {iterations} iterations")
            if not summary[guessed_bird]:
                 summary[guessed_bird] = [iterations]
            else:
                summary[guessed_bird].append(iterations)
    print('------------summary------------')
    for key, value in summary.items():
        unfound = 0
        if not_found[key]:
            unfound = len(not_found[key])
        print(f"{key} was found {len(value) / (len(value) + unfound) * 100:.0f}% with an average of {np.mean(value):.1f} guess")
    
if __name__ == "__main__":
    run_bird_identifier()