from .models import Product
from django.utils.six.moves.urllib.parse import urlparse
import bottlenose
from django.conf import settings
from lxml import etree
from pprint import pprint
from .forms import ProductForm
import re
from datetime import datetime


def get_product(request, purchased_component_url_link, purchased_component_name):
    item_name = purchased_component_name
    item_url = urlparse(purchased_component_url_link)
    #If URL is provided and URL is amazon.com, get the item ID out of it, else look up based on item name
    if item_url:
        if item_url.netloc == 'www.amazon.com':
            item_id = find_amazon_item_id(item_url.path)    
            try:
                product = Product.objects.get(asin = item_id) #Returns product object      
            except:
                product_info = product_info_from_amazon(item_id)
                product = assign_values_to_product_model(request, product_info) #Returns product object
                print 'Product: ', product, type(product), product.id

    return product


def product_info_from_amazon(item_id):
    AMAZON_NS = './/{http://webservices.amazon.com/AWSECommerceService/2011-08-01}'
    amazon = bottlenose.Amazon(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_ASSOCIATE_TAG, MaxQPS=0.9)
    xml_response = amazon.ItemLookup(ItemId = item_id, ResponseGroup ='OfferListings')
    xml_response_itemattributes = amazon.ItemLookup(ItemId = item_id, ResponseGroup ='ItemAttributes')
    response = etree.fromstring(xml_response)
    response_itemattributes = etree.fromstring(xml_response_itemattributes)
    items_response = response[1]
    itemattributes_response = response_itemattributes[1]
    price = items_response.find(AMAZON_NS +'Amount').text
    currency = items_response.find(AMAZON_NS+'CurrencyCode').text
    asin = str(item_id)
    upc = itemattributes_response.find(AMAZON_NS + 'UPC').text
    ean = itemattributes_response.find(AMAZON_NS + 'EAN').text
    name = itemattributes_response.find(AMAZON_NS + 'Title').text
    referral_url = itemattributes_response.find(AMAZON_NS+'DetailPageURL').text
    return_dict = {
        'price':price,
        'currency':currency,
        'asin':asin,
        'upc':upc,
        'ean':ean,
        'name':name,
        'url':referral_url,
        }
    return return_dict


def assign_values_to_product_model(request, product_info):
    productform = ProductForm(request.POST,)
    if productform.is_valid():
        productform = productform.save(commit=False)
        productform.asin = product_info['asin']
        productform.currency = product_info['currency']
        productform.upc = product_info['upc']
        productform.ean = product_info['ean']
        productform.name = product_info['name']
        productform.price = product_info['price']
        productform.url = product_info['url']
        productform.last_updated = datetime.now()
        productform.save()
        product = Product.objects.get(asin = product_info['asin'])
        print 'Product ID: ', product.id
        return product


def find_amazon_item_id(parse_path):
    item_id_compiler = re.compile(r'/[A-Z0-9]{10}[%|/]')
    item_id = item_id_compiler.search(parse_path).group()
    item_id = item_id.strip('/').strip('%')
    return item_id