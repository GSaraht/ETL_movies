#Genre
from bs4 import BeautifulSoup
import requests
import csv
from pandas import *
import re

# reading CSV file
data = read_csv("bechdel_dirty.csv")

# converting column data to list
ltitle = data['title'].tolist()
test = ltitle[2:5]

with open ("genre_test.csv", "w", encoding = "utf-8", newline='') as csv_file: # create a new csv file
    csv_writer = csv.writer(csv_file)                                         # create the csv writer
    csv_writer.writerow(["title", "genre"])           # write rows to the csv file

    for title in test:                        # loop through each movie on bechdel page
        print(title.encode('utf-8'))

        no_space_title = title.replace(" ", "+")          # replace " " in title with + so url works

        url = 'https://www.boxofficemojo.com/search/?q={x}'.format(x=no_space_title)
        source = requests.get(url).text                   # get the website
        soup = BeautifulSoup(source, 'lxml')

        #INTERMEDIATE SEARCH RESULTS
        no_results = soup.find("div", class_="a-section mojo-gutter")  # check if there are any results on page
        no_search = soup.h1  # check if the search is valid
        # If search is invalid then pass
        if "No results found" in str(no_results) or "No Search Entered" in str(no_search):
            pass

        # If search is valid continue
        else:
            first_title = soup.find("a", class_="a-size-medium a-link-normal a-text-bold").text #find the movie title

        # if search result is exactly the same as the title entered in the search, continue, else pass
            if title == first_title:
                try:
                    span = soup.find("div", class_ = "a-fixed-left-grid-col a-col-right")   #find section containing info
                    genre = list(span.stripped_strings)[2]      #outerHTML <br> text <br>
                except IndexError:
                    genre = "no genre given"
            else:
                genre = "movie not found"


            # write results to csv
            csv_writer.writerow([title, genre])



