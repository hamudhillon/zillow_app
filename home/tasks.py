from celery import shared_task
from payment_gateways.celery import app

@shared_task
def zillow_scrapper():
    from home.zillow_ui import check_status
    check_status()

@shared_task
def check_zillowrecords():
    from home.zillow_ui import check_rec
    check_rec()
    
    
@app.task()
def get_craigslists():
    from utilities.process_file import get_craigslists
    get_craigslists()

    
    