import requests
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from flask_cors import CORS


# Establishes a connection with Pi Shop website, uses Solenium to load dynamic content 
# and Beautiful Soup to parse for info


def retrieve_item_pi_shop(search_product):

    #initalize webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.page_load_strategy = 'eager'
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)

    base_url = 'https://www.pishop.us/search.php'
    url = f'{base_url}?search_query={search_product.replace(" ", "%20")}&section=product'
    print(url)
    #driver.get(url)

    product_info = []

    #initialize BeautifulSoup, find the div classes of products
    main_page = driver.page_source
    soup = BeautifulSoup(main_page, 'html.parser')
    product_grids = soup.find_all('div', class_= "product-grid product-grid-4 col-lg-3 col-md-4 col-6")
    
    #Scrape the info for first 4 products since those are the most relevant

    for product in product_grids[:4]:
            #right block in Pi Shop contains link to product page and product name
            right_block= product.find('div', class_= "right-block")
            product_title = right_block.find('a').text

            status = right_block.find('div', class_ = 'action-item addToCart').find('a').text

            #Check if the item is actually in stock
            if status == 'Notify Me':
                continue

            #Check if the product title contains the product we are looking for
            #If it doesn't start the next iteration
            if product_title.find(search_product) == -1:
                continue

            product_link = right_block.find('a').get('href')
        
            
            left_block = product.find('div', class_='left-block')
            product_img = left_block.find('img').get('src')
            
           

            product_price = right_block.find('span', class_='price--withoutTax').text
            
            
            try:
                #find scratcher info and add it to list
                product_info.append((product_img, product_title, product_price, product_link))
            except Exception as e:
                print(e)
                continue

    print(product_info)
    return product_info

    driver.close()

def scrape():
     
    information = []

    #Storing all of the infomration for all of the Raspberry Pis in Pi Shop
    information.append(retrieve_item_pi_shop("Raspberry Pi 3"))
    information.append(retrieve_item_pi_shop("Raspberry Pi 4"))
    information.append(retrieve_item_pi_shop("raspberry pi 5"))

    #2 Options: We can send all of the information all at once and let the front end organize, or 
    #we can organize it here and send information multiple times