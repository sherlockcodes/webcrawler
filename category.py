import urlparse

from crawler import Crawler

class Category():
	def __init__(self, url):
		self.url = url
		self.config = {}
		self.load_config()

	def load_config(self):
		self.config = {"name":{"type":"string"},"url":{"type":"url"},"main_menu":{"path":{"class":{"div":"collapse navbar-collapse navbar-ex1-collapse"}}}}

	def get_categories(self):
		categories = []
		main_menu_config = self.config["main_menu"]["path"]
		del self.config["main_menu"]
		crawler  = Crawler(self.url)
		main_menu = None
		if "id" in main_menu_config:
			main_menu = crawler.get_items_by_id(main_menu_config["id"])
		elif "class" in main_menu_config:
			for item_type, item_name in main_menu_config["class"].iteritems():
				main_menu = crawler.get_items_by_class(item_type, item_name)
		if main_menu:
			if len(main_menu) == 1: 
				main_menu = main_menu[0].findAll('a')
			for category in main_menu:
				item = {}
				for item_name, item_config in self.config.iteritems():
					item_type = item_config["type"]
					if item_type == "string":
						item[item_name] = crawler.get_item_value(category)
					elif item_type == "url":
						category_url = crawler.get_item_link(category)
						if category_url:
							path = urlparse.urlparse(category_url).path
							item[item_name] = self.url + path
				categories.append(item)
		return categories

