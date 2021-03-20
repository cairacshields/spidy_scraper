# Spidy Scraper

It's a webscraper that will constantly go through Newegg and Amazon to search for stock/price changes on the geforce 3080 graphics card. 

# How To Use

You'll need to install these packages using pip:
 1. requests
 2. BeautifulSoup4
 3. textmagic
 4. emoji
Syntax `pip install requests`

Next, you'll want to add your phone number in the code: `phoneNumber = 'your_number'`. 

After that, you should just be able to run the python program on your machine! 🙌

## High level overview of how it works

Essentially what it will do is, go through the HTML of each site and search for certain `DIV's` or `SPAN's` that contain information about the product. 

If the information matches some condition (ex: being lower than a certain price) we will notify you with the text message. 

**Side note:** 
*Please don't spam the message functionality, because they aren't free and you should only send the text if the status of the item is a positive one 😁*
