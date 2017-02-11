import json
import sys

import requests
from bs4 import BeautifulSoup

class Crawler():
	'''
		class to scrap data from given ecommerce website url.
	'''
	def __init__(self, url):
		self.url = url
		self.soup = None
		self.config = {}
		self.load_content()

	def load_content(self):
		try:
			content = requests.get(self.url).content
		except requests.exceptions.Timeout:
			print 'connection timed out'
			sys.exit(1)
		except requests.exceptions.RequestException as e::
			print 'something wrong with requests',e
			sys.exit(1)
		self.soup = BeautifulSoup(content)

	def set_config(self, config):
		self.config  = config

	def get_items_by_id(self, id):
		'''
		 	method to get items by div or someother element id
		 	id: id of the div or section
		'''
		items = self.soup.find(id=id)
		return items

	def get_items_by_class(self, item_type, item_name):
		'''
			method to get bs4 elements from given type
			item_type : div, nav, table
			item_name : name of the block
		'''
		items = self.soup.findAll(item_type, {"class":item_name})
		return items

	def get_item_value(self, item):
		'''
			method to get title or alternate text from the given item
		'''
		if item:
			value = item.string
			if value is None:
				value = item.get('title') or item.get('alt')
			return value

	def get_item_link(self, item):
		'''
			method to get link from the given bs4 element tag.
		'''
		if item:
			return item.get('href')

	def get_links(self, section):
		'''
			method to get links from div sections. 
			section : section object is beautiful soup element tag
		'''
		if section:
			return section.findAll("a")
		return []
		