import urlparse

from crawler import Crawler

class Category():
	def __init__(self, url):
		self.url = url
		self.config = {}
		self.crawler  = Crawler(self.url)
		self.load_config()

	def load_config(self):
		self.config = {"name":{"type":"string"},"url":{"type":"url"},"main_menu":{"path":{"class":{"div":"collapse navbar-collapse navbar-ex1-collapse"}}}}
		self.main_menu_config = self.config["main_menu"]
		del self.config["main_menu"]

	def get_categories(self):
		categories = []
		main_menu = self.__get_main_menu()
		if main_menu:
			if len(main_menu) == 1: 
				main_menu = main_menu[0].findAll('a')
			for category in main_menu:
				item = {}
				for item_name, item_config in self.config.iteritems():
					item_type = item_config["type"]
					if item_type == "string":
						item[item_name] = self.crawler.get_item_value(category)
					elif item_type == "url":
						category_url = self.crawler.get_item_link(category)
						if category_url:
							path = urlparse.urlparse(category_url).path
							item[item_name] = self.url + path
				categories.append(item)
		return categories

	def __get_main_menu(self):
		main_menu = []
		if "id" in self.main_menu_config["path"]:
			main_menu = self.crawler.get_items_by_id(self.main_menu_config["path"]["id"])
		elif "class" in self.main_menu_config["path"]:
			for item_type, item_name in self.main_menu_config["path"]["class"].iteritems():
				main_menu = self.crawler.get_items_by_class(item_type, item_name)
		return main_menu

