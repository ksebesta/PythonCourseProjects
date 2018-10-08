'''
Title: sebesta_HW4_WebScrapePart2.py
Comments Authored by: Kalea Sebesta
Date: 12/4/2017
Purpose: PART 2
'''

"""
Created on Wed Nov 30 @way too late in th evening O'clock 2017

@author: Eric
"""
# INSTRUCTIONS: In the code below you will find each code
# section has either a "BONUS" or a "REQUIRED" comment tag
# at the front. If it has a "REQUIRED" comment tag, then it is
# part of the homework assignment and you must provide comments
# interpretting that portion of the code. Ideal comments will
# indicate what the code is for and, if it is a function, what
# the function does, what it takes in as input (if anything) and what
# it provides as output (if anything)
# The "BONUS" sections carry the same comment requirements but
# are NOT REQUIRED for a full score...however, they allow for
# extra points. The "BONUS" sections are ones you may not be familiar with.
# HINT: duckduckgo.com is YOUR FRIEND, there is NO SHAME in using
# any resources available to you to UNDERSTAND something.

# REQUIRED
#urllib.request is a package that allows you to change the headers and agent and
# appear as real web browser which allows you to crawl easier
import urllib.request
#urllib.parse is a package that has features which allow you to parse the url for
# desired information, for example the path, map, location, and other fragments
import urllib.parse
#beautifulSoup is a package that can handle the nonsense of html and interprete it
# while allowing the user to understand and analyze the content within
from bs4 import BeautifulSoup
#re stands for regular expressions and is a package that allows you to use re to
# parse through and grab specific data
import re

# BONUS
# comment is an element that is handled with beautiful soup (the html document is
# tranformed into a tree of python objects with comment is one of 4 types of objects
from bs4.element import Comment
# uses the ascii_lowercase funcationality to transform letters into lowercase
from string import ascii_lowercase
# the random module provised many functions that support operations dealing with
# creating random things
import random

# REQUIRED
# this function takes in a url, uses the urllib parse package to check whether the network
# location from the url is vaild (meaning that is a valid url which contains a domain name)
# if it is a vaild url then the url is returned otherwise it takes the start and combines it
# with the unvaild (fragmented) url that was provided.
def ensure_absolute(url):
    if bool(urllib.parse.urlparse(url).netloc):    
        return url
    else:
        return urllib.parse.urljoin(start,url)

# REQUIRED
# this function takes in urlw and creates an empty list. it then finds the start network
# location and sets that to represent the basenet location. from there the each url in
# the urls is looped through and the url is checked to see if it is valid then extracts
# the path, netloc, query, fragment, and parma from the url. if the netloc is the same
# as the basenet location and wiki is in the path and query, fragment, and param are empty
# then the url is added to the list. this function returns the list of urls
def ensure_urls_good(urls):
    result = []
    basenetloc = urllib.parse.urlparse(start).netloc
    for url in urls:
        url = ensure_absolute(url)
        path = urllib.parse.urlparse(url).path
        netloc = urllib.parse.urlparse(url).netloc
        query = urllib.parse.urlparse(url).query
        fragment = urllib.parse.urlparse(url).fragment
        param = urllib.parse.urlparse(url).params
        if (netloc == basenetloc and re.match(r'^/wiki/', path) and query == '' and fragment == '' and param == ''):
            result += [url]
    return result

# REQUIRED
# this function passes in a url, then sets the header with a specific common user agent,
# it then is sent as a request (GET). the responding html page is read and the user
# connection is closed. then the html page is soupified using beautifulsoup, both the
# parsed soupified page and the original html page are returned from this function
def getsource(url):
    req=urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}) #sends GET request to URL
    uClient=urllib.request.urlopen(req)
    page_html=uClient.read() #reads returned data and puts it in a variable
    uClient.close() #close the connection
    page_soup=BeautifulSoup(page_html,"html.parser")
    return [page_soup, page_html]

# REQUIRED
# this function takes in a page that has been soupified. an empty list that will
# hold the results is initialized. for each anchor in the page that has a div
# with id=bodycontent get the link from the anchor and append it to the result list
# then test the url to make sure it is a vaild url then return the list of urls found
def getanchors(pagesoup):
    result = []
    for anchor in pagesoup.find('div', {"id":'bodyContent'}).findAll('a'):
        result += [anchor.get('href')]
    result = ensure_urls_good(result)
    return result

