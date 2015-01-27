from pprint import pprint
from threading import Thread, Lock
from multiprocessing import Process, Lock
from requests_throttler import BaseThrottler
import requests
import bs4
#import queue
import json
import csv
import random
import time



#API-Foursquare
#Scrape - GooglePlus, Yelp

class venueCategorizer:


	def __init__(self):
		#apiCallsEnabled and scrapingEnabled are safety precautions to make sure you are aware of what is going on
		print ("\n\n\n\n\n Venue Categorizer \n______________ ")
		pprint("Initializing.")
		self.apiCallsEnabled = False
		self.scrapingEnabled = False
		#INSERT Foursquare API Credentials
		self.FSclientID="&client_id=V"
		self.FSclientSecret="&client_secret="
		self.FSv="&v="
		#Google Info to be Scraped If Available
		self.GHoursOfOperationFlag = False
		self.GImageFlag = False

		self.UserAgents=[]

		self.throttlingConstant=.8675309

		self.entryList=[]
		self.entryDict={}

		self.urlList=[]		
		self.urlDict= {}
		self.foursquareUrlDict={}
		self.YelpUrlDict={}
		self.GooglePlusUrlDict={}

		self.successCounter=0
		self.failureCounter=0

		self.foursquareCounter=0
		self.foursquareClientID=""
		self.foursquareClientSecret=""
 
		self.yelpCounter=0
		self.googlePlusCounter=0
		#Threading
		self.mutex = Lock()

		with open("venues.csv","rt",encoding="utf8") as venueData:
			reader = csv.DictReader(venueData)
			data = next(reader)
			for a in reader:
				self.entryList.append(a)
				self.entryDict[a["venueID"]]=a
		with open("UserAgentList.csv","rt",encoding="utf8") as userAgentData:	
			reader = csv.DictReader(userAgentData)
			data = next(reader)
			for a in reader:
				self.UserAgents.append(a["User-Agent"])
		pprint("Initialization Complete")
		print(".......................")


	def __repr__(self):
		return "Venue Category Scraper"
	def __iter__ (self):
		for a in urlList:
			yield a
	def __getitem__(self,key):
		for a in self.urlDict.keys():
			return urlDict[key]
	def __len__(self) :
		return len(entryList)

	#Currently suppourted websites/apis are foursquare api, google+, yelp. Be careful as to not get blocked
	def urlBuilder(self,Websites):
		if self.scrapingEnabled:
			pprint("Scraping Enabled")
		else:
			pprint("Scraping Disabled")
		if self.apiCallsEnabled:
			pprint("API Calls Enabled")
		else:
			pprint("API Calls Disabled")
		if self.apiCallsEnabled:
			if "Foursquare" in Websites:
				print(".......................")
				pprint("Generating Foursquare URLs")				
				self.foursquareURLGenerator()
				pprint("Foursquare URLs Complete")
				print(".......................")
		if self.scrapingEnabled:
			if "GooglePlus" in Websites:
				pprint("Generating GooglePlus URLs ")
				self.GooglePlusURLGenerator()
				pprint("GooglePlus URLs Complete")
				print(".......................")
			if "Yelp" in Websites:
				pprint("Generating Yelp URLs")
				self.YelpURLGenerator()
				pprint("Yelp URLS Complete")
				print(".......................")
	def Categorizer(self):
		if self.apiCallsEnabled:
			self.foursquareApiCaller()
		if self.scrapingEnabled :
			self.googlePlusScraper()

		
	def foursquareApiCaller(self):
		#Using the foursquare API alone it successfully categorizes 460,000 out of 500,000
		#The other scrapers will be there to help
		self.simpleRandomThrottler()
		for c in self.foursquareUrlDict.keys():
			foursquareLink=self.foursquareUrlDict[c][0]
			foursquareResponse=requests.get(foursquareLink,headers=self.headerCycler())
			fsJson = foursquareResponse.json()
			category=""
			d=self.entryDict[c]
			venueid=c
			try:
				name = d["name"]
				fsJson['response']['venues']
				for a in fsJson['response']['venues']:
					if name==a['name'] :
						FSvenueID=a['id']
						foursquareImageLink = "https://api.foursquare.com/v2/venues/"+FSvenueID+"/photos?"+self.FSclientID+self.FSclientSecret+self.FSv
						foursquareImageResponse = requests.get(foursquareImageLink,headers=self.headerCycler())
						fsImageJson=foursquareImageResponse.json()
						with open('py_results.csv','a') as csvfile:
							categoryWriter = csv.writer(csvfile,quoting=csv.QUOTE_NONE,lineterminator='\n',delimiter=',')
							categoryWriter.writerow([venueid,a['categories'][0]['name'],"foursquare"])
							csvfile.close()
							pprint("Foursquare             -"+name+"-"+a['categories'][0]['name'])							
							self.foursquareCounter+=1						
						for b in fsImageJson['response']['photos']['items']:
							prefix = b["prefix"]
							width = str(b["width"])
							height = str(b["height"])
							suffix = b["suffix"]
							imgURL = prefix + width + "x" + height + suffix
							with open('VenueImages.csv','a') as csvfile:
								imageWriter = csv.writer(csvfile,quoting=csv.QUOTE_NONE,lineterminator='\n',delimiter=',')
								imageWriter.writerow([venueid,imgURL,"foursquare"])
								csvfile.close()
							break
					else:
						if self.levenshtein_jumbledwords(name,a['name'])>60:
							FSvenueID=a['id']
							foursquareImageLink = "https://api.foursquare.com/v2/venues/"+FSvenueID+"/photos?"+self.FSclientID+self.FSclientSecret+self.FSv
							foursquareImageResponse = requests.get(foursquareImageLink,headers=self.headerCycler())
							fsImageJson=foursquareImageResponse.json()
							bFlag = True
							with open('py_results.csv','a') as csvfile:
								categoryWriter = csv.writer(csvfile,quoting=csv.QUOTE_NONE,lineterminator='\n',delimiter=',')
								categoryWriter.writerow([venueid,a['categories'][0]['name'],"foursquare"])
								csvfile.close()
								pprint("Foursquare             -"+name+"-"+a['categories'][0]['name'])	
								self.foursquareCounter+=1
							for b in fsImageJson['response']['photos']['items']:
								prefix = b["prefix"]
								width = str(b["width"])
								height = str(b["height"])
								suffix = b["suffix"]
								imgURL = prefix + width + "x" + height + suffix
								with open('VenueImages.csv','a') as csvfile:
									imageWriter = csv.writer(csvfile,quoting=csv.QUOTE_NONE,lineterminator='\n',delimiter=',')
									imageWriter.writerow([venueid,imgURL,"foursquare"])
									csvfile.close()
									break
						else:
							pprint('FOURSQUARE HAS FAILED')					
					break			
				continue
			except(IndexError,KeyError,UnicodeEncodeError):


				pprint("Foursquare Error")

	def googlePlusScraper(self):
		self.simpleRandomThrottler()
		for c in self.GooglePlusUrlDict.keys():
			googlePlusUrl = self.GooglePlusUrlDict[c][0]
			googlePlusResponse = requests.get(googlePlusUrl,headers=self.headerCycler())
			googlePlusSoup = bs4.BeautifulSoup(googlePlusResponse.text)
			try:
				googlePlusCategory = googlePlusSoup.select('div.Ny span.d-s')[0].text
				print("GooglePlusCategory--"+googlePlusCategory)
				with open('py_results.csv','a') as csvfile:	
					categoryWriter = csv.writer(csvfile,quoting=csv.QUOTE_NONE,lineterminator='\n',delimiter=',')
					categoryWriter.writerow([c,googlePlusCategory,"GooglePlus"])
					csvfile.close()
					pprint ( "GooglePlus            -"+ str(self.entryDict[c]['name']) +"-" + googlePlusCategory)
					self.googlePlusCounter+=1
			except IndexError:
				print ("GooglePlus Scraper Index Error")
				print("error on page |||  "+googlePlusUrl)
	def yelpScraper(self):
		for c in YelpUrlDict:
			yelpUrl=YelpUrlDict[c]
			name=urlDict[c]
			responseYelp = requests.get(yelpUrl,headers=self.headerCycler())
			yelpSoup = bs4.BeautifulSoup(responseYelp.text)
			#yelpCategories = yelpSoup.select('div.price-category span.category-str-list')[0].text
			yelpCategory=""
			try:
				yelpCategory = yelpSoup.select('a[href*="c/"]')[0].text
				pprint ( "Yelp                   -"+name +"-"+yelpCategory)
			except IndexError:
				print("Bad Results Yelp")

	def foursquareURLGenerator(self):
		for a in self.entryList:
			name = a["name"]
			city = a["city"]
			state= a["state"]
			lat = a["latitude"]
			lon = a["longitude"]
			venueID = a["venueID"]
			#Client ID Client Secret and Version must be set to your specific Parameters
			#The foursquare api limits requests to 4,000 per hour
			foursquareLink="https://api.foursquare.com/v2/venues/search?&near="
			foursquareLink+=city+","+state+"&ll="+lat+","+lon+"&query="+name+self.FSclientID+self.FSclientSecret+self.FSv
			if venueID in self.foursquareUrlDict.keys(): 
				self.foursquareUrlDict[venueID].append(foursquareLink)
			else :
				self.foursquareUrlDict[venueID] = []
				self.foursquareUrlDict[venueID].append(foursquareLink)
			if venueID in self.urlDict.keys():
				self.urlDict[venueID].append(foursquareLink)
			else:
				self.urlDict[venueID] = []
				self.urlDict[venueID].append(foursquareLink)

	def GooglePlusURLGenerator(self):
		self.simpleRandomThrottler()
		for a in self.entryList:
			name = a["name"]
			city = a["city"]
			state= a["state"]
			lat = a["latitude"]
			lon = a["longitude"]
			venueID = a["venueID"]
			adjustedName = name.replace(" ","+")
			googleBaseUrl = "https://www.google.com/search?q="
			googleLink = googleBaseUrl+adjustedName+"+"+city+"+"+state
			responseGoogle = requests.get(googleLink)#,headers=self.headerCycler())
			googleSoup =  bs4.BeautifulSoup(responseGoogle.text)
			googlePlusLinks =  googleSoup.select('a[href*="https://plus.google.com"]') 
			for a in googlePlusLinks:
				#we only extract the top result
				googlePlusLink=str(a.get('href')) 
				googlePlusLink=googlePlusLink[7:]
				googlePlusLink = googlePlusLink[:45]		
				if venueID in self.GooglePlusUrlDict.keys():
					self.GooglePlusUrlDict[venueID].append(googlePlusLink)
				else :
					self.GooglePlusUrlDict[venueID]=[]
					self.GooglePlusUrlDict[venueID].append(googlePlusLink)
				if venueID in self.urlDict.keys():
					self.urlDict[venueID].append(googlePlusLink)
				else:
					self.urlDict[venueID] = []
					self.urlDict[venueID].append(googlePlusLink)
				break

	def YelpURLGenerator(self):
		self.simpleRandomThrottler()
		for a in self.entryList:
			name = a["name"]
			city = a["city"]
			state= a["state"]
			lat = a["latitude"]
			lon = a["longitude"]
			venueID = a["venueID"]
			adjustedName = name.replace(" ","%20")
			googleBaseUrl = "https://www.google.com/search?q="
			yelpUrl = googleBaseUrl + adjustedName+"%20"+city+"%20"+state+"%20"+"yelp"
			responseYelp = requests.get(yelpUrl,headers=self.headerCycler())
			yelpSoup = bs4.BeautifulSoup(responseYelp.text)
			yelpSoupLinks = yelpSoup.select('a[href*="http://www.yelp.com"]')
			yelpFlag=True
			for a in yelpSoupLinks:
				yelpString = str(a.get('href'))
				try:
					yelpURL = yelpString[7:]
					andIndex = yelpURL.index('&')
					yelpLink = yelpURL[:andIndex]

					pprint(yelpLink)
					if venueID in self.YelpUrlDict.keys():
						self.YelpUrlDict[venueID].append(yelpLink)
					else :
						self.YelpUrlDict[venueID]=[]
						self.YelpUrlDict[venueID].append(yelpLink)
					if venueID in self.urlDict.keys():
						self.urlDict[venueID].append(yelpLink)
					else:
						self.urlDict[venueID] = []
						self.urlDict[venueID].append(yelpLink)
					pprint("Yelp Link Generated")
					break
				except (IndexError,ValueError):
					pprint("Yelp URL invalid")

	def headerCycler(self):
		NewHeader = {}	
		dictLength = len(self.UserAgents)
		userAgentIndex = int(dictLength*random.random())-1
		NewHeader['User-Agent']=self.UserAgents[userAgentIndex]
		return NewHeader
	def Complete(self):
		name="done.txt"
		open(name,'w')
	def levenshtein_jumbledwords(self,first,second):
		#this is to handle venues that may appear like 
		#"City Hall of Dustin" Against "Dustin City Hall"
		s1 = ''
		s2 = ''
		if len(first)>len(second):
			s1=first
			s2=second
		else:
			s1=second
			s2=first
		potentialScore=0
		totalScore=0
		wordLoop1 = s1.split()
		wordLoop2 = s2.split()
		potentialScore = 100 *len(s1.split())

		for a in wordLoop1 :
			highestScore=0
			for b in wordLoop2 :
				score = self.levenshtein_distance(a,b)
				if score > highestScore :
					highestScore = score
			totalScore += highestScore
			highestScore=0
		return (totalScore/potentialScore)*100

	def levenshtein_distance(self,first,second) :
		if len(first) > len(second):
			first, second = second, first
		if len(second) == 0 :
			return len(first)
		first_length = len(first) + 1
		second_length = len(second) + 1
		distance_matrix = [[0] * second_length for x in range(first_length)]
		for i in range(first_length):
			distance_matrix[i][0] = i
			for j in range(second_length):
				distance_matrix[0][j]=j
		for i in range(1, first_length):
			for j in range(1, second_length):
				deletion = distance_matrix[i-1][j] + 1
				insertion = distance_matrix[i][j-1] + 1
				substitution = distance_matrix[i-1][j-1]
				if first[i-1] != second[j-1]:
					substitution += 1
				distance_matrix[i][j] = min(insertion, deletion, substitution)
		operations = distance_matrix[first_length-1][second_length-1]
		return (1-operations/len(second))*100

	def simpleRandomThrottler(self):
		time.sleep(random.random()*self.throttlingConstant+3)
		return ""




