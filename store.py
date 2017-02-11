from category import Category
from products import Products

class Store():
	def __init__(self, url):
		self.url = url
		self.category = Category(self.url)

	def get_categories(self):
		return self.category.get_categories()

	def get_products(self, category):
		self.products = Products(category).get_products()
		return self.products
