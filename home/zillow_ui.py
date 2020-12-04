import os
import sys
rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(rootPath)
os.environ["DJANGO_SETTINGS_MODULE"] = "payment_gateways.settings"
import django
django.setup()
import pandas as pd
from pprint import pprint as pp
import json
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import xlwt
import xlrd
import time
from home.models import result
from home.models import Scraper

from scraper_api import ScraperAPIClient
client = ScraperAPIClient('60d3e592477ebfd328a11e92ce6600c9')


# Logger
import sys
from utilities.LogHandler import DologHandler
from utilities.email_handler import EmailManager

obj_email=EmailManager()
to_email=['hamu.dhillon@gmail.com','deepak.dhanjal12@gmail.com']
subject='Info in Zillow Bot'



# soup=BeautifulSoup(driver.page_source,u'html.parser')
session = HTMLSession()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Referer': 'https://www.zillow.com/homedetails/949-W-Hawthorn-St-APT-32-San-Diego-CA-92101/67712352_zpid/',
    'content-type': 'text/plain',
    'Origin': 'https://www.zillow.com',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

# rb = xlrd.open_workbook(input_filename) 
# sheet = rb.sheet_by_index(0)
row=0
running_city=[]
main_arr=[]
# pagination=str('{"pagination":"currentPage":1}')
# url='https://www.zillow.com/san-diego-ca/condos/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-117.23793983459473%2C%22east%22%3A-117.10301399230957%2C%22south%22%3A32.68056297457832%2C%22north%22%3A32.770821270041424%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A54296%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22wat%22%3A%7B%22value%22%3Atrue%7D%2C%22sf%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D'

def check_rec():
    old_res=result.objects.all()
    
    for res in old_res:
        print(res.url)
        update_obj=result.objects.get(id=res.id)
        list_link=res.url
        if res.url!=None:
            zpid=list_link.split('_zpid/')[0].split('/')[-1]
                # print(zpid)
            con = session.get(
                list_link, headers=headers)
            title=list_link.split(zpid)[0].split('homedetails/')[1].replace('/','').replace('-',' ')
            soup = BeautifulSoup(con.text, u"html.parser")
            main_arr=[]
            s=con.html.find('#hdpApolloPreloadedData',first=True)
            scc=str(s.text)
            # try:
            #     type(json.loads(scc))
            #     # print()
            # except:
            #     import sys
            #     print(sys.exc_info())
            
            try:
                dataa=json.loads(scc)
                datta=json.loads(dataa['apiCache'])['VariantQuery{\"zpid\":'+str(zpid)+'}']
            except:
                update_obj.status='In active'
                update_obj.save()
                continue
            # data2=json.loads(dataa['apiCache'])['ForSaleDoubleScrollFullRenderQuery{\"zpid\":'+str(zpid)+',\"contactFormRenderParameter\":{\"zpid\":'+str(zpid)+',\"platform\":\"desktop\",\"isDoubleScroll\":true}}']
            home_status=datta['property']['homeStatus']
            price=datta['property']['price']
            if 'SOLD' in home_status:
                update_obj.status='In active'
                update_obj.save()

            pre_price=res.price
            # pre_price='099999'
            
            if str(pre_price)!=str(price):
                # update_obj.scraper_id=res.scraper_id
                update_obj.price=price
                update_obj.save()
                print("Price Updated !")
                
                
