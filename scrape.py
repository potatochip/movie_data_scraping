import urllib2
import re
import csv

from bs4 import BeautifulSoup

headers = ["movie title", "domestic total gross", "release date", "runtime", "rating", "data source"]

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

def save_data(datadict):
    with open("boxofficemojo_data.csv", "wb") as csv_file:
        dict_writer = csv.DictWriter(csv_file, headers)
        dict_writer.writeheader()
        dict_writer.writerows(datadict)

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

def page_grabber(base_url="boxofficemojo.com"):
    total_set_of_pages = set()

    total_set_of_pages.add(base_url)
    return total_set_of_pages


url_list = page_grabber("http://www.boxofficemojo.com/movies/?id=biglebowski.htm")
print url_list

#movie_data = [page_parser(url) for url in url_list]
#check whether it is a legitimate movie page before calling page_parser

#save_data(movie_data)