import time
from store import Store

url = 'http://www.tiekart.com/'
store = Store(url)
categories = store.get_categories()
print 'total categories', len(categories) , ' in ' + url
time.sleep(5)
for category in categories:
  if "name" in category:
  	print 'getting products for ', category["url"]
  products = store.get_products(category)
  print 'totally ' + str(len(products)) + ' products in the ' + str(category["name"])+ " category"
  time.sleep(3)
  for product in products:
  	print product