def zillow_get(url,list_name,sid):
    merror='-'
    log_obj=DologHandler('Zillow','file')
    lg_msg='Started Process with this list name - '+str(list_name)
    lg_type='INFO'
    log_obj.dolog('zillow_get',lg_type,lg_msg)
    message='<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta http-equiv="X-UA-Compatible" content="ie=edge"><meta name="Description" content="Report Of Zillow Bot"/><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.0.0-alpha2/css/bootstrap.min.css"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.0/css/all.min.css"><link rel="stylesheet" href="assets/css/style.css"><title>Zillow Bot Report</title></head><body><table class="table table-borderless">  <thead>    <tr>      <th scope="col">List Name</th>    <th scope="col">Error</th>    </tr>  </thead>  <tbody>    <tr>      <td>'+str(list_name)+'</td> <td>'+str(merror)+'</td>    </tr>  </tbody></table><script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.1/umd/popper.min.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.0.0-alpha2/js/bootstrap.min.js"></script></body></html>'
    obj_email.SendEmail(to_email,subject,message)
    proxies = {
  "http": "http://scraperapi:60d3e592477ebfd328a11e92ce6600c9@proxy-server.scraperapi.com:8001",
  "https": "http://scraperapi:60d3e592477ebfd328a11e92ce6600c9@proxy-server.scraperapi.com:8001"
}
    print(url)
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Referer': 'https://www.zillow.com/new-york-ny/condos/',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
    }

    ''
    if 'searchQueryState=':
        query_state=str(url).split('searchQueryState=')[1]
    # print(query_state)
    else:
        query_state=str(url).split('https://www.zillow.com/homes/')[1].split(',')[0]
    params = (
        ('searchQueryState',query_state),
        ('wants', '{"cat1":["listResults","mapResults"]}'),
        ('requestId', '11'),
    )
    reqq=True
    response = session.get('https://www.zillow.com/search/GetSearchPageState.htm', headers=headers, params=params,proxies=proxies ,verify=False)
    # print(response)
    # data=json.loads(response.content)['cat1']['searchResults']['listResults']
    try:
        total_pages=json.loads(response.content)['cat1']['searchList']['totalPages']
    except:
        reqq=False
        # print('Pass')
        merror=sys.exc_info()
        lg_msg=sys.exc_info()
        lg_type='ERROR'
        log_obj.dolog('zillow_get',lg_type,lg_msg)
        message='<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta http-equiv="X-UA-Compatible" content="ie=edge"><meta name="Description" content="Report Of Zillow Bot"/><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.0.0-alpha2/css/bootstrap.min.css"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.0/css/all.min.css"><link rel="stylesheet" href="assets/css/style.css"><title>Zillow Bot Report</title></head><body><table class="table table-borderless">  <thead>    <tr>      <th scope="col">List Name</th>      <th scope="col">URl</th>        <th scope="col">Error</th>    </tr>  </thead>  <tbody>    <tr>      <td>'+str(list_name)+'</td>      <td>'+str(url)+'</td>      <td>'+str(merror)+'</td>    </tr>  </tbody></table><script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.1/umd/popper.min.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.0.0-alpha2/js/bootstrap.min.js"></script></body></html>'
        obj_email.SendEmail(to_email,subject,message)
        pass
    re_count=0
    while not reqq:
        if re_count==3:
            break
        response = session.get('https://www.zillow.com/search/GetSearchPageState.htm', headers=headers, params=params,proxies=proxies ,verify=False)
        try:
            total_pages=json.loads(response.content)['cat1']['searchList']['totalPages']
        except:
            re_count+=1
            # print('Pass '+str(re_count))
            merror=sys.exc_info()
            lg_msg=sys.exc_info()
            lg_type='ERROR'
            log_obj.dolog('zillow_get',lg_type,lg_msg)
            message='<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta http-equiv="X-UA-Compatible" content="ie=edge"><meta name="Description" content="Report Of Zillow Bot"/><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.0.0-alpha2/css/bootstrap.min.css"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.0/css/all.min.css"><link rel="stylesheet" href="assets/css/style.css"><title>Zillow Bot Report</title></head><body><table class="table table-borderless">  <thead>    <tr>      <th scope="col">List Name</th>      <th scope="col">URl</th>        <th scope="col">Error</th>    </tr>  </thead>  <tbody>    <tr>      <td>'+str(list_name)+'</td>      <td>'+str(url)+'</td>      <td>'+str(merror)+'</td>    </tr>  </tbody></table><script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.1/umd/popper.min.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.0.0-alpha2/js/bootstrap.min.js"></script></body></html>'
            obj_email.SendEmail(to_email,subject,message)
            reqq=False
        
    # total_pages=1
    # print(total_pages)
    # if total_pages>1:
    lg_msg="Total Pages were - "+str(total_pages)
    lg_type='INFO'
    log_obj.dolog('zillow_get',lg_type,lg_msg)
    rec_saved=0
    for tp in range(1,(total_pages+1)):
        # print(tp)
        lin=query_state.replace('%7B%22pagination%22%3A%7B%22currentPage%22%3A%7D%2C','%7B%22pagination%22%3A%7B%22currentPage%22%3A'+str(tp)+'%7D%2C').replace('%7B%22pagination%22%3A%7B%7D%2C','%7B%22pagination%22%3A%7B%22currentPage%22%3A'+str(tp)+'%7D%2C')
        params = (
            ('searchQueryState', lin),
            ('wants', '{"cat1":["listResults","mapResults"]}'),
            ('requestId', '11'),
        )
        response = session.get('https://www.zillow.com/search/GetSearchPageState.htm', headers=headers, params=params,proxies=proxies ,verify=False)
        try:
            data=json.loads(response.content)['cat1']['searchResults']['listResults']
        except:
            lg_msg=sys.exc_info()
            lg_type='ERROR'
            log_obj.dolog('zillow_get',lg_type,lg_msg)
            reqq=False
            continue
        # print(len(data))
        lg_msg="Total Data in this page - "+str(len(data))
        lg_type='INFO'
        log_obj.dolog('zillow_get',lg_type,lg_msg)
        for d in data:
            try:
                list_link=d['detailUrl']
                lg_msg="Running List Url - "+str(list_link)
                lg_type='INFO'
                log_obj.dolog('zillow_get',lg_type,lg_msg)
                
                ck_res=result.objects.filter(url=list_link)
                
                if not ck_res:
                # ld_json=lists.find('script')
                    # print(list_link)
                    zpid=list_link.split('_zpid/')[0].split('/')[-1]
                    # print(zpid)
                    con = session.get(
                        list_link, headers=headers)
                    title=list_link.split(zpid)[0].split('homedetails/')[1].replace('/','').replace('-',' ')
                    soup = BeautifulSoup(con.text, u"html.parser")
                    
                    s=con.html.find('#hdpApolloPreloadedData',first=True)
                    scc=str(s.text)
                    # try:
                    #     print(type(json.loads(scc)))
                    # except:
                    #     import sys
                    #     print(sys.exc_info())
                    
                    dataa=json.loads(scc)
                    datta=json.loads(dataa['apiCache'])['VariantQuery{\"zpid\":'+str(zpid)+'}']
                    data2=json.loads(dataa['apiCache'])['ForSaleDoubleScrollFullRenderQuery{\"zpid\":'+str(zpid)+',\"contactFormRenderParameter\":{\"zpid\":'+str(zpid)+',\"platform\":\"desktop\",\"isDoubleScroll\":true}}']
                    main_arr=dict()
                    try:
                        st_address=datta['property']['streetAddress']
                    except:
                        st_address=''
                    # print(st_address)
                    try:
                        zipcode=datta['property']['zipcode']
                        # print(zipcode)
                    except:
                        zipcode=''
                    try :
                        city=datta['property']['city']
                    except:
                        city=''
                        # print(city)
                    try:
                        state=datta['property']['state']
                    except:
                        state=''
                    try:
                        # print(state)
                        price=datta['property']['price']
                    except:
                        price=''
                    
                    try:
                        # print(price)
                        bathrooms=datta['property']['bathrooms']
                    except:
                        bathrooms=''
                        # print(bathrooms)
                    try:
                        bedrooms=datta['property']['bedrooms']
                        # print(bedrooms)
                    except:
                        bedrooms=''
                    try:
                        zestimate=datta['property']['zestimate']
                    except:
                        zestimate=''
                    # print(zestimate)
                    import datetime
                    # print(str(data2['property']['datePosted'])[:-3])
                    try:
                        list_date=datetime.datetime.fromtimestamp(int(str(data2['property']['datePosted'])[:-3]))
                    except:
                        zestimate=''
                    try:
                        # print(list_date)
                        desc=data2['property']['description']
                    except:
                        zestimate=''
                    pic_arr=[]
                    try:
                        pictures=data2['property']['hugePhotos']
                        for pic in pictures:
                            pic=pic['url']
                            pic_arr.append(pic)
                            # print(pic)
                    except:
                        pic_arr=''
                    try:
                        facts=data2['property']['resoFacts']
                        # print(facts)
                    except:
                        facts=''
                    try:
                        home_fact=data2['property']['homeFacts']
                    except:
                        home_fact=''
                    try:
                        agent_name=data2['property']['listingProvider']['agentName']
                    except:
                        agent_name=''
                    try:
                        agent_number=data2['property']['listingProvider']['phoneNumber']
                    except:
                        agent_number=''
                    try:
                        agent_broke=data2['property']['listingProvider']['postingWebsiteLinkText']
                    except:
                        agent_broke=''
                    try:
                        agent_pic=data2['property']['contactFormRenderData']['data']['contact_recipients'][0]['image_data']['url']
                    except:
                        agent_pic=''
                    # print(agent_pic)
                    try:
                        priceHistory=home_fact=data2['property']['priceHistory']
                    except:
                        priceHistory=''
                    main={
                        "Title":title,
                        "Address":st_address,
                        "City":city,
                        "State":state,
                        "Price":price,
                        "Bathrooms":bathrooms,
                        "Bedrooms":bedrooms,
                        "zestimate":zestimate,
                        "list_date":str(list_date),
                        "Description":desc,
                        "Pictures":pic_arr,
                        "Facts":facts,
                        "home_fact":home_fact,
                        "Price History":priceHistory,
                        "agent_name":agent_name,
                        "agent_number":agent_number,
                        "agent_broke":agent_broke,
                        "agent_pic":agent_pic,
                        "List url" :list_link
                    }
                    # print(pic_arr)
                    # print(facts)
                    # print(home_fact)
                    main_arr.update(main)
                    
                    # print(json.dumps(main_arr, indent=4, sort_keys=True, default=str))
                    
                    obj_zl = result()
                    obj_zl.title = title
                    obj_zl.scraper_id=sid
                    obj_zl.scraper_name=list_name
                    obj_zl.Address = st_address
                    obj_zl.city = city
                    obj_zl.state = state
                    obj_zl.price = price
                    obj_zl.bathrooms = bathrooms
                    obj_zl.Bedrooms = bedrooms
                    obj_zl.zestimate = zestimate
                    obj_zl.list_date = list_date
                    obj_zl.Description = desc
                    obj_zl.Pictures = pic_arr
                    obj_zl.priceHistory=priceHistory
                    obj_zl.rawdata=main_arr
                    obj_zl.Facts = facts
                    obj_zl.home_fact = home_fact
                    obj_zl.agent_name = agent_name
                    obj_zl.agent_number = agent_number
                    obj_zl.agent_broke = agent_broke
                    obj_zl.agent_pic = agent_pic
                    obj_zl.url = list_link
                    obj_zl.save()
                    rec_saved+=1
                    print(' '*30)
                    print('__________'*30)
                    # break
            except:
                import sys
                # print(sys.exc_info())
                lg_msg=sys.exc_info()
                lg_type='ERROR'
                log_obj.dolog('zillow_get',lg_type,lg_msg)
                reqq=False
                continue
    
    message='<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta http-equiv="X-UA-Compatible" content="ie=edge"><meta name="Description" content="Report Of Zillow Bot"/><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.0.0-alpha2/css/bootstrap.min.css"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.0/css/all.min.css"><link rel="stylesheet" href="assets/css/style.css"><title>Zillow Bot Report</title></head><body><table class="table table-borderless">  <thead>    <tr>      <th scope="col">List Name</th>      <th scope="col">URl</th>      <th scope="col">Total Records Saved</th>      <th scope="col">Error</th>    </tr>  </thead>  <tbody>    <tr>      <td>'+str(list_name)+'</td>      <td>'+str(url)+'</td>      <td>'+str(rec_saved)+'</td>      <td>'+str(merror)+'</td>    </tr>  </tbody></table><script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.1/umd/popper.min.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.0.0-alpha2/js/bootstrap.min.js"></script></body></html>'
    obj_email.SendEmail(to_email,subject,message)
    # print(main_arr)
        # return main_arr

# url = ''
# print(zillow_get(url))

def check_status():
    # scobj=Scrapers()
    status=Scraper.objects.filter(status=True,source='zillow')
    if status:
        for s in status:
            if 'zillow' in s.links:
                    print(s.list_name)
                    zillow_get(s.links,s.list_name,s.id)
                    # check_rec()
    else:
        print('NO Scrapper Is up')
        
def test_run():
    print('Tested')
