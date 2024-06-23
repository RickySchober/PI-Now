import requests
import re
import time
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from flask_cors import CORS
import os


def retrieve_item_ada_fruit(search_product):

    #initalize webdriver
    option = webdriver.ChromeOptions()
    option.add_argument("start-maximized")
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--incognito')
    option.page_load_strategy = 'eager'
    option.add_argument('--headless=new')
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=option)

    base_url = 'https://www.adafruit.com/search?q='
    url = f'{base_url}{search_product.replace(" ", "%20")}&section=product'
    print(url)
    driver.get(url)

    product_info = []

    #initialize BeautifulSoup, find the div classes of products
    main_page = driver.page_source
    soup = BeautifulSoup(main_page, 'html.parser')
    product_grids = soup.find_all('div', class_= "row product-listing")
    
    #Scrape the info for first 4 products since those are the most relevant
    
    for product in product_grids[:4]:
            
            #right block in Pi Shop contains link to product page and product name
            title_block= product.find('div', class_= "product-listing-right col-lg-9 col-md-9 col-sm-9 col-xs-6")
            
            product_title = title_block.find('a').text

            #Determine whether item is in stock or not
            status = product.find('div', class_ = 'stock').text

            #Remove extra lines from status
            status = os.linesep.join([s for s in status.splitlines() if s])
            print(status)
    
            #If the item isn't a stock skip it
            if status == 'Out of stock' or status == "Coming soon":
                continue

            #Check if the product title contains the product we are looking for
            #If it doesn't start the next iteration
            
            link = product.find('div', class_='product-listing-text-wrapper')

            product_link = link.find('a').get('href')
            #print(product_link)
            product_link = "https://www.adafruit.com" + product_link
            #print(product_link)

           
            product_img = product.find('img').get('src')
            #print(product_img)
            
            product_price = product.find('span', class_='normal-price').text
            
            #remove $
            product_price = product_price.replace("$", "")
            #if int(product_price) < 10: 
                #continue
            print(product_price)
            try:
                #find scratcher info and add it to list
                product_info.append((product_title, product_price, product_img, product_link, "Ada Fruit"))
            except Exception as e:
                print(e)
                continue

    print(product_info)

    driver.close()
    return product_info

# Establishes a connection with Pi Shop website, uses Solenium to load dynamic content 
# and Beautiful Soup to parse for info


def retrieve_item_pi_shop(search_product):

    option = webdriver.ChromeOptions()
    option.add_argument("start-maximized")
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--incognito')
    option.page_load_strategy = 'eager'
    option.add_argument('--headless=new')
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=option)

    base_url = 'https://www.pishop.us/search.php'
    url = f'{base_url}?search_query={search_product.replace(" ", "%20")}&section=product'
    print(url)
    driver.get(url)

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

            print(product_title)

            status = right_block.find('div', class_ = 'action-item addToCart')
            if status is None:
                 continue
            
            status =status.find('a').text

            print(status)
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
            
           #pi_now23

            product_price = right_block.find('span', class_='price--withoutTax').text
            
            #remove $
            product_price = product_price.replace("$", "")

            try:
                #find scratcher info and add it to list
                product_info.append((product_title, product_price, product_img, product_link, "Pi Shop"))
            except Exception as e:
                print(e)
                continue

    print(product_info)

    driver.close()
    return product_info



def scrape():
     
    #information = [('Raspberry Pi 4 Model B/4GB', '55.00', 'https://cdn11.bigcommerce.com/s-2fbyfnm8ev/images/stencil/300x300/products/641/2349/4GB-9004__53667.1560436241__58682.1561146139.jpg?c=2', 'https://www.pishop.us/product/raspberry-pi-4-model-b-4gb/', 'Pi Shop'), ('Raspberry Pi 4 Desktop Kit US - 8GB', '140.00', 'https://cdn11.bigcommerce.com/s-2fbyfnm8ev/images/stencil/300x300/products/944/3334/8GB_desktop__34274.1590607488.jpg?c=2', 'https://www.pishop.us/product/raspberry-pi-4-desktop-kit-us-8gb/', 'Pi Shop')]
    information = []
    info = retrieve_item_pi_shop("Raspberry Pi 3")
    if info:   information.append(info)
    info = retrieve_item_pi_shop("Raspberry Pi 4")
    if info:   information.append(info)
    info = retrieve_item_pi_shop("Raspberry Pi 5")
    if info:   information.append(info)
    info = retrieve_item_ada_fruit("Raspberry Pi 3")
    if info:   information.append(info)
    info = retrieve_item_ada_fruit("Raspberry Pi 4")
    if info:   information.append(info)

    info = retrieve_item_ada_fruit("Raspberry Pi 5")
    if info:   information.append(info)
    #Storing all of the infomration for all of the Raspberry Pis in Pi Shop
    #information now holds all the info

    #jsonify(information, 200)

#scrape()