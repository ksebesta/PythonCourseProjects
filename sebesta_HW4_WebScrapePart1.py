'''
Title: sebesta_HW4_WebScarpePart1.py
Author: Kalea Sebesta
Date: 12/3/2017
Purpose: PART 1

Write a Python script that will scrape Craig’s List for items for sale of
a type you specify from a city you select, other than San Antonio.
Expectations:
1) You may hard-code the item type and city.
   You may not knowingly pick the same city and item as another student.
2) You must scrape the date the item was posted to Craig’s list, its location,
   the full description of the item, and its price.
3) All items for sale on the page must be included in your output, even if
   some of the attributes are not provided (i.e. an item for sale does not
   include a location).
4) The script must write all scraped data in a nicely formatted CSV file, having
   a descriptive header row and properly delimited data/columns.
'''
# ------------------------------------------------------------------------------
#Basic Scrapper
from urllib.request import urlopen as uReg
from bs4 import BeautifulSoup as soup

# ------------------------------------------------------------------------------
# 1) Hard code item type and city
my_url='https://honolulu.craigslist.org/search/oah/bia'
# ------------------------------------------------------------------------------
# 2) Scrape the date the item was posted
#sends GET request to URL
uClient=uReg(my_url)
#reads returned data and puts it in a variable
page_html=uClient.read()
#close the connection
uClient.close()

# create discriptive header rows
fileName="sebesta_HW4_ScrapedData.csv"
f=open(fileName, "w")
headers="Date,Location,Description,Price\n"
f.write(headers)

#use Beautifulsoup to parse the webpage
page_soup=soup(page_html, "html.parser")
containers=page_soup.findAll("time", {"class", "result-date"})

i=0
location=[]
description=[]
price=[]
loc=[]

#pages = page_soup.findAll("span", {"class", "totalcount"})
#total_pages=pages[0].text
#for page in total_pages:

for i in range(len(containers)):
    # --------------------------------------------------------------------------
    # Scrape the item's location
    containers_location = page_soup.findAll("span", {"class", "result-meta"})
    loc = containers_location[i].findNext('span',{'class':'result-hood'})

    # checks to see if there is a location for that item,
    # if so it appends it to the list if not it appends a blank
    # I think my logic is off on this because there should be more blank locations
    if loc is not None:
        location.append(loc.text.strip())
    else:
        location.append('')
    # -------------------------------------------------------------------------
    # Scrape the item's full description
    containers_description=page_soup.findAll("a", {"class", "result-title hdrlnk"})
    description.append(containers_description[i].text)
    # -------------------------------------------------------------------------
    # Scrape the items price
    containers_price = page_soup.findAll("span", {"class": "result-meta"})
    con_price = containers_price[i].findNext('span',{'class':'result-price'})
    price.append(con_price.text)

# ------------------------------------------------------------------------------
    # Write al scraped data in csv file
    f.write(containers[i].text+','+location[i] + ',' + description[i].replace(",",":") + ',' + price[i] + '\n')
f.close()
# ------------------------------------------------------------------------------