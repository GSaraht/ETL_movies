from bs4 import BeautifulSoup
import requests
import csv
from pandas import *
import time
import re

#reading Kim's bechdel movies CSV file
data = read_csv("bechdel_dirty.csv")

#converting column data to list
ltitle = data['title'].tolist()
tlist = ltitle[1:5]             #defining a test list

with open("Cineman_rating_scrape_test.csv", "w", encoding="utf-8", newline='') as csv_file:  #create a new csv file
    csv_writer = csv.writer(csv_file)                       #create the csv writer
    csv_writer.writerow(['title', 'review_by_cineman', 'cineman_movie_charts']) #write rows to the csv file
    n = 0       #iteration starts from 0 on                                                          

    for title in tlist:  #loop through each movie on bechdel movies
        print(title)
        n = n+1             #next row in csv file
        print(n)
        if n > 50:          #after each 50 rows there is a
            time.sleep(20)  #delay for 20s
            n = 0           #the iteration starts from 0 again to have after each 50 rows a delay or else it would not enter the time.sleep
        else:
            pass

        no_space_title = title.replace(" ", "+")  # replace " " in title with + so url works
        #### START SEARCHING the Movie
        search_url = 'https://www.cineman.ch/en/finder/movie/?q={x}'.format(x=no_space_title)  #get search url
        search_source = requests.get(search_url).text                                          #get the whole html file
        search_soup = BeautifulSoup(search_source, 'lxml')                                     #pass in html file to BeautifulSoup
        n = n + 1           #add 1 to get to the next row

        ####INTERMEDIATE RESEARCH Results
        try:
            movie_title = search_soup.find("div", class_="col-xs-8").h4.text.strip()    #check(find) if "results movies: XX" and movie title exist
            print(movie_title)
        except AttributeError:                                                          #if not then write the exception
            review_by_cineman = "couldn't find movie"

        if movie_title == title:        #check if title in cineman and csv are the same
            print("yes")
            movie_link = search_soup.find("div", class_="col-xs-8").a["href"]   #find the movie link which is in the movie title
            rating_url = "https://www.cineman.ch{x}".format(x=movie_link)       #attach the movie_link at the end of the Cineman url
            print(rating_url)
            rating_source = requests.get(rating_url).text               #get the whole html file
            rating_soup = BeautifulSoup(rating_source, 'lxml')          #pass in html file to BeautifulSoup

            #### MOVIE PAGE
            try:
                review_by_cineman = rating_soup.find("strong", class_="color-cineman").text.strip() #find the first rating in text
                print("foundrating")
            except AttributeError:              #if not available write the exception
                review_by_cineman = "no score"

            try:
                cineman_movie_charts = rating_soup.find("strong", class_="color-playstation").text.strip()  #find the second rating in text
                print("foundrating")
            except AttributeError:
                cineman_movie_charts = "no score"

        else:                                           #if title in cineman and movies.csv are not the same (line 44) go into the else section
            review_by_cineman = "couldn't find movie1"
            cineman_movie_charts = "couldn't find movie1"

        csv_writer.writerow([title, review_by_cineman, cineman_movie_charts])
    

