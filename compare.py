import numpy as np
import pandas as pd
import matplotlib.plot as plt

def read_final_dict(url="boxofficemojo_final_dictionary.json"):
    with open(url, "rb") as json_file:
        return json.load(json_file)

def genres():
    # genre_dict = {}
    # for movie in main_dict:
    #     for genre in movie['genres']
    #         genre_dict.setdefault(genre, 1).update()

main_dict = read_final_dict()
genres()