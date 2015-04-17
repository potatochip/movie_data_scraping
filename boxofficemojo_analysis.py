
# coding: utf-8

# In[111]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

def read_final_dict(url="boxofficemojo_final_dictionary.json"):
    with open(url, "rb") as json_file:
        return json.load(json_file)
main_dict = read_final_dict()


# In[105]:

#destroys main_dict so need to reload the above every time before running this
single_headers = ['title', 'runtime', 'rating', 'studio','opening date', 'opening gross', 'opening theaters', 
 'total gross', 'total theaters', 'boxofficemojo url']
genrelist = []
actorlist = []
singlevaluedict = {}
for title, movie in main_dict.iteritems():
    if 'genres' in movie: genrelist.append([title] + movie.pop('genres'))
    if 'actors' in movie: actorlist.append([title] + movie.pop('actors'))
    singlevaluedict.update({title: [movie.get(header,'unknown') for header in single_headers]})


# In[112]:

# print(genrelist)
df = pd.DataFrame(genrelist)
names = df.columns.tolist()
names[names.index(0)] = 'title'
df.columns = names
#pd.set_option('display.max_rows', 500)
genre_df = df[range(1,10)].stack().value_counts()
df.head()


# In[177]:

mylist=[]
for row in genrelist:
    for values in row:
        if row[0] != values:
            mylist.append([row[0], values])
genre_df = pd.DataFrame(mylist)
genre_df.columns = ['title', 'genre']
genre_df['genre'].value_counts()


# In[178]:

df2 = genre_df[(genre_df['genre'] == 'Shark')]
df2


# In[157]:

mylist=[]
for row in actorlist:
    for values in row:
        if row[0] != values:
            mylist.append([row[0], values])
actor_df = pd.DataFrame(mylist)

actor_df.columns = ['title', 'actors']
actor_df



# In[165]:

single_value_df = pd.DataFrame(singlevaluedict)
single_value_df = single_value_df.T
single_value_df.columns = single_headers
single_value_df


# In[206]:

# single_value_df[['title', 'boxofficemojo url', 'rating']].groupby('rating').size()
single_value_df['rating'].value_counts()


# In[214]:

#dataframe of movies by rating
non_pg_movies = single_value_df[(single_value_df['rating'] == 'R') | (single_value_df['rating'] == 'Unrated') | (single_value_df['rating'] == 'PG-13') | (single_value_df['rating'] == 'Not Yet Rated') | (single_value_df['rating'] == 'NC-17') | (single_value_df['rating'] == 'Unknown') | (single_value_df['rating'] == 'M') | (single_value_df['rating'] == 'unknown') | (single_value_df['rating'] == 'n/a') | (single_value_df['rating'] == 'X')]
non_pg_movies

