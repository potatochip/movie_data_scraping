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



def link_grabber(url):
    '''
    grabs all the movie links from a page and returns a dictionary of them along with additional info
    '''
    link_dict = {}
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    for item in soup.find_all('a'):
        if item.has_attr('href'):
            if item['href'][:11] == "/movies/?id":
                full_row = [i.parent.parent.parent for i in soup.find_all('a') if i['href'][:11] == "/movies/?id"]
                #not working. why?
                link = item['href']
                title = item.string
                studio = item.find_next('td').string
                total_gross = item.find_next('td').find_next('td').string
                total_theaters = item.find_next('td').find_next('td').find_next('td').string
                opening_gross = item.find_next('td').find_next('td').find_next('td').find_next('td').string
                opening_theaters = item.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string
                opening_date = item.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string
                link_dict.update({title: {"url": base_url + link, "title":title, "studio":studio, "total gross":total_gross, "total theaters":total_theaters, "opening gross": opening_gross, "opening theaters":opening_theaters, "opening date":opening_date}})
    return link_dict

# list_of_titles = [i.string for i in soup.find_all('a') if i['href'][:11] == "/movies/?id"]
# list_of_links = [i['href'] for i in soup.find_all('a') if i['href'][:11] == "/movies/?id"]
# full_link = [i for i in soup.find_all('a') if i['href'][:11] == "/movies/?id"]
# alt_full_link = soup.select('a[href^=/movies/?id=]')
# parent_cells = [i.parent.parent.next_sibling.next_sibling for i in soup.find_all('a') if i['href'][:11] == "/movies/?id"]
# siblign_cells = [i.find_next('td').contents for i in soup.find_all('a') if i['href'][:11] == "/movies/?id"]

def movie_links():
    master_dict = {}
    link_list = []
    for page in [base_url + category_url + letter + page_url + str(number) for number in sub_pages for letter in categories]:
        link_list.append(page)
        print("processing " + page)
        master_dict.update(link_grabber(page))
    link_data_saver(link_list)
    return master_dict


movie_data_saver(movie_links())

#movie_data = [page_parser(url) for url in url_list]
#check whether it is a legitimate movie page before calling page_parser by whether it begins with /movies
