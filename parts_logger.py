#########################################################
# Author: Drake Bell
# Last Modified: 10/3/2018
# Description: This program is a simple webscraper that 
# grabs product information from the following sites...
# Adafruit, SparkFun, Digikey, Grainger, and McMaster
# The datapoints it looks for specifically are...
# Link, Item Name, Price, Description, Vendor, Vendor ID
# Manufacturer, Manufacturer ID
# Once it processes a single link, it will write it into
# the data.csv file. 
#########################################################
import re
import requests
import io
import time
import csv
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver

# Enables debug printing
DEBUG = True

# Delay time for scraping (seconds)
# To avoid hammering servers, don't set 
# below 1. (Be NICE!)
DELAY = 1

# Data Dictionary for gathering data points
# Key -> Value pairings
dd = {}

############################################################
# Name: url_parse
# Desc: Takes an entire URL, and parses it to find the
# URL root name.
# Example: 'www.mcmaster.com/blah/101' to 'mcmaster'
############################################################
def url_parse(url):
	try: 
		parsed = re.split('www.|.com|.net|.gov|.edu|.org', url)
		return parsed[1]
	except IndexError:
		return None

############################################################
# Name: process_website
# Desc: This function is as control structure to choose 
# which site to process according to its URL root name. 
# It also has a sleep function which was implemented to be
# courteous when scraping websites. 
############################################################
def process_website(url):
	# Parse the url for website name
	site = url_parse(url)

	# Control to select appropiate website
	if(site == 'adafruit'):
		adafruit(url)
	elif(site == 'sparkfun'):
		sparkfun(url)
	elif(site == 'digikey'):
		digikey(url)
	elif(site == 'grainger'):
		grainger(url)
	elif(site == 'mcmaster'):
		mcmaster(url)
	else:
		print("Invalid website!")

	if(DEBUG):
		print()

	# BE KIND, <(^.-)>!
	time.sleep(DELAY)

############################################################
# Name: url_fetch
# Desc: Given a url, it will attempt to pull that website's
# page source code. Returns the source code, or None if
# something went wrong during retrieval.
############################################################
def url_fetch(url):
	try: 
		with closing(requests.get(url, stream=True)) as resp:
			if is_good_response(resp):
				return resp.content
			else:
				return None
	except RequestException as e:
		print('Error during request! {0} : {1}'.format(url, str(e)))
		return None


############################################################
# Name: is_good_response
# Desc: Simple validation check on the response recieved
# from the url_fetch function.
############################################################
def is_good_response(resp):
	content_type = resp.headers['Content-Type'].lower()
	return (resp.status_code == 200
			and content_type is not None
			and content_type.find('html') > -1)


############################################################
# Name: logger
# Desc: Simple debugging logger. If the global variable
# DEBUG = True, then it will print to stdout the data points
# that this program is trying to scrape for.
############################################################
def logger(s):
	if(DEBUG):
		print(s)


############################################################
# Name: adafruit
# Desc: Pull in desired information from Adafruit's site.
# Please note you need to get the '/product' page
############################################################ 
def adafruit(url):
	response = url_fetch(url)

	# Parser engine on reponse
	html = BeautifulSoup(response, 'html.parser')

	# Link
	dd['Link'] = url

	# Item Name
	iname = html.find('div', {'class':'mobile-product-header'}).contents[1].string
	dd['ItemName'] = iname
	logger("Name: " + iname)
	
	# Price
	price = html.find('div',{'id':'prod-price'}).get_text().strip()
	dd['Price'] = price
	logger("Price: " + price)
	
	# Description
	description = html.find('div', {'id':'description'}).find('p').get_text()

	# Arbitrarily limit number of characters
	# Adafruit's descriptions can be very long
	description = description[0:350]

	dd["Description"] = description
	logger("Description: " + description)
	

############################################################
# Name: sparkfun
# Desc: Pull in desired information from SparkFun's site.
# Please note that you need to get the '/products' page.
############################################################ 
def sparkfun(url):
	response = url_fetch(url)
	html = BeautifulSoup(response, 'html.parser')

	# Link
	dd['Link'] = url
	
	# Item Name
	iname = html.find('div', {'class':'product-title'}).h1.string
	dd['ItemName'] = iname
	logger("Item: " + iname)
	
	# Price
	price = html.find('span', {'itemprop':'price'}).contents[0]
	dd['Price'] = price
	logger("Price: " + price)
	
	# Description
	description = str(html.find('div', {'class':'tab-content'}).find('p').get_text())
	dd['Description'] = description
	logger("Description: " + description)

	