# BONUS
# this function determinds if an element has a visible tag.
# it looks at the elements parent name and if the element is
# in a comment in either case they return false otherwise it
# is considered a visible tag
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# BONUS
# this function is given the original html page and pasrses it using beautiful
# soup and then filters just the visible tags in the texts. the function returns
# the tag striped of whitespace
def text_from_html(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

# BONUS
# this function initialized a dictionary for the letters of the alphabet.
# is uses the ascii_lowercase identification to place letters of the text
# into the dictionary and the counts of the letters as the values in the dictionary
def count_letters(texts):
    alphabet = {}
    for letter in ascii_lowercase:
        alphabet[letter] = texts.count(letter)
    return alphabet

# BONUS
# this function counts the ngrams in a text and is passed the text and the
# desired number of characters. then it looks for the pattern at least one
# alphanumeric string or a string with either upper or lower case letters
# then an apostrophy zero or one time followed by at least one or more lower
# or uppercase letters. then for every match of that pattern in the texts,
# check to see the length of the grams list, if the list is less then the n
# passed through as a parameter then appened the matched group of 1 to the
# grams list, else combine the grams to create teh ngram variable and
# increment it. grams list gets all the grams from row 1 and all the columns
# and then the match of the group of 1 is appened to the list. the final grams
# list is returned from the function
def count_ngrams(texts, n):
    ngrams = {}
    grams = []
    pattern = re.compile(r'\[\w+\]|([a-zA-Z]+\'{0,1}[a-zA-Z]+)')
    for m in re.finditer(pattern, texts):
        if (str(m.group(1)) != 'None'):
            if (len(grams) < n):
                grams += [m.group(1)]
            else:
                ngram = ' '.join(grams);
                if (ngram in ngrams):
                    ngrams[ngram] = ngrams[ngram]+1
                else:
                    ngrams[ngram] = 1
                grams = grams[1:]
                grams += [m.group(1)]
    return ngrams

# BONUS
# this function is given two dictionaries and combinds them into one dictionary
# which is returned from the function. for each key in dictionary 1 and 2 they are
# combined into one key
def combinedicts(dict1,dict2):
    result = { k: dict1.get(k, 0) + dict2.get(k, 0) for k in set(dict1) | set(dict2) }
    return result

# REQUIRED
# this function takes in a file name, header, and data to write the data to a csv.
# a file is opened and given writen premissions, the header row is writen to the
# file along with a newline then for each item in the sorted data set, the
# string item from the data and the contents of the data at that specific item is
# writen to the file the file is then closed. nothing is returned from this function.
def write_dict_to_csv(fname,header,data):
    f=open(fname,'w')
    f.write(header)
    f.write('\n')
    for item in sorted(data, key=lambda i: int(data[i]), reverse=True):
        f.write(str(item)+','+str(data[item]))
        f.write('\n')
    f.close()
    return

# REQUIRED
# this function takes in the url and the limit. two dictionaries are
# initialized and page data is grabbed from the url as are the anchors.
# it then begins to crawl. the limit that was passed is the stopping point
# for the crawl. within the crawl random.SystemRandom creates a cryptographically
# secure pseudo-random number it then randomly chooses an anchor and makes
# it the random_url and then gets the data from that html page then it gets the
# text from the html and converts it to all lower case. from there the letter
# frequency is found by counting the letters in the text, it also gets the ngram
# frequencies by counting the ngrams in the text and a specifiying the ngram level
# and then the anchors are gotten again (updating the anchors from the new random url)
# if the length of the result1 dictionary is greater than 1 then combined the
# dictionaries of result1 and letterfrequency. else just the letterfreq is put into
# the results1 dictionary, if the length of the result2 dictionary is greater than
# 1 then combined the dictionaries of result2 and ngramfreq. else just the ngram freq
# is put into the results2 dictionary. both dictionaries are returned from this function.
def crawl(url, limit):
    result1 = {}
    result2 = {}
    pagedata = getsource(url)
    anchors = getanchors(pagedata[0])
    for i in range(0,limit):
        secure_random = random.SystemRandom()
        random_url = secure_random.choice(anchors)
        pagedata = getsource(random_url)
        texts = text_from_html(pagedata[1]).lower()
        letterfreqs = count_letters(texts)
        ngramfreqs = count_ngrams(texts, desired_ngram_level)
        anchors = getanchors(pagedata[0])
        if len(result1) > 1:
            result1 = combinedicts(result1,letterfreqs)
        else:
            result1 = letterfreqs
        if len(result2) > 1:
            result2 = combinedicts(result2,ngramfreqs)
        else:
            result2 = ngramfreqs
    return [result1, result2]

# REQUIRED
# assigns the start variable to hold a specific url
start="https://en.wikipedia.org/wiki/Special:Random"

# REQUIRED
# assigns the pagetocrawl as 20 (desired page to start the crawl at)
pagestocrawl = 20

# BONUS
# sets the ngram level as 2 meaning it sets the class that supports lookup
# by a 2-gram (2 being the number of characters per ngram) string similarity
desired_ngram_level = 2

# REQUIRED
# calls the crawl function and passes the starting url and the page to start
# crawling at. it then returns the dictionaries to the variable freqs and writes
# the information to a csv file
freqs = crawl(start,pagestocrawl)
write_dict_to_csv('letter_freqs.csv','letter,frequency',freqs[0])
write_dict_to_csv('ngram_freqs.csv','ngram,frequency',freqs[1])


