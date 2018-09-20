from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import pymongo
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    browser = init_browser()
    mars_data = {}

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    news_html = browser.html
    news_soup = BeautifulSoup(news_html, 'html.parser')

    news_title = news_soup.find("div", class_="content_title").text
    mars_data["news_title"] = news_title
    
    news_p = news_soup.find("div", class_="rollover_description_inner").text
    mars_data["news_p"] = news_p

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')

    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')

    article = image_soup.find("article")
    source = article.find("figure", class_="lede").a["href"]
    base_url = "https://www.jpl.nasa.gov"
    featured_image_url = base_url + source

    mars_data["featured_image_url"] = featured_image_url

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    weather_html = browser.html
    weather_soup = BeautifulSoup(weather_html, 'html.parser')

    mars_weather = weather_soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_data["mars_weather"] = mars_weather

    facts_url = 'http://space-facts.com/mars/'

    tables = pd.read_html(facts_url)
    df = tables[0]
    df.columns = ["Key", "Value"]
    df.set_index("Key", inplace=True)
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')
    mars_data["html_table"] = html_table

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    hemisphere_image_urls = []
    
    browser.click_link_by_partial_text('Cerberus')
    Cerberus_html = browser.html
    Cerberus_soup = BeautifulSoup(Cerberus_html, 'html.parser')
    Cerberus_image = Cerberus_soup.find("div", class_="downloads").a["href"]
    hemisphere_image_urls.append({"title": "Cerberus Hemisphere", "img_url": Cerberus_image})

    browser.click_link_by_partial_text('Schiaparelli')
    Schiaparelli_html = browser.html
    Schiaparelli_soup = BeautifulSoup(Schiaparelli_html, 'html.parser')
    Schiaparelli_image = Schiaparelli_soup.find("div", class_="downloads").a["href"]
    hemisphere_image_urls.append({"title": "Schiaparelli Hemisphere", "img_url": Schiaparelli_image})

    browser.click_link_by_partial_text('Syrtis Major')
    Syrtis_Major_html = browser.html
    Syrtis_Major_soup = BeautifulSoup(Syrtis_Major_html, 'html.parser')
    Syrtis_Major_image = Syrtis_Major_soup.find("div", class_="downloads").a["href"]
    hemisphere_image_urls.append({"title": "Syrtis Major Hemisphere", "img_url": Syrtis_Major_image})

    browser.click_link_by_partial_text('Valles Marineris')
    Valles_Marineris_html = browser.html
    Valles_Marineris_soup = BeautifulSoup(Valles_Marineris_html, 'html.parser')
    Valles_Marineris_image = Valles_Marineris_soup.find("div", class_="downloads").a["href"]
    hemisphere_image_urls.append({"title": "Valles Marineris Hemisphere", "img_url": Valles_Marineris_image})

    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    return mars_data