############################################################
# Name: digikey
# Desc: Pull in desired information from Digikey's site. 
# Please note that you need to get the '/product-detail'
# page.  
############################################################ 
def digikey(url):
	response = url_fetch(url)
	html = BeautifulSoup(response, 'html.parser')

	# Link
	dd['Link'] = url

	# Item Name
	iname = html.find('td', {'itemprop':'description'}).string.strip()
	dd['ItemName'] = iname
	logger("Name: " + iname)

	# Price
	price = html.find('span', {'itemprop':'price'}).string.strip()
	dd['Price'] = price
	logger("Price: " + price)

	# Description
	description = html.find('h3', {'itemprop':'description'}).string.strip()
	dd['Description'] = description
	logger("Desc: " + description)

	# Vendor ID
	vid = html.find('td', {'id':'reportPartNumber'}).contents[2].string.strip()
	dd['VendorID'] = vid
	logger("Vendor ID: " + vid)

	# Manufacturer Name
	mname = html.find('span', {'itemprop':'name'}).string.strip()
	dd['Manufacturer'] = mname
	logger("Manufacturer Name: " + mname)

	# Manufacturer ID
	mid = html.find('h1', {'itemprop':'model'}).string.strip()
	dd['ManufacturerID'] = mid
	logger("Manufacturer Id: " + mid)


############################################################
# Name: grainger
# Desc: Pull in desired information from Grainger's site. 
# Please note you need to get the '/product' page.
############################################################ 
def grainger(url):
	response = url_fetch(url)
	html = BeautifulSoup(response, 'html.parser')
	
	# Link
	dd['Link'] = url

	# Item Name
	iname = html.find('h1', {'class':'productName'}).string.strip()
	dd['ItemName'] = iname
	logger("Name: " + iname)
	
	# Price
	price = html.find('span', {'class':'gcprice-value'}).get_text().strip()
	dd['Price'] = price
	logger("Price: " + price)
	
	# Manufacture ID
	mid = html.find('span', {'itemprop':'model'}).string.strip()
	dd['ManufacturerID'] = mid
	logger("Manufacturing Number: " + mid)


############################################################
# Name: mcmaster
# Desc: Pull in desired information from McMaster's site.
# McMaster is the only website that requires the Selenium
# driver to forcibly grab the HTML.
# Please note you need to be on the 'product detail page.
############################################################ 
def mcmaster(url):
	# Selenium setup (Relative Pathing)
	driver = webdriver.Chrome('chromedriver/chromedriver.exe')
	
	# Load up browser, and navigate to the desired page
	driver.get(url)
	
	# Wait for javascript to populate html
	time.sleep(2)

	# Retrieve page's html
	response = driver.page_source
	html = BeautifulSoup(response, 'html.parser')
	
	# Link
	dd['Link'] = url

	# Item Name
	iname = html.find('h3', {'class':'header-primary--pd'}).get_text()
	print(iname)

	# Price
	price = html.find('div', {'class':'PrceTxt'}).string
	# For certain items price is not shown
	if(price != None):
		dd['Price'] = price
		logger("Price: " + price)
	else:
		logger("Price not listed!")
	
	# Description
	description = html.find('div', {'class':'CpyCntnr'}).p.get_text()
	dd['Description'] = description
	logger(description)
	
	# Close selenium
	driver.close()

####################################################
# Name: write_csv_row
# Desc: Writes a single row into the csv file.
####################################################
def write_csv_row(data_dict):
	writer.writerow({	'link': data_dict['Link'], 
						'item_name': data_dict['ItemName'], 
						'price': data_dict['Price'], 
						'description': data_dict['Description'],
						'vendor': data_dict['Vendor'],
						'vendor_id': data_dict['VendorID'],
						'manufacturer': data_dict['Manufacturer'],
						'manufacturer_id': data_dict['ManufacturerID']
					})

####################################################
# Name: null_dict
# Desc: Resets all of the data dictionary values
# to the string 'None'. This is necessary because
# not all websites contain all the data points. It
# helps avoid any of the NoneType errors. 
####################################################
def null_dict():
	dd['Link'] = 'None'
	dd['ItemName'] = 'None'
	dd['Price'] = 'None'
	dd['Description'] = 'None'
	dd['Vendor'] = 'None'
	dd['VendorID'] = 'None'
	dd['Manufacturer'] = 'None'
	dd['ManufacturerID']  = 'None'


######################################################
# Name: __main__
# Desc: This code is the initialization and control
# logic for the entire program. Prepares the user 
# supplied links.txt file for processing. Prepares the
# CSV dictonary writer. For each link read in, process
# the site for it's data points, and write that info
# into the data.csv file.
######################################################
if __name__ == '__main__':
	print("Starting Link Processing...")
	
	# Open links.txt
	file = open('links.txt')

	# Open csv file for writing/appending
	with open('data.csv', 'a', newline='') as csvfile:
		# Supply the core field names
		fieldnames = ['link', 'item_name', 'price', 'description', 'vendor', 'vendor_id', 'manufacturer', 'manufacturer_id']
		
		# Initalize csv writer and write initial header
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()

		########### Control Structure ###########
		# Read in links from a file line by line
		# Process each link based on domain name
		for url in file:
			# Null out dictionary each iteration
			null_dict()

			# Selects and processes each site
			# Make sure to remove appended newline
			process_website(url.rstrip())

			# Writes a single row to data.csv file
			write_csv_row(dd)
		file.close()