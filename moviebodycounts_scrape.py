from __future__ import division
import urllib2
import re
import sys
import json
from pprint import pprint
import time
from bs4 import BeautifulSoup, SoupStrainer
from brinery import *

def emergency_pickle(data, filename):
    f = filename+".recovery.pkl"
    dump_pickle(data,f)
    print("*EMERGENCY PICKLE DUMP TO {0}*".format(f))

def movie_data_saver(datadict, filename="moviebodycounts_movie_data.json"):
    try:
        with open(filename, "wb") as json_file:
            newData = json.dumps(datadict, sort_keys=True, indent=4) 
            json_file.write(newData)
    except:
        emergency_pickle()

def link_data_saver(linklist, filename="moviebodycounts_link_data.txt"):
    try:
        with open(filename, "wb") as txt_file:
            for item in linklist: 
                txt_file.write(item.encode("UTF-8"))
                txt_file.write("\n")
    except:
        emergency_pickle()

def read_main_dict(url="moviebodycounts_movie_data.json"):
    with open(url, "rb") as json_file:
        return json.load(json_file)

def link_grabber(url, base_url="http://moviebodycounts.com/"):
    '''
    grabs all the movie links from a page
    '''
    link_dict = {}
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    all_rows = soup.find(src='graphic-movies.jpg').parent.next_sibling.next_sibling.next_sibling.next_sibling.find_all('a')
    # does not account for when , the is followed by other information like '(1980)'
    #swap 'the' to the beginning when title ends with ', the'
    row_values = {(lambda x: 'The '+x[:-5] if x[-5:] == ', The' else x)(i.text) :i['href'] for i in all_rows}
    #swap "a" to the beginning
    row_values = {(lambda x: 'A '+x[:-3] if x[-3:] == ', A' else x)(k):v for k,v in row_values}
    #swap "an" to the beginning
    row_values = {(lambda x: 'An '+x[:-4] if x[-4:] == ', An' else x)(k):v for k,v in row_values}
    #return with weird space characters removed
    clean_data = {re.sub('\r\n', ' ', k): {"url":base_url+v} for k,v in row_values.items()}
    return clean_data

def movie_links(base_url="http://moviebodycounts.com"):
    category_url ="/movies-"
    categories = ["numbers"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    ending = ".htm" 
    master_dict={}
    link_list = []
    for url in [base_url + category_url + letter + ending for letter in categories]:
        print("processing " + url)
        try:
            master_dict.update(link_grabber(url))
            link_list.append(url)
        except:
            print("Error: {0} doesn't exist".format(url))
    link_data_saver(link_list)
    ## error correction
    master_dict.pop("Narnia (see Chronicles of Narnia)")
    master_dict.pop("Grindhouse: Double Feature")
    return master_dict

def page_parser(url, pickled=None):
    url_fail_list = []
    #check for pickled data
    try:
        page = urllib2.urlopen(url) if pickled == None else pickled
    except:
        # if url can't be found in pickle
        url_fail_list.append(url)
    link_data_saver(url_fail_list, "url_parse_fail_log.txt")
    
    soup = BeautifulSoup(page)
    headers = ["body count", "director", "url"]
    try:
        director = soup.find(text=re.compile("Director:"))
        if director[9] == u'\xa0':
            director = director.next.text
        if len(director) > 12:
            director = director[10:]
        else:
            director = director.next.text
    except:
        try:
            director = soup.find(text=re.compile("Directors:"))
            if len(director) > 13:
                director = director[11:]
            else:
                director = director.next.text
        except:
            print("\n"+"*DIRECTOR FAIL*: "+url)
            director = "n/a"
    director = re.sub('\xa0', ' ', director) 
    director = re.sub('\r\n', ' ', director)
    director = director.strip()
    try:
        body_count = soup.find(text=re.compile('Entire'))
        body_count = body_count.split('(')[0]
        body_count = body_count.split('on')[0]
        body_count = body_count.split('*')[0]
        body_count = body_count.split(":")[1]
    except:
        try:
            body_count = soup.find(text=re.compile('Segment'))
            body_count = body_count.split('(')[0]
            body_count = body_count.split('on')[0]
            body_count = body_count.split('*')[0]
            body_count = body_count.split(":")[1]
        except:
            try:
                body_count = soup.find(text=re.compile('Kills'))
                body_count = body_count.split('Kills')[0]
            except:
                try:
                    body_count = soup.find(text=re.compile('kills'))
                    body_count = body_count.split('kills')[0]
                except:
                    print("\n"+"*BODY COUNT FAIL*: "+url)
                    body_count = "n/a"
    try:
        body_count = re.sub('\xa0', ' ', body_count) 
        body_count = re.sub('\r\n', ' ', body_count)
        body_count = body_count.strip()
    except:
        print("FAIL: " + url + ' kills is ' + str(body_count))
    return dict(zip(headers, [body_count, director, url]))

def compare_titles():
    #compare the titles here with those from boxoffimojo to make sure they match up. make a list of errors
    print("Conflict with the title: {0}".format(title))
    correct_name = input("What should we call the moviebodycount title?: ")
    pass

# ## create final dictionary
# pickled = grab_pickle('movie_body_count_pages.pkl')
# main_dict = read_main_dict()
# temp_dict = {}
# for index, (k, v) in enumerate(main_dict.items()):
#     # if index == 20: break
#     url = v['url']
#     temp_dict[k] = page_parser(url, pickled[url])
# movie_data_saver(temp_dict, "moviebodycounts_final_movie_data.json")
# # cleaning up the final file by hand



# ## begin main dictionary file with urls and titles. save url page data to pickle
# master_dict = movie_links()
# movie_data_saver(master_dict)
# list_of_links = [i for i in master_dict.values()]
# print("\nSour pickle jar: " + str(brine_time(list_of_links, 'movie_body_count_pages.pkl', maxsleep=2)))

# ## single pickle correction
# single_pickle('movie_body_count_pages.pkl')