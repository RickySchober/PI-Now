import requests
import re
import time
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from flask_cors import CORS
from mysql.connector import MySQLConnection, Error
import os

import mysql.connector

def retrieve_item_ada_fruit(search_product):

    #initalize webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.page_load_strategy = 'eager'
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)

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


def flatten_information(information):
    # Flatten the nested list of tuples
    flat_information = [item for sublist in information for item in sublist]
    return flat_information


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
  
    

    #2 Options: We can send all of the information all at once and let the front end organize, or 
    #we can organize it here and send information multiple times


    cnx = mysql.connector.connect(
            host='localhost',
            user='root',
            password='pi_now23',
            database='pi_now'
    )
    information = [[('Raspberry Pi 3 – Model A+ (PLUS) - 512MB RAM', '25.00', 'https://cdn11.bigcommerce.com/s-2fbyfnm8ev/images/stencil/300x300/products/437/1726/2063_3__64258.1546973813.jpg?c=2', 'https://www.pishop.us/product/raspberry-pi-3-model-a-plus-512mb-ram/', 'Pi Shop')], [('Raspberry Pi 4 Model B/4GB', '55.00', 'https://cdn11.bigcommerce.com/s-2fbyfnm8ev/images/stencil/300x300/products/641/2349/4GB-9004__53667.1560436241__58682.1561146139.jpg?c=2', 'https://www.pishop.us/product/raspberry-pi-4-model-b-4gb/', 'Pi Shop')], [('\nAluminum Heat Sink for Raspberry Pi 3 - 14 x 14 x 8mm', '1.50', 'https://cdn-shop.adafruit.com/310x233/3083-00.jpg', 'https://www.adafruit.com/product/3083', 'Ada Fruit')], [('\nRaspberry Pi 4 Model B - 2 GB RAM', '45.00', 'https://cdn-shop.adafruit.com/310x233/4292-03.jpg', 'https://www.adafruit.com/product/4292', 'Ada Fruit'), ('\nRaspberry Pi 4 Model B - 4 GB RAM', '55.00', 'https://cdn-shop.adafruit.com/310x233/4296-11.jpg', 'https://www.adafruit.com/product/4296', 'Ada Fruit')]]
    #print(information)

        
    if cnx.is_connected():
        print('Connected to MySQL server')

    # Create a cursor object
    cursor = cnx.cursor()

    #empty the table befor adding
    sql = "TRUNCATE raspberry_pi;"

    cursor.execute(sql)
    cnx.commit()
    # Flatten the information list
    information = flatten_information(information)

    sql = "INSERT INTO raspberry_pi (name, price, img_url, product_url, shop_name) " \
      "VALUES (%s, %s, %s, %s, %s) " \
      "ON DUPLICATE KEY UPDATE price = VALUES(price), " \
      "product_url = VALUES(product_url), " \
      "img_url = VALUES(img_url)"
    
    cursor.executemany(sql, information)
    
    cnx.commit()

    cursor.close()
    cnx.close() 

def get_pis():

    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='pi_now23',
        database='pi_now'
    )
        
    # Create a cursor object
    cursor = cnx.cursor()
        
    # Execute a SELECT query to fetch data from the table
    query = "SELECT * FROM raspberry_pi"
    cursor.execute(query)
        
    # Fetch all rows of the result
    rows = cursor.fetchall()
        
    # Convert the rows to a list of dictionaries
    data = []
    for row in rows:
        data.append({
            'name': row[0],
            'price': row[1],
            'img_url': row[2],
            'product_url': row[3],
            'shop_name': row[4],
        })
        
    # Close the cursor and connection
    cursor.close()
    cnx.close()

    print(data)
        
    # Return the data as JSON
    return jsonify(data), 200

    


scrape()