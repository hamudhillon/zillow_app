import requests
from bs4 import BeautifulSoup

con = requests.get('https://orlando.craigslist.org/reb/d/our-experience-your-home-home-in-winter/7230611348.html')

soup= BeautifulSoup(con.content, u'html.parser')
try:
    try:
        Bedrooms = soup.find('section',attrs={'id':'postingbody'})
        Bedrooms = str(Bedrooms).split('BEDS:')[1].split('<br/>')[0]
        print('Beds',Bedrooms)
    except:
        Bedrooms = soup.find('section',attrs={'id':'postingbody'}).text.lower().split('bed')[0].split(' ')[-2]
        
    if len(Bedrooms)>2:
        Bedrooms = soup.find('span',attrs={'id':'titletextonly'}).text.lower().split('bed')[0].split(' ')[-2]
    
    if not Bedrooms.isdigit():
        Bedrooms = 'N/A'
        
except:
    # import sys
    # print(sys.exc_info())
    Bedrooms = 'N/A'
    
try:
    try:
        Bathroom = soup.find('section',attrs={'id':'postingbody'})
        Bathroom = str(Bathroom).split('BATHS:')[1].split('<br/>')[0]
    except:
        Bathroom = soup.find('section',attrs={'id':'postingbody'}).text.lower().split('bath')[0].split(' ')[-2]
        
        # print(Bathroom)
    if len(Bathroom)>2:
        Bathroom = soup.find('span',attrs={'id':'titletextonly'}).text.lower().split('bath')[0].split(' ')[-2]
        
    if not Bathroom.isdigit():
        Bathroom = 'N/A'
        
except:
    Bathroom = 'N/A'
             
# print(Bathroom,Bedrooms)
