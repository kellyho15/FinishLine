from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re

# open new chrome browser
driver = webdriver.Chrome()

# open csv to record data
csv_file = open('finishline_review.csv', 'w')
writer = csv.writer(csv_file)

# go to the page to scrape
driver.get("https://www.finishline.com/store/product/mens-nike-air-zoom-mariah-flyknit-racer-running-shoes/prod902579?styleId=918264&colorId=401")


# get item info
item = driver.find_element_by_xpath('//h1[@id="title"]').text
price = driver.find_element_by_xpath('//div[@class="productPrice"]/span').text



# Click review button to go to the review section
review_button = driver.find_element_by_xpath('//span[@class="BVRRNumber"]')
review_button.click()


# Page index used to keep track of where we are. ##################
index = 1
while True:
	try:
		print("Scraping Page number " + str(index))
		index = index + 1
		# Find all the reviews on the page
		wait_review = WebDriverWait(driver, 10)
		reviews = wait_review.until(EC.presence_of_all_elements_located((By.XPATH,
									'//span[@itemprop="review"]')))

		ave = driver.find_element_by_xpath('//div[@class="BVDIBody BVDI_QTBodySummaryBox"]')

		ave_stars = ave.find_element_by_xpath('//div[@class="BVRRRatingNormalImage"]/img').get_attribute('title')
		total_review = ave.find_element_by_xpath('//span[@class="BVRRCustomReviewCountNumber"]').text
		recom = ave.find_element_by_xpath('//span[@class="BVRRBuyAgainPercentage"]').text
		ave_size = ave.find_element_by_xpath('(//div[@class="BVRRRatingSliderImage"]/img)').get_attribute('title')
		ave_width = ave.find_element_by_xpath('(//div[@class="BVRRRatingSliderImage"]/img)[2]').get_attribute('title')
		ave_comfort = ave.find_element_by_xpath('(//div[@class="BVRRRatingSliderImage"]/img)[3]').get_attribute('title')
		
		
		
		for review in reviews:
			# Initialize an empty dictionary for each review
			review_dict = {}
			# Use relative xpath to locate the title, text, username, date.
			# Once you locate the element, you can use 'element.text' to return its string.
			# To get the attribute instead of the text of each element, use 'element.get_attribute()'
			
			try:
				stars = review.find_element_by_xpath('.//div[@class="BVRRRatingNormalImage"]/img').get_attribute('title')
			except NoSuchElementException:
				stars = ""

			try:
				title = review.find_element_by_xpath('.//span[@itemprop="name"]').text
			except NoSuchElementException:
				title = ""
			
			try:
				user = review.find_element_by_xpath('.//span[@itemprop="author"]').text
			except NoSuchElementException:
				user = ""
			
			try:
				review_text = review.find_element_by_xpath('.//span[@class="BVRRReviewText"]').text
			except NoSuchElementException:
				review_text = ""
			
			try:
				reason = review.find_element_by_xpath('.//span[@class="BVRRValue BVRRContextDataValue BVRRContextDataValuePurchaseReason"]').text
			except NoSuchElementException:
				reason = ""
			
			try:
				helpful = review.find_element_by_xpath('.//span[@class="BVDINumber"]').text
			except NoSuchElementException:
				helpful = ""
			
			try:
				not_helpful = review.find_element_by_xpath('(.//span[@class="BVDINumber"])[2]').text
			except NoSuchElementException:
				not_helpful = ""

			try:
				date = review.find_element_by_xpath('.//meta[@itemprop="datePublished"]').get_attribute('content')
			except NoSuchElementException:
				date = ""

			review_dict['item'] = item
			review_dict['price'] = price
			review_dict['ave_stars'] = ave_stars
			review_dict['total_review'] = total_review
			review_dict['recom'] = recom
			review_dict['ave_size'] = ave_size
			review_dict['ave_width'] = ave_width
			review_dict['ave_comfort'] = ave_comfort


			review_dict['stars'] = stars
			review_dict['title'] = title
			review_dict['user'] = user
			review_dict['review_text'] = review_text
			review_dict['reason'] = reason
			review_dict['helpful'] = helpful
			review_dict['not_helpful'] = not_helpful
			review_dict['date'] = date


			writer.writerow(review_dict.values())

		# Locate the next button on the page

		wait_button = WebDriverWait(driver, 10)
		next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,
									'//button[@class="button pag-button light-gray ml-1"]')))
		next_button.click()
		time.sleep(2)

	except Exception as e:
		print(e)
		csv_file.close()
		driver.close()
		break