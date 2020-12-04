# coding: utf-8
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import time, json, requests
import os
import sys
rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(rootPath)
os.environ["DJANGO_SETTINGS_MODULE"] = "payment_gateways.settings"
import django
django.setup()
# ============================================================
from home.models import result
from scraper_api import ScraperAPIClient
client = ScraperAPIClient('60d3e592477ebfd328a11e92ce6600c9')

# ============================================================
# Main Process Handler
class ScraperHandler():
    def __init__(self, craigslist_url,sid,scrapper_name,objLog):
        self.craigslist_url = craigslist_url
        
        self.sid = sid
        self.scrapper_name = scrapper_name
        self.counter = 0
        self.logger = objLog
        # self.proxies  = {
        #     "http": "http://scraperapi:60d3e592477ebfd328a11e92ce6600c9@proxy-server.scraperapi.com:8001",
        #     "https": "http://scraperapi:60d3e592477ebfd328a11e92ce6600c9@proxy-server.scraperapi.com:8001"
        #     }
        
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('load-extension=/home/nvdeep/Projects/Scripts/chromedriver')
        # self.driver = webdriver.Chrome('/home/nvdeep/Projects/Scripts/chromedriver')
        # self.driver.get('https://dashboard.hcaptcha.com/welcome_accessibility')
        
        # time.sleep(30)
        # self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div[3]/button').click()

    def getAllcraigslist(self):
        try:
            lg_type = 'INFO'
            lg_msg = 'Process Started For '+str(self.scrapper_name)+'   '+str(self.craigslist_url)
            self.logger.dolog('getAllcraigslist',lg_type,lg_msg)
            pagesoup = self.getSoup(self.craigslist_url)
            try:
                total_pages = pagesoup.find('span', attrs={'class':'totalcount'})
                total_pages = total_pages.text.strip()
                total_pages = int(total_pages)/120
                total_pages = int(total_pages)
            except:
                total_pages = 1
            
            lg_type = 'INFO'
            lg_msg = 'Total Pages are '+str(total_pages)
            self.logger.dolog('getAllcraigslist',lg_type,lg_msg)

            all_craigslist = []
            for page in range(total_pages):
                
                # 'https://orlando.craigslist.org/search/rea?s=0'
                craigslist_url = self.craigslist_url + str(int(page)*120)
                soup = self.getSoup(craigslist_url)
                craigslist_url = soup.findAll('a', attrs={'class':'result-title'})
                for craigslist in craigslist_url:
                    try:
                        main_arr = []
                        craig_url = craigslist['href']
                        is_exists = result.objects.filter(url = craig_url).count()
                        
                        if is_exists>0:
                            # print('In Continue')
                            continue
                                            
                        craigslist_data = self.getDetailOfcraigslist(craig_url)
                        main_arr.append(craigslist_data)
                        print('==================================')
                        
                        title = craigslist_data['Title']
                        url = craigslist_data['Url']
                        zipcode = craigslist_data['Zip']
                        city = craigslist_data['City']
                        price = craigslist_data['Price']
                        desc = craigslist_data['Desc']
                        bedroom = craigslist_data['Bedroom']
                        pics = craigslist_data['Pics']
                        bathrooms = craigslist_data['Bathrooms']
                        address = craigslist_data['Address']
                        posted = craigslist_data['Posted']
                        area = craigslist_data['Area']
                        latlon = craigslist_data['Latlon']
                        state = craigslist_data['state']
                        
                        
                        
                        obj_craig = result()
                        obj_craig.title = title
                        obj_craig.scraper_id=self.sid
                        obj_craig.scraper_name=self.scrapper_name
                        obj_craig.Address = address
                        obj_craig.zipcode = zipcode
                        obj_craig.area = area
                        obj_craig.latlon = latlon
                        obj_craig.Address = address
                        obj_craig.city = city
                        obj_craig.state = state
                        obj_craig.price = price
                        obj_craig.bathrooms = bathrooms
                        obj_craig.Bedrooms = bedroom
                        obj_craig.list_date = posted
                        obj_craig.Description = desc
                        obj_craig.Pictures = pics
                        obj_craig.rawdata=main_arr
                        obj_craig.url = url
                        obj_craig.source = 'craigslist'
                        # TODO:
                        # obj_craig.save()
                        self.counter+=1
                        print('Done ',self.counter)
                        
                        # break
                    except:
                        import sys
                        lg_type = 'ERROR'
                        lg_msg = sys.exc_info()
                        self.logger.dolog('getAllcraigslist',lg_type,lg_msg)
            # Here is the code
        except:
            import sys
            lg_type = 'ERROR'
            lg_msg = sys.exc_info()
            self.logger.dolog('getAllcraigslist',lg_type,lg_msg)

    def getDetailOfcraigslist(self, craig_url):
        craigslist_data = {}
        try:
            # craig_url = 'https://jacksonville.craigslist.org/reo/d/yulee-get-into-your-next-home-before/7190127157.html'
            soup = self.getSoup(craig_url)
            try:
                Title = soup.find('span', attrs={'id':'titletextonly'})
                Title = Title.text.strip()
                Title = " ".join(Title.split())
                Title = Title.strip()
            except:
                Title = 'N/A'

            reg = 'N/A'
            try:
                script = soup.findAll("script", {"type": "application/ld+json"})[1]
                Address = json.loads(script.contents[0], strict=False)
                
                try:
                    reg = Address['address']['addressRegion']
                except:
                    reg = 'N/A'
                
                
                Address = Address['address']['streetAddress']+', '+Address['address']['addressLocality']+', '+Address['address']['addressRegion']+', '+Address['address']['addressCountry']
                Address = " ".join(Address.split())
                Address = Address.strip()
            except:
                Address = 'N/A'

            try:
                script = soup.findAll("script", {"type": "application/ld+json"})[1]
                City = json.loads(script.contents[0], strict=False)
                City = City['address']['addressLocality']
                City = City.strip()
            except:
                City = 'N/A'

            try:
                script = soup.findAll("script", {"type": "application/ld+json"})[1]
                Zip = json.loads(script.contents[0], strict=False)
                Zip = Zip['address']['postalCode']
                Zip = Zip.strip()
            except:
                Zip = 'N/A'

            try:
                try:
                    Bedrooms = soup.find('section',attrs={'id':'postingbody'})
                    Bedrooms = str(Bedrooms).split('BEDS:')[1].split('<br/>')[0]
                except:
                    Bedrooms = soup.find('section',attrs={'id':'postingbody'}).text.lower().split('bed')[0].split(' ')[-2]
                    
                if len(Bedrooms)>2:
                    Bedrooms = soup.find('span',attrs={'id':'titletextonly'}).text.lower().split('bed')[0].split(' ')[-2]
                
                if not Bedrooms.isdigit():
                    Bedrooms = 'N/A'
                    
            except:
                Bedrooms = 'N/A'
                
            try:
                try:
                    Bathroom = soup.find('section',attrs={'id':'postingbody'})
                    Bathroom = str(Bathroom).split('BATHS:')[1].split('<br/>')[0]
                except:
                    Bathroom = soup.find('section',attrs={'id':'postingbody'}).text.lower().split('bath')[0].split(' ')[-2]
                if len(Bathroom)>2:
                    Bathroom = soup.find('span',attrs={'id':'titletextonly'}).text.lower().split('bath')[0].split(' ')[-2]
                    
                if not Bathroom.isdigit():
                    Bathroom = 'N/A'
                    
            except:
                Bathroom = 'N/A'

                            
            try:
                Description = soup.find('section',attrs={'id':'postingbody'}).text.strip()
                if 'QR Code Link to This Post' in Description:
                    Description = Description.split('QR Code Link to This Post')[1].strip()
            except:
                Description = 'N/A'


            try:
                lat = soup.find('div',attrs={'id':'map'})['data-latitude']
                lon = soup.find('div',attrs={'id':'map'})['data-longitude']
                
                latlon = str(lat)+' '+str(lon)
                
            except:
                latlon = 'N/A'
                
            try:
                img_arr = []
                images = soup.findAll('img')
                for img in images:
                    image = img['src']
                    img_arr.append(image)    
            except:
                img_arr = []
                            
                
            try:
                Price = soup.find('span',attrs={'class':'price'}).text.strip()
            except:
                Price = 'N/A'            
            try:
                Posted = soup.find('time',attrs={'class':'date timeago'}).text.strip()
            except:
                Posted = 'N/A'
                
            try:
                Area = soup.find('span',attrs={'class':'housing'}).text.strip()
            except:
                Area = 'N/A'
        
            # try:
            #     try:
            #         Phone = soup.find('section',attrs={'id':'postingbody'})
            #         Phone = str(Phone).split('</section>')[-2].split('<br/>')[-1].split('(')[1]
            #         Phone = '('+Phone
            #         # print(Phone)
            #     except:
            #         Phone = soup.find('section',attrs={'id':'postingbody'}).text.split('@')[1].split('PRICE')[0]
            #         # print(Phone)
                
            # except:
            #     Phone = ''
                
            # print(Phone)

            craigslist_data.update({'Title': Title})
            craigslist_data.update({'Url': craig_url})
            craigslist_data.update({'Zip': Zip})
            craigslist_data.update({'City': City})
            craigslist_data.update({'Price': Price})
            craigslist_data.update({'Desc': Description})
            craigslist_data.update({'Bedroom': Bedrooms})
            craigslist_data.update({'Pics': img_arr})
            craigslist_data.update({'Bathrooms': Bathroom})
            # craigslist_data.update({'Phone': Phone})
            craigslist_data.update({'Address': Address})
            craigslist_data.update({'Posted': Posted})
            craigslist_data.update({'Area': Area})
            craigslist_data.update({'Latlon': latlon})
            craigslist_data.update({'state': reg})
        except:
            return {}
        return craigslist_data
    
    def getSoup(self, craig_url):
        try:
            # print(self.proxies)
            con = requests.get(craig_url)
            soup= BeautifulSoup(con.content, u'html.parser')
        except:
            import sys
            lg_type = 'ERROR'
            lg_msg = sys.exc_info()
            self.logger.dolog('getSoup',lg_type,lg_msg)
            soup = None
        return soup


