
class plugin:

	"""
		Initialization includes assigning:
			A Plugin title
			A Plugin Query (What query triggers the plugin)
			A main function for the plugin to run
			Optional parameters for the function
	"""
	def __init__(self, title, func, query, params=None):
		self.function = func
		self.title = title
		self.query = query
		self.params = params

	"""
		Run plugin main function.
	"""
	def run(self):
		return self.function(*self.params)

	"""
		Return plugin title.
	"""
	def get_title(self):
		return self.title

	"""
		Return trigger query.
	"""
	def get_query(self):
		return self.query

	"""
		Return parameters for the plugin main function.
	"""
	def get_params(self):
		return self.params

	"""
		Overwrite existing parameters to call plugin 
		main function with.
	"""
	def set_params(self, params):
		self.params = params