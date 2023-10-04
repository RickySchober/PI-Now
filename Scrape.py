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

retrieve_item_pi_shop()

def retrieve_item_pi_shop():

    #initalize webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.page_load_strategy = 'eager'
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)

    
    driver.get("https://www.pishop.us/search.php?search_query=raspberry%20pi%204&section=product")

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
            if product_title.find("Raspberry Pi 4") == -1:
                continue

            product_link = right_block.find('a').get('href')

            left_block = product.find('div', class_='left-block')
            print(product_img)
            product_img = left_block.find('img', class_='img-responsive lazyautosizes lazyloaded').get('src')
            print
           

            product_price = right_block.find('a', class_='price-section price-section--withoutTax').find('span', class_='price price--withoutTax').text
            print(product_price)
            try:
                #find scratcher info and add it to list
                product_info.append((product_img, product_title, product_price, product_link))
            except Exception as e:
                print(e)
                continue

    print(product_info)


    driver.close()