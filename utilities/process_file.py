import os
import sys
rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(rootPath)
os.environ["DJANGO_SETTINGS_MODULE"] = "payment_gateways.settings"
import django
django.setup()

# ============================================================
from utilities.craigslist import ScraperHandler
from utilities.LogHandler import DologHandler
from home.models import Scraper

def get_craigslists():
    """Main Process Function"""
    logger = DologHandler('craigslist','file')
    status=Scraper.objects.filter(status=True,source ='craigslist')
    lg_type = 'INFO'
    lg_msg = 'Process has '+str(len(status))+' objects to process'
    logger.dolog('getAllcraigslist',lg_type,lg_msg)
    if status:
        for s in status:
            if 'craigslist' in s.links:
                    craigslist_url = s.links
                    objSH = ScraperHandler(craigslist_url,     s.id,   s.list_name,logger)
                    objSH.getAllcraigslist()
        lg_type = 'INFO'
        lg_msg = 'Process Comleted Successfully!'
        logger.dolog('getAllcraigslist',lg_type,lg_msg)
    else:
        lg_type = 'INFO'
        lg_msg = 'No Lists Found To Process having status True'
        logger.dolog('getAllcraigslist',lg_type,lg_msg)
        
# get_craigslists()
# craigslist_url = 'https://orlando.craigslist.org/search/rea?s=0'