#_-------------------------------------------------------------------------------
#_-------------------------------------------------------------------------------
#_-------------------------------------------------------------------------------
#_------------------------------BEGIN PROCEDURAL---------------------------------
#_-------------------------------------------------------------------------------
#_-------------------------------------------------------------------------------
#_-------------------------------------------------------------------------------
#_-------------------------------------------------------------------------------




def get_category_name_url(name,city,state,lat,lon,venueID,UserAgents):
	x=0
	y=0
	#GooglePlus
	time.sleep(1.1)
	FoursquareResult =askFourSquare(name,city,state,lat,lon,venueID,UserAgents)
	if FoursquareResult==True   :
		return True
	else :
		adjustedName = name.replace(" ","+")
		google_url = "https://www.google.com/search?q="
		google_plus_url = google_url+adjustedName
		responseGoogle = requests.get(google_plus_url,headers=headerCycler(UserAgents))
		googleSoup =  bs4.BeautifulSoup(responseGoogle.text)

		googleImage = googleSoup.select('img[src*="https://lh"]')
		print(googleImage)

		googlePlusLinks =  googleSoup.select('a[href*="https://plus.google.com"]') 
		googlePlusFlag=True
		for a in googlePlusLinks:
			gpUrl=str(a.get('href')) 
			gpUrl=gpUrl[8:]
			gpUrl = gpUrl[:45]
			googlePlusFlag=False	
			if(scrapeGooglePlusPage(gpUrl,name,UserAgents)):
				return True
			else:
				if  googlePlusFlag:
					yelpUrl = google_url + adjustedName+"+yelp"
					responseYelp = requests.get(yelpUrl,headers=headerCycler(UserAgents))
					yelpSoup = bs4.BeautifulSoup(responseYelp.text)
					yelpSoupLinks = yelpSoup.select('a[href*="http://www.yelp.com"]')
					yelpFlag=True
					for a in yelpSoupLinks:
						yelpString = str(a.get('href'))
						try:
							yelpURL = yelpString[7:]
							andIndex = yelpURL.index('&')
							yelpURL = yelpURL[:andIndex]
							if (scrapeYelpPage(yelpURL,name,UserAgents)):
								return True
						except IndexError:
							return False
					if yelpFlag:
						print("BAD RESULTS")
						return False
	'''	
	else:
		pprint("Bad Results from Foursquare")
		return False
	'''	
