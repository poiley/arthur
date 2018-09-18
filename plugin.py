
class plugin:
	def __init__(self, title, func, query, params=None):
		self.function = func
		self.title = title
		self.query = query
		self.params = params

	def run(self):
		self.function(*self.params)

	def get_title(self):
		return self.title

	def get_query(self):
		return self.query

	def get_params(self):
		return self.params

	def set_params(self, params):
		self.params = params