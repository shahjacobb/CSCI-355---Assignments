"""
Queens College
CSCI 355 - Internet and Web Technologies
Winter 2024
Assignment 4
Shah Bhuiyan
Worked with the class, again!
"""

# [1] import necessary modules

from bs4 import BeautifulSoup
import requests
import html5lib
from Assignment3 import OutputUtils as ou

# [2] Define a function that prints the HTML content of a web page
def get_page_content(url):
    response = requests.get(url)
    print(response.content)

# [3] Define a function to parse the HTML content for a given URL.
def parse_page_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html5lib")
    print(soup.prettify())

# [4] Define a function to get the next text item from an iterator
def next_text(itr):
    return next(itr).text

# [5] Define a function to get the next int item from an iterator
def next_int(itr):
    return int(next_text(itr).replace(',', ''))

#  [6] Define a function to scrape the site.
def covid_scraper(dict_countries_population):
    url = 'https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'
    # get URL html
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    data = []
    itr = iter(soup.find_all('td'))
    while True:
        try:
            country = next_text(itr)
            cases = next_int(itr)
            deaths = next_int(itr)
            continent = next_text(itr)
            if country.startswith("Japan"):
                country = "Japan"
            if country in ["Channel Islands", "MS Zaandam"]:
                continue
            population = dict_countries_population[country]


            percent_cases = round(100 * cases/population)
            percent_deaths = round(100 * deaths/population)
            data.append([country,continent, population, cases, percent_cases, deaths, percent_deaths])
        except StopIteration:
            break

    return data
"""
[7] Define a function get_country_population(url) that will scrape this website to get country populations: https://www.worldometers.info/world-population/population-by-country/. 
Build a dictionary in which the keys are country names and the values are country populations.
"""

def get_country_population():
    url = 'https://www.worldometers.info/world-population/population-by-country/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    itr = iter(soup.find_all('td'))
    dict_countries = {}
    while True:
        try:
            no = next_text(itr)
            country = next_text(itr)
            population = next_int(itr)
            for i in range(9):
                junk = next_text(itr)
            dict_countries[country] = population
            print(country, population)
        except StopIteration:
            break
    return dict_countries

# a function that adds a hyperlink to the corresponding wikipedia page of that country

def add_wiki_link(data, i, j):
    name = data[i][j]
    wikiname = name
    if wikiname == "Australia/Oceania":
        wikiname = "Australia"
    href = "https://en.wikipedia.org/" + wikiname.replace(" ", "_")
    a_attributes = "href = '" + href + "' target = 'blank'"
    data[i][j] = ou.create_element(ou.TAG_A, name, a_attributes)

def make_html(data, assn):
    title = "COVID Data by Country"
    align = ["L", "L", "R", "R", "R", "R", "R"]
    types = ["S", "S", "N", "N", "N", "N", "N"]
    heads = ["Country", "Continent", "Population", "Cases", "Pct Cases", "Deaths", "Pct Deaths"]
    output_file = "Assignment4.html"
    ou.write_tt_file(assn + ".txt", title, heads, data, align)
    ou.write_csv_file(assn + ".csv", heads, data)
    ou.write_xml_file(assn + ".xml", title, heads, data, True)
    x_label, y_label = "Population", "Cases"
    x_data = [data[i][2] for i in range(len(data))]
    y_data = [data[i][3] for i in range(len(data))]
    x_ticks = [i * 1000000 for i in range(50)]
    y_ticks = [i * 1000000 for i in range(50)]
    for i in range(len(data)):
        add_wiki_link(data, i, 0)
        add_wiki_link(data, i, 1)
    ou.add_stats(data, [2,3,4,5,6], 0, 1, True)
    ou.write_html_file(output_file, title, heads, types, align, data, open_file=True)

def add_wiki_link(data, i, j):
    name = data[i][j]
    wikiname = name
    if wikiname == 'Australia/Oceania':
        wikiname = 'Australia'
    href = "https://en.wikipedia.org/wiki/" + wikiname.replace(' ', '_')
    a_attributes = 'href="' + href + '" target="_blank"'
    data[i][j] = ou.create_element(ou.TAG_A, name, a_attributes)

# [9] Define a function to write the data in a text table. Don't hard code values - pass parameters
def write_text_table(data):
    ou.write_tt_file("Assignment 4.txt")


def main():
    dict_countries_population  =  get_country_population()
    data = covid_scraper(dict_countries_population)
    make_html(data, "Assignment4")

if __name__ == "__main__":
    main()