#Start Safe Api Calls
def askFourSquare(name,city,state,lat,lon,venueid,UserAgents):
	clientID="&client_id=V1C3AFPVWVHYW43LZ2JLOTGBMKQOMNQY2DTJLW4GZ4USNI2X"
	clientSecret="&client_secret=RR5TFBWRC1D4TM0VBD4QFKAXU5UOYOJYZZLOVX1COLWAAC1D"
	v="&v=20130815"
	foursquareLink="https://api.foursquare.com/v2/venues/search?&near="
	foursquareLink+=city+","+state+"&ll="+lat+","+lon+"&query="+name+clientID+clientSecret+v
	foursquareResponse=requests.get(foursquareLink,headers=headerCycler(UserAgents))
	fsJson = foursquareResponse.json()
	category=""
	try:
		fsJson['response']['venues']
		for a in fsJson['response']['venues']:
			if name==a['name'] :
				venueID=a['id']
				foursquareImageLink = "https://api.foursquare.com/v2/venues/"+venueID+"/photos?"+clientID+clientSecret+v
				foursquareImageResponse = requests.get(foursquareImageLink,headers=headerCycler(UserAgents))
				fsImageJson=foursquareImageResponse.json()
				for b in fsImageJson['response']['photos']['items']:
					prefix = b["prefix"]
					width = str(b["width"])
					height = str(b["height"])
					suffix = b["suffix"]
					imgURL = prefix + width + "x" + height + suffix
					with open('VenueImages.csv','a') as csvfile:
						imageWriter = csv.writer(csvfile,quoting=csv.QUOTE_NONE,lineterminator='\n',delimiter=',')
						imageWriter.writerow([venueid,imgURL,"foursquare"])
						csvfile.close()
					with open('VenueCategories.csv','a') as csvfile:
						categoryWriter = csv.writer(csvfile,quoting=csv.QUOTE_NONE,lineterminator='\n',delimiter=',')
						categoryWriter.writerow([venueid,a['categories'][0]['name'],"foursquare"])
						csvfile.close()
						pprint("Foursquare             -"+name+"-"+a['categories'][0]['name'])			
					return True	
				with open('VenueCategories.csv','a') as csvfile:
					categoryWriter = csv.writer(csvfile,quoting=csv.QUOTE_NONE,lineterminator='\n',delimiter=',')
					categoryWriter.writerow([venueid,a['categories'][0]['name'],"foursquare"])
					csvfile.close()
					pprint("Foursquare             -"+name+"-"+a['categories'][0]['name'])							
					return True
			else:
				if levenshtein_jumbledwords(name,a['name'])>80:
					venueID=a['id']
					foursquareImageLink = "https://api.foursquare.com/v2/venues/"+venueID+"/photos?"+clientID+clientSecret+v
					foursquareImageResponse = requests.get(foursquareImageLink,headers=headerCycler(UserAgents))
					fsImageJson=foursquareImageResponse.json()
					bFlag = True
					for b in fsImageJson['response']['photos']['items']:
						bFlag=False
						prefix = b["prefix"]
						width = str(b["width"])
						height = str(b["height"])
						suffix = b["suffix"]
						imgURL = prefix + width + "x" + height + suffix
						with open('VenueImages.csv','a') as csvfile:
							imageWriter = csv.writer(csvfile,quoting=csv.QUOTE_NONE,lineterminator='\n',delimiter=',')
							imageWriter.writerow([venueid,imgURL,"foursquare"])
							csvfile.close()
						with open('VenueCategories.csv','a') as csvfile:
							categoryWriter = csv.writer(csvfile,quoting=csv.QUOTE_NONE,lineterminator='\n',delimiter=',')
							categoryWriter.writerow([venueid,a['categories'][0]['name'],"foursquare"])
							csvfile.close()	
							pprint("Foursquare             -"+name+"-"+a['categories'][0]['name'])	
						return True
					if bFlag:
						with open('VenueCategories.csv','a') as csvfile:
							categoryWriter = csv.writer(csvfile,quoting=csv.QUOTE_NONE,lineterminator='\n',delimiter=',')
							categoryWriter.writerow([venueid,a['categories'][0]['name'],"foursquare"])
							csvfile.close()
							pprint("Foursquare             -"+name+"-"+a['categories'][0]['name'])									
						return  True
					with open('VenueCategories.csv','a') as csvfile:
						categoryWriter = csv.writer(csvfile,quoting=csv.QUOTE_NONE,lineterminator='\n',delimiter=',')
						categoryWriter.writerow([venueid,a['categories'][0]['name'],"foursquare"])
						csvfile.close()
						pprint("Foursquare             -"+name+"-"+a['categories'][0]['name'])	
						return True
		return False
	except KeyError:
		print("Bad Four Square Results")
		return ""				
	#Start Scrapers

