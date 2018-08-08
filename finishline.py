from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import re

# open new chrome browser
driver = webdriver.Chrome()

# open csv to record data
csv_file = open('finishline_men.csv', 'w')
writer = csv.writer(csv_file)

# get start url
driver.get("https://www.finishline.com/store/men/shoes/_/N-1737dkj?mnid=men_shoes#/store/men/shoes/_/N-1737dkj?mnid=men_shoes&No=0")

last_page = driver.find_element_by_xpath('.//span[@class="results-count"]').text
last_page_number = int(re.findall('\d+', last_page)[0])

urls = ['https://www.finishline.com/store/men/shoes/_/N-1737dkj?mnid=men_shoes#/store/men/shoes/_/N-1737dkj?mnid=men_shoes&No={}'.format(x) for x in range(0,last_page_number,40)]

# Page index used to keep track of where we are
index = 1

# go to the page to scrape
for url in urls:
	print("Scraping Page number " + str(index))
	index = index + 1
	
	driver = webdriver.Chrome()
	driver.get(url)

	# load the whole page
	time.sleep(2)
	SCROLL_PAUSE_TIME = 0.5

	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
		# Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)

		# Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height


	# Find all the shoes on the page
	shoes = driver.find_elements_by_xpath('//div[@class="product-card"]')
	
	for shoe in shoes:
		# Initialize an empty dictionary for each shoe
		shoe_dict = {}

		# Use relative xpath to locate the item, color, price, sale price, review numbers, rating			
		item = shoe.find_element_by_xpath('.//h2[@class="product-name"]').text
		color = shoe.find_element_by_xpath('.//strong[@class="color-count hide-for-small-only"]').text
		price = shoe.find_element_by_xpath('.//div[@class="product-card__details"]/div/span').text
		
		try:
			sale_price = shoe.find_element_by_xpath('.//div[@class="product-card__details"]/div/span[2]').text
		except:
			sale_price =""

		try:
			review = shoe.find_element_by_xpath('.//span[@class="rating-count"]').text
			review_num = int(re.findall('\d+', review)[0])
		except NoSuchElementException:
			review_num = ""
			
		try:
			rating = shoe.find_element_by_xpath('.//div[@class="product-card-stars"]').get_attribute('data-user-rating')
		except NoSuchElementException:
			rating = ""

		shoe_dict['item'] = item
		shoe_dict['color'] = color
		shoe_dict['price'] = price
		shoe_dict['sale_price'] = sale_price
		shoe_dict['review_num'] = review_num
		shoe_dict['rating'] = rating
		
		writer.writerow(shoe_dict.values())

csv_file.close()
driver.close()
