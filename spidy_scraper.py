###
### This program will check the specified website every 1 minute for the current 
### stock status for the geforce 3080 graphics card. 
###
### For Newegg --> If the status is available, you'll get a text message! 
### For Amazon --> If the price is lower than $800 you'll get a tect message! 

import sys
import requests 
from bs4 import BeautifulSoup
from textmagic.rest import TextmagicRestClient
import emoji
from time import time, sleep


#We need these headers to trick amazon into thinking we're using a browser (hahahahahaha jokes on them)
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0'}
newegg_url = 'https://www.newegg.com/evga-geforce-rtx-3080-10g-p5-3897-kr/p/N82E16814487518'
amazon_url = 'https://www.amazon.com/Graphics-Technology-Backplate-DisplayPort-Supernova/dp/B08YP4DYFJ/'

#Set up TextMagic
username = "startyinc"
token = "DkVqJGUWNMJhtaVas3eCg1nbIlQzfE"
client = TextmagicRestClient(username, token)

while True:
  #Do this check every minute 
  #sleep(60 - time() % 60)

  ### NEWEGG ###
  response = requests.get(newegg_url)
  if response.status_code != 200:
    print('Failure' + str(response.status_code))
  else:
    results = BeautifulSoup(response.content, 'html.parser')
  
    #Get the product title (not necessary... but whatever)
    itemTitle = results.head.title.text
  
    #Find the stock status text on the page 
    itemStockStatus = results.find("div", {"id": "ProductBuy"}).text
    itemStockStatus2 = results.find("div", {"class": "product-inventory"}).text
    finalStockStatus = ""
    if itemStockStatus == "":
      finalStockStatus = itemStockStatus2
    else:
      finalStockStatus = itemStockStatus
    
    #Not necessary... but very fun! 
    correctEmoji = ""
    if ("available" in str(itemStockStatus.lower())) or ("in stock" in str(itemStockStatus.lower())) :
      correctEmoji = emoji.emojize(':eyes: :fire:')
      #Define the text to send...
      messageText = itemTitle + " is: " + finalStockStatus + correctEmoji
      message = client.messages.create(phones="13616761174", text=messageText)
    else:
      correctEmoji = emoji.emojize(':crying_face:')
  
    messageText = itemTitle + " is: " + finalStockStatus + correctEmoji
    #Uncomment to send the text NO MATTER what the status is... (This will be pricy)
    #message = client.messages.create(phones="13616761174", text=messageText)

    #Print the message just because 
    print(messageText)  


  #### AMAZON ####
  amazonResponse = requests.get(amazon_url, headers=headers)
  if amazonResponse.status_code != 200:
    print('Failure' + str(amazonResponse.status_code))
  else:
    amazonResults = BeautifulSoup(amazonResponse.content, 'html.parser')
    amazonItemTitle = amazonResults.head.title.text
    #Find the price on the page
    itemCurrentPrice = amazonResults.find("span", {"id": "price_inside_buybox"}).text
    
    #check for comma and remove if found
    if ("," in str(itemCurrentPrice)):
      itemCurrentPrice = itemCurrentPrice.replace(',', '')

    #check for dollar sign and remove if found
    if ("$" in str(itemCurrentPrice)):
      itemCurrentPrice = itemCurrentPrice.replace('$', '')
    
    #check for period and remove if found
    if ("." in str(itemCurrentPrice)):
      split_string = itemCurrentPrice.split(".", 1)
      itemCurrentPrice = split_string[0]

    # You'll get a text if the price is less than $800... (you can change that number if you'd like)
    if int(itemCurrentPrice) <= 800:
      messageText = amazonItemTitle + " is: $" + itemCurrentPrice + " " + emoji.emojize(':eyes: :fire:')
      message = client.messages.create(phones="13616761174", text=messageText)
    else:
      messageText = amazonItemTitle + " is: $" + itemCurrentPrice + " " + emoji.emojize(':crying_face:')
      print(messageText)