def scrapeGooglePlusPage(googlePlusUrl,name,UserAgents):
	googlePlusResponse = requests.get(googlePlusUrl,headers=headerCycler(UserAgents))
	googlePlusSoup = bs4.BeautifulSoup(googlePlusResponse.text)
	try:
		googlePlusCategory = googlePlusSoup.select('div.Ny span.d-s')[0].text
		pprint ( "GooglePlus            -"+name +"-" + googlePlusCategory)
		return True
	except IndexError:
		print ("Bad results Google Plus")
		return False

def scrapeYelpPage(yelpUrl,name,UserAgents):
	responseYelp = requests.get(yelpUrl,headers=headerCycler(UserAgents))
	yelpSoup = bs4.BeautifulSoup(responseYelp.text)
	#yelpCategories = yelpSoup.select('div.price-category span.category-str-list')[0].text
	yelpCategory=""
	try:
		yelpCategory = yelpSoup.select('a[href*="c/"]')[0].text
		pprint ( "Yelp                   -"+name +"-"+yelpCategory)
		return True
	except IndexError:
		print("Bad Results Yelp")
		return False


	#Start Auxillary Functions

def headerCycler(UserAgents):
	NewHeader = {}	
	dictLength = len(UserAgents)
	userAgentIndex = int(dictLength*random.random())-1
	NewHeader['User-Agent']=UserAgents[userAgentIndex]
	return NewHeader

