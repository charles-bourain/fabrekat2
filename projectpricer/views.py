from django.shortcuts import render
from .models import AmazonPrice
from django.utils.six.moves.urllib.parse import urlparse
import bottlenose
from django.conf import settings
from lxml import etree
from pprint import pprint





def get_amazon_price(purchased_component):
	AMAZON_NS = './/{http://webservices.amazon.com/AWSECommerceService/2011-08-01}'
	TAGPOS = len(AMAZON_NS)
	amazon = bottlenose.Amazon(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_ASSOCIATE_TAG)
	item = purchased_component
	item_name = item.purchased_component_name
	item_url = urlparse(item.purchased_component_url_link)
	#If URL is provided and URL is amazon.com, get the item ID out of it, else look up based on item name
	if item_url:
		if item_url.netloc == 'www.amazon.com':
			split_url = item_url.path.split('/')
			item_id = split_url[3]
			xml_response = amazon.ItemLookup(ItemId = item_id, ResponseGroup = 'OfferSummary')
			response = etree.fromstring(xml_response)
			items_response = response[1]
			print etree.tostring(items_response, pretty_print = True)
			pprint([el.tag for el in items_response.iter()])
			price = items_response.find(AMAZON_NS +'Amount')
			print price.text
			currency = items_response.find(AMAZON_NS+'CurrencyCode')
			print currency.text
			return price.text
