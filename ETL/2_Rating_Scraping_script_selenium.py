from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import selenium
import time
import pandas as pd
import csv

"""To run the code with a visible browser please go to line 32 and change it to False. Then activate the following:
Line 42 remove the # to be able to skip the ads
Line 54 - 57 also remove # to skip ads
Line 68 - 71 remove # to skip ads """


# reading CSV file
data = pd.read_csv("bechdel_dirty.csv")

# converting column data to list
ltitle = data['title'].tolist()
test = ltitle[2:3]


with open ("rating_seleniumIV2.csv", "w", encoding = "utf-8", newline='') as csv_file: # create a new csv file
    csv_writer = csv.writer(csv_file)                                         # create the csv writer
    csv_writer.writerow(['moviename', 'review_cineman',  'review_moviechart'])  # write rows to the csv file 

    url ='https://www.cineman.ch/en/finder/?q='     #search page on Cineman

    for title in test:
        movie_found = True  #At the beginning of each loop the movie exists

        opts = Options()
        opts.headless =True                     #to run the code without browser
        driver = webdriver.Chrome(options=opts) 
        driver.get(url)              

        time.sleep(3)   #delay to fully load website

        #accept cookies on chrome 
        cookie = driver.find_element(By.XPATH, '/html/body/div[1]/div/a')  #search accept button
        #skip commercial
        #ads = driver.find_element(By.XPATH, '//*[@id="welcomeModal"]/div/div/div[1]/h4/a') #search continue button

        #if cookie thing appears accept it if it does not appear pass
        try:
            cookie.click()
        except:
            pass
        
        #if ad appears accept it if not pass
        #it is commented because it is not necessary with the headless browser
        #try:
        #    ads.click()
        #except:
        #    pass

        #find search field        
        movietitle = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div[1]/div/form/div/div[1]/input')   
        movietitle.click()                  #click on search field
        time.sleep(1)                       #delay 1s
        movietitle.send_keys(title)         #enter movie title 
        time.sleep(1)                       #add a 1s delay

        #if random ad appears continue to Cineman
        #it is commented because it is not necessary with the headless browser
        #try:
        #    ads.click()
        #except:
        #    pass

        #Find search button to click on it
        searchmt = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div[1]/div/form/div/div[2]/button') 
        searchmt.click()    # click on it       
        time.sleep(1)       #add 1s delay                        

        ######  Try find INTERMEDIATE search result if there are none, pass
        try:
            driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div[1]/div/div/h3') #find the class containing "result movies"
        except NoSuchElementException:          #if not available enter exception
            moviename = title
            review_cineman = 'no cineman review'
            review_moviechart = 'no movie chart review'
            movie_found = False                 #movie is not found

        if movie_found:         #if movie is found
            #First find movie title and then find movie title link
            resulttitle = driver.find_element(By.XPATH,'/html/body/div[2]/div/main/div[1]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/a/h4').text
            resulttitle_link = driver.find_element(By.XPATH,'/html/body/div[2]/div/main/div[1]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/a') 

            #if movie equals the movie title in test list (line 16) then 
            if resulttitle == title:
                resulttitle_link.click()        #click on movie title link
                time.sleep(2)                   #delay 5s for random ads
                
                #Find movie title
                try:
                    moviename = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div[1]/section/div[1]/div[4]/div[1]/div/div[1]/h1/span').text
                except NoSuchElementException:
                    pass

                #Find review by cineman
                try:
                    review_cineman = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div[1]/section/div[1]/div[4]/div[4]/div[1]/div[1]/h4/em/a/strong').text
                except NoSuchElementException:
                    pass
                    
                #Find review by movie chart
                try:
                    review_moviechart = driver.find_element(By.CSS_SELECTOR, '.color-playstation').text    
                except NoSuchElementException:
                    pass

            else:       #If movie title (line 83) cannot be found enter else
                moviename = title
                review_cineman = 'no cineman review'
                review_moviechart = 'no movie chart review'


        csv_writer.writerow([moviename, review_cineman,  review_moviechart])







