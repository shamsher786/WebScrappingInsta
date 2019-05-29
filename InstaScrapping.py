from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from bs4 import BeautifulSoup
import shutil
import requests

class App:
	def __init__(self, username='8376095003',password='9717157932',target_username='shamsheralikhan786',
	path='D:\Wbscrapping_InstaAccount\pictures'):

		#print(os.path.exists(path)) # check whether path exists or not
		#print("path is :", path)
		self.username = username
		self.password = password
		self.target_username = target_username
		self.path = path
		self.driver = webdriver.Chrome('D:\Software\chromedriver.exe')
		self.main_url = 'https://www.instagram.com'
		self.error = False
		self.driver.get(self.main_url)
		sleep(3)
		
		self.login()
		if self.error is False:
			self.closeDialogueBox()
			self.openTargetprofile()
		if self.error is False:
			self.scrollDown()
		if self.error is False:
			if not os.path.exists(path):
				os.mkdir(path)
			self.DownloadingImages()

		sleep(5)
		self.driver.close()

	def login(self,):
		try:
			loginButton = self.driver.find_element_by_xpath('//p[@class="izU2O"]//a')
			print("HII",loginButton)
			loginButton.click()
			try:
				wait = WebDriverWait(self.driver,10);
				wait.until(EC.title_contains("Login"))
				#assert.true(self.driver.title_contains("Login"));
				usernameInput = self.driver.find_element_by_xpath("//input[@name='username']")
				usernameInput.send_keys(self.username)
				passwordInput = self.driver.find_element_by_xpath("//input[@name='password']")
				passwordInput.send_keys(self.password)
				usernameInput.submit()
			except Exception as e:
				print('Unable to find username and password field')
				self.error = True
				print(e)
		except Exception as e:
			print('Unable to Login!!')
			self.error = True
			print(e)
			

	def openTargetprofile(self):
		try:
			print("inside search function")
			sleep(1)
			searchBar = self.driver.find_element_by_xpath('//input[@placeholder="Search"]')
			searchBar.send_keys(self.target_username)
			sleep(5)
			tareget_profile_url = self.main_url + '/' + self.target_username + '/'
			self.driver.get(tareget_profile_url)
			sleep(3)
		except Exception:
			print ('Unable to open target profile!!!!!!!')


	def closeDialogueBox(self):
		try:
			sleep(3)
			popupBox = self.driver.find_element_by_xpath('//button[@class="aOOlW   HoLwm "]')
			popupBox.click()
			print("Dialogue box is closed!!!")
		except Exception:
			print('Unable to find dialogue box!!')

	def scrollDown(self):
		try:
			numberOfPosts = self.driver.find_element_by_xpath('//span[@class="g47SY "]')
			numberOfPosts = str(numberOfPosts.text).replace(',','') # 15,489 --> 15483
			numberOfPosts = int(numberOfPosts)
			print("number of posts are :",numberOfPosts)

			if numberOfPosts > 12:
				numberOfScrolls = int(numberOfPosts/12) + 3
				print("Number of scroll ", numberOfScrolls)

				for value in range(numberOfScrolls):
					print(value)
					self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
					sleep(1)
		except Exception:
			print('Scroll failed!!!')

	def DownloadingImages(self):
		soup = BeautifulSoup(self.driver.page_source ,'lxml')
		#sleep(2)
		allImages = soup.find_all('img')
		#sleep(2)
		print('Length of all images', len(allImages))
		self.DownloadCaptions(allImages)

		for index , image in enumerate(allImages):
			filename = 'image_' + str(index) + '.jpg'
			#imagePath = self.path + '/' + filename
			#print(imagePath)
			imagePath = os.path.join(self.path, filename)
			link = image['src']
			print('Downloading iamge',index)
			response = requests.get(link, stream=True)
			try:
				with open(imagePath, 'wb') as file:
					shutil.copyfileobj(response.raw, file)
			except Exception as e:
				print(e)
				print('Could not download image number', index)
				print('Image link --->', link)

	def DownloadCaptions(self, images):
		captionsFolderPath = os.path.join(self.path, 'captions')
		if not os.path.exists(captionsFolderPath):
			os.mkdir(captionsFolderPath)
		for index, image in enumerate(images):
			try:
				caption = image['alt']
			except KeyError:
				caption = 'No caption exists for this image'
			fileName = 'caption_' + str(index) + '.txt'
			filePath = os.path.join(captionsFolderPath , fileName)
			link = image['src']
			with open(filePath , 'wb') as file:
				file.write(str("link: " + str(link)  + "      \n" + "caption:" + caption).encode())

if __name__ == '__main__':
	app = App()