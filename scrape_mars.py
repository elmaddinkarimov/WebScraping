# Import Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 

# Initialize browser
def init_browser(): 
  
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', headless=False, **executable_path)

# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# NASA MARS NEWS
def scrape_mars_news(): 
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')


    # Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find('div', class_='content_title').find('a').text.strip()
    news_p = soup.find('div', class_='article_teaser_body').text.strip()

    # Dictionary entry from MARS NEWS
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_p

    return mars_info

    

# FEATURED IMAGE
def scrape_mars_image(): 
    browser = init_browser()
    image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url_featured)
        
    html_image = browser.html

    soup = BeautifulSoup(html_image, 'html.parser')

    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website Url 
    main_url = 'https://www.jpl.nasa.gov'

    # Concatenate website url with scrapped route
    featured_image_url = main_url + featured_image_url

    # Display full link to featured image
    featured_image_url 

    # Dictionary entry from FEATURED IMAGE
    mars_info['featured_image_url'] = featured_image_url 
        
    return mars_info
        

# Mars Weather 
def scrape_mars_weather():
    browser = init_browser()
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    html_weather = browser.html

    soup = BeautifulSoup(html_weather, 'html.parser')

    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

    for tweet in latest_tweets: 
        weather_tweet = tweet.find('p').text
        if 'Sol' and 'pressure' in weather_tweet:
            print(weather_tweet)
            break
        else: 
            pass

    # Dictionary entry from WEATHER TWEET
    mars_info['weather_tweet'] = weather_tweet
        
    return mars_info
  


# Mars Facts
def scrape_mars_facts():
 
    facts_url = 'http://space-facts.com/mars/'

    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    data = mars_df.to_html()

    # Dictionary entry from MARS FACTS
    mars_info['mars_facts'] = data

    return mars_info


# MARS HEMISPHERES


def scrape_mars_hemispheres():
    browser = init_browser() 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    html_hemispheres = browser.html

    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hiu = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov' 

    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
            
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
            
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
            
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
            
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
        # Append the retreived information into a list of dictionaries 
        hiu.append({"title" : title, "img_url" : img_url})

    mars_info['hiu'] = hiu

        
    # Return mars_data dictionary 

    return mars_info