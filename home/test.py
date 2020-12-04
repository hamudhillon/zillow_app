from scraper_api import ScraperAPIClient
client = ScraperAPIClient('60d3e592477ebfd328a11e92ce6600c9')
result = client.get(url = 'http://httpbin.org/ip').text
print(result)