def levenshtein_distance(first, second):
	if len(first) > len(second):
		first, second = second, first
	if len(second) == 0:
		return len(first)
	first_length = len(first) + 1
	second_length = len(second) + 1
	distance_matrix = [[0] * second_length for x in range(first_length)]
	for i in range(first_length):
		distance_matrix[i][0] = i
		for j in range(second_length):
			distance_matrix[0][j]=j
	for i in range(1, first_length):
		for j in range(1, second_length):
			deletion = distance_matrix[i-1][j] + 1
			insertion = distance_matrix[i][j-1] + 1
			substitution = distance_matrix[i-1][j-1]
			if first[i-1] != second[j-1]:
				substitution += 1
			distance_matrix[i][j] = min(insertion, deletion, substitution)
	operations = distance_matrix[first_length-1][second_length-1]
	return (1-operations/len(s2))*100

def levenshtein_jumbledwords(self,first,second):
	#this is to handle venues that may appear like 
	#"City Hall of Dustin" Against "Dustin City Hall"
	s1 = ''
	s2 = ''
	if len(first)>len(second):
		s1=first
		s2=second
	else:
		s1=second
		s2=first
	potentialScore=0
	totalScore=0
	wordLoop1 = s1.split()
	wordLoop2 = s2.split()
	potentialScore = 100 * wordCount1
	for a in wordLoop1 :
		highestScore=0
		for b in wordLoop2 :
			score = self.levenshtein_distance(a,b)
			if score > highestScore :
				highestScore = score
		totalScore += highestScore
	return (totalScore/potentialScore)




