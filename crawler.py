import json

import requests
from bs4 import BeautifulSoup

class Crawler():
	def __init__(self, url):
		self.url = url
		self.soup = None
		self.config = {}
		self.load_content()

	def load_content(self):
		content = requests.get(self.url).content
		self.soup = BeautifulSoup(content)

	def set_config(self, config):
		self.config  = config

	def get_items_by_id(self, id):
		items = self.soup.find(id=id)
		return items

	def get_items_by_class(self, item_type, item_name):
		items = self.soup.findAll(item_type, {"class":item_name})
		return items

	def get_item_value(self, item):
		if item:
			value = item.string
			if value is None:
				value = item.get('title') or item.get('alt')
			return value

	def get_item_link(self, item):
		if item:
			return item.get('href')

	def get_links(self, section):
		if section:
			return section.findAll("a")
		return []
		