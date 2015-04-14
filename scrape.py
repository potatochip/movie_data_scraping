import urllib2
import re
import json
from pprint import pprint

from bs4 import BeautifulSoup, SoupStrainer

base_url="http://www.boxofficemojo.com"
category_url="/movies/alphabetical.htm?letter="
categories= ["NUM"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
page_url="&page="
sub_pages=range(1, 16)

def link_data_saver(linklist):
    with open("boxofficemojo_link_data.txt", "wb") as txt_file:
        for item in linklist: 
            txt_file.write(item.encode("UTF-8"))
            txt_file.write("\n")

def movie_data_saver(datadict):
    with open("boxofficemojo_movie_data.json", "wb") as json_file:
        newData = json.dumps(datadict, sort_keys=True, indent=4) 
        json_file.write(newData) 

def list_splitter(list, size=7):
    return[ list[i:i+size] for i  in range(0, len(list), size) ]

def link_grabber(url):
    '''
    grabs all the movie links from a page and returns a dictionary of them along with additional info
    '''
    link_dict = {}
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    header_row = soup.find(text=re.compile('Title')).parent.parent
    all_rows = soup.find(text=re.compile('Title')).parent.parent.find_all_next('td')
    row_font_values = [i.font for i in all_rows][4:-28]

    happy_list = list_splitter(row_font_values)
    for item in happy_list:
        link = item[0].find('a')['href']
        title = item[0].string
        studio = item[1].string
        total_gross = item[2].string
        total_theaters = item[3].string
        opening_gross = item[4].string
        opening_theaters = item[5].string
        opening_date = item[6].string
        link_dict.update({title: {"url": base_url + link, "title":title, "studio":studio, "total gross":total_gross, "total theaters":total_theaters, "opening gross": opening_gross, "opening theaters":opening_theaters, "opening date":opening_date}})
    return link_dict

def movie_links():
    master_dict = {}
    link_list = []
    for page in [base_url + category_url + letter + page_url + str(number) for number in sub_pages for letter in categories]:
        link_list.append(page)
        print("processing " + page)
        master_dict.update(link_grabber(page))
    link_data_saver(link_list)
    return master_dict

def get_movie_value(soup, field_name):
    """
    takes a string attr of a movie on the page, and returns the string in the next sibling object (the value for that attribute)
    """
    obj = soup.find(text=re.compile(field_name))
    if not obj: return None
    next_sibling = obj.findNextSibling()
    if next_sibling:
        return next_sibling.text
    else: 
        return None

def page_parser(url="http://www.boxofficemojo.com/movies/?id=biglebowski.htm"):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)

    title_string = soup.find('title').text
    title_string.split("(")[0].strip()
    dtg = get_movie_value(soup, "Domestic Total")
    runtime = get_movie_value(soup, "Runtime")
    rating =  get_movie_value(soup, "MPAA Rating")
    release_date = get_movie_value(soup, "Release Date")
    return dict(zip(headers, [title_string, dtg, release_date, runtime, rating, url]))

# testing page parsing
#page_parser("http://www.boxofficemojo.com/movies/?page=main&id=offthelip.htm")

# grab all the movies on site and their initial data plus links to their original pages and correct bad data
temp_dict = movie_links()
print temp_dict
temp_dict['Waiting for "Superman"'] = temp_dict.pop(None)
temp_dict['Waiting for "Superman"']['title'] = 'Waiting for "Superman"'
temp_dict['Offender']['studio'] = 'n/a'
temp_dict['Toy Story 2 (3D)']['studio'] = 'BV'
movie_data_saver(temp_dict)





#new function that has a long list of try/except for individual pages()

# list_of_titles = [i.string for i in soup.find_all('a') if i['href'][:11] == "/movies/?id"]
# list_of_links = [i['href'] for i in soup.find_all('a') if i['href'][:11] == "/movies/?id"]
# full_link = [i for i in soup.find_all('a') if i['href'][:11] == "/movies/?id"]
# alt_full_link = soup.select('a[href^=/movies/?id=]')
# parent_cells = [i.parent.parent.next_sibling.next_sibling for i in soup.find_all('a') if i['href'][:11] == "/movies/?id"]
# siblign_cells = [i.find_next('td').contents for i in soup.find_all('a') if i['href'][:11] == "/movies/?id"]