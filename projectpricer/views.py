from django.shortcuts import render
from .models import AmazonPrice
from django.utils.six.moves.urllib.parse import urlparse

def get_amazon_price(purchased_component):

	item = purchased_component
	item_name = item.purchased_component_name
	item_url = urlparse(item.purchased_component_url_link)
	#If URL is provided and URL is amazon.com, get the item ID out of it, else look up based on item name
	
	if item_url:
		if item_url.netloc == 'www.amazon.com':
			print 'THIS IS AMAZON'
			split_url = item_url.path.split('/')
			item_id = split_url[3]
			print 	split_url[3]

