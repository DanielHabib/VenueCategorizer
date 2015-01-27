# VenueCategorizer
Pull meta data from a variety of websites about a specific venue

The primary goal of the Venue categorizer is to pull venue metadata (Category, Proximity Boundary, Hours of Operation , Images,etc.)
In its current form, it uses two different methods for pulling venue category, API Calls and Webscraping but will implement more as I find methods that yield quality results.
I have provided both OO and Procedural implementations and examples within.


--------------------------------------Methods
||
API --Foursquare

  You must supply your own API credentials,from foursquare in order to use the associated methods. This is HIGHLY reccomended if you are trying to categorize venues because Foursquare is able to categorize with 75%+ rate of accuracy. The images provided by the foursquare API aren't relevant because it supplies user generated photos. These photos can be completely misleading and have nothing to do with the venue. The throttler that is implemented will prevent you from ever breaching their limit on a single thread.
  
WebScraping - Google, GooglePlus,Yelp

  Scraping Google, GooglePlus,Yelp yields a wide variety of information. While not being as powerful in categorization as Foursquare, it does supply very strong results for images and hours of operation. 
  WARNING:: Methods are taken to prevent you from being blocked by Google and Yelp, while these methods are effective they can still result in getting blocked. Random throttlers are used and random user agents are used throughout the code. To mask my IP I make use of Amazon EC2 instances. Run a portion of the http requests on each one(Approx 120 per) and then I have it deleted, this is all done programatically . This prevents me from being blocked and I have not had any issues up to this point.
  
-----------------------------------------Input
||
Sample input Provided under sampleInputData
  
----------------------------------------Results
||
Out of 500,000 venues I was able to receive 94% Categorization. Spot checking the results proved very promising and I have found one bad category assignment after checking for 20 minutes.

-----------------------------------------GOALS
||
To adapt the code to provide a wide variety of meta data from a select choice of reliable sources
