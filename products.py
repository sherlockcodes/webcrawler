import urlparse

from crawler import Crawler

class Products():
	def __init__(self, category):
		self.category_url = ""
		self.category_name = ""
		if "url" in category:
			self.category_url = category["url"]
		if "name" in category:
			self.category_name = category["name"]
		self.crawler  = Crawler(self.category_url)
		self.config = {}
		self.load_config()

	def load_config(self):
		# config will be loaded from data/customer_website_name/products.json
		self.config = {"name":{"type":"string","position":1},"url":{"type":"url","position":0},"image":{"type":"image","position":0},"products_section":{"path":{"class":{"div":"product-block"},"multi_link":True}}}
		self.products_section_config = self.config["products_section"]
		del self.config["products_section"]

	def get_products(self):
		products = []
		products_section = self.__get_products_section()
		if products_section:
			for product in products_section:
				item = {}
				if "multi_link" in self.products_section_config["path"]: # if multi_link is set, every product block have multiple link section with image, href, and name
					links = self.crawler.get_links(section=product)
					for item_name, item_config in self.config.iteritems():
						item_type = item_config["type"]
						item_class = item_config.get("class",None)
						position = item_config.get("position",None) # position in which link have title or alternate text
						if item_type == "string" and position and len(links) >= position:
							item[item_name] = self.crawler.get_item_value(links[position])
						elif item_type == "url" and position and len(links) >= position:
							product_url = self.crawler.get_item_link(links[position])
							if product_url:
								path = urlparse.urlparse(product_url).path
								base_url = urlparse.urlparse(self.category_url).netloc
								item[item_name] = base_url + path
						elif item_type == "image" and position is not None and len(links) >= position:
							images = self.crawler.get_images(links[position])
							if images and len(images):
								item[item_name] = self.crawler.get_item_image(images[0])
								
				else:
					for item_name, item_config in self.config.iteritems():
						item_type = item_config["type"]
						if item_type == "string":
							item[item_name] = self.crawler.get_item_value(product)
						elif item_type == "url":
							product_url = self.crawler.get_item_link(product)
							if product_url:
								path = urlparse.urlparse(product_url).path
								item[item_name] = self.url + path
				item.update({"category_url":self.category_url,"category":self.category_name})
				products.append(item)
		return products

	# private methods
	def __get_products_section(self):
		'''
			private method to get products section.
		'''
		products_section = []
		if "id" in self.products_section_config["path"]:
			products_section = self.crawler.get_items_by_id(self.products_section_config["path"]["id"])
		elif "class" in self.products_section_config["path"]:
			for item_type, item_name in self.products_section_config["path"]["class"].iteritems():
				products_section = self.crawler.get_items_by_class(item_type, item_name)
		return products_section