#  #PROCEDURAL EXAMPLE
# pprint("Preparing User-Agents list.......")
# UserAgents=[]
# with open("C:/Python34/UserAgentList.csv","rt",encoding="utf8") as userAgentData:
# 	reader = csv.DictReader(userAgentData)
# 	data = next(reader)
# 	for a in reader:
# 		UserAgents.append(a["User-Agent"])
# pprint ("Begin Scraping........")
# with open("C:/Python34/scraperVenueData.csv","rt",encoding="utf8") as venueData:
# 	reader = csv.DictReader(venueData)
# 	data = next(reader)
# 	x=0
# 	y=0
# 	for a in reader:
# 		name = a["name"]
# 		city = a["city"]
# 		state= a["state"]
# 		lat = a["latitude"]
# 		lon = a["longitude"]
# 		venueID = a["venueID"]
# 		if name == "" :
# 			pprint("venueID "+venueID+" doesn't have enough information to process")
# 		else:
# 			if get_category_name_url(name,city,state,lat,lon,venueID,UserAgents):
# 				x+=1
# 			else:
# 				y+=1
# 	print ("x ="+str(x))
# 	print ("y ="+str(y))
# pprint("Scraping Complete!")
# print ("\n\n\n\n\n")

#OBJECT ORIENTED EXAMPLE
categorizer = venueCategorizer()
categorizer.apiCallsEnabled=True
categorizer.scrapingEnabled=True
categorizer.urlBuilder(["Foursquare","GooglePlus"])
categorizer.Categorizer()
categorizer.Complete()
print(categorizer.foursquareCounter)