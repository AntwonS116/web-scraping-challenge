#Dependencies and setup
import pandas as pd 
import time 
from splinter import Browser, driver
from bs4 import BeautifulSoup
from selenium import webdriver

def scrape():
  executable_path = {"executable_path": "chromedriver.exe"}
  browser = Browser("chrome", **executable_path, headless=False)
  mars_dict = {}

  #Mars news 
  url = "https://redplanetscience.com/"
  browser.visit(url)
  html_news = browser.html
  soup = BeautifulSoup(html_news, "html.parser")
  news_title = soup.find("div", class_ = "content_title").text
  news_paragraph = soup.find("div", class_ = "article_teaser_body").text

  #JPL Featured Space Image
  url_spaceimage = ("https://spaceimages-mars.com/")
  browser.visit(url_spaceimage)
  html = browser.html
  soup = BeautifulSoup(html, "html.parser")
  header = soup.find("div", class_ = "header")
  browser.links.find_by_partial_text('FULL IMAGE').click()
  html = browser.html
  soup = BeautifulSoup(html, 'html.parser')
  image_box = soup.find('div', class_='fancybox-inner')
  featured_image_url = url_spaceimage.replace('index.html', '') + image_box.img['src']

  #Mars Facts
  url_facts = "https://galaxyfacts-mars.com/"
  mars_facts = pd.read_html(url_facts)
  mars_facts_df = mars_facts[0]
  mars_facts_df = mars_facts_df.rename(columns={0: "Mars - Earth Comparison", 1: "Mars" , 2: "Earth"})
  mars_facts_df.drop([0, 0,6], axis=0, inplace=True)
  mars_html = mars_facts_df.to_html()
  mars_html = mars_html.replace("\n", "")

  #Mars Hemispheres
  url_hemisphere = "https://marshemispheres.com/"
  browser.visit(url_hemisphere)
  html_hemisphere = browser.html
  soup = BeautifulSoup(html_hemisphere, "html.parser")
  hemispheres = soup.find_all("div", class_="item")
  hemispheres_info = []
  hemispheres_url = "https://marshemispheres.com/"

  for i in hemispheres:
    title = i.find("h3").text
    hemispheres_img = i.find("a", class_="itemLink product-item")["href"]
    browser.visit(hemispheres_url + hemispheres_img)
    image_html = browser.html
    web_info = BeautifulSoup(image_html, "html.parser")
    img_url = hemispheres_url + web_info.find("img", class_="wide-image")["src"]
    hemispheres_info.append({"title" : title, "img_url" : img_url})

  #Create dictionary for everything scraped
  mars_dict = {
    "news_title" : news_title,
    "news_paragraph" : news_paragraph,
    "featured_image_url" : featured_image_url,
    "mars_facts" : mars_html,
    "hemisphere_images" : hemispheres_info
  }

  #Closing the browser
  browser.quit()
  return mars_dict














