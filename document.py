class Document:
	class Element:
		def __init__(self, val, window):
			self.val = val
			self.window = window
			
		def innerHTML(self, value=None):
			try:
				if value:
					value = str(value).strip('\'')
					self.window.evaluate_js( f"document.getElementById('{self.val}').innerHTML = \"{value}\"" )
				else:
					return self.window.evaluate_js( f"document.getElementById('{self.val}').innerHTML" )
			except:
				pass

		def __call__(self, attr, value=None):
			try:
				if value:
					value = str(value).strip('\'')
					self.window.evaluate_js( f"document.getElementById({self.val}).{attr} = \"{value}\"" )
				else:
					return self.window.evaluate_js( f"document.getElementById({self.val}).{attr}" )
			except:
				pass


	def __init__(self, window):
		self.window = window
		self.flags = {}

	def get(self, value): 
		return self.Element(value, self.window)

	def eval_js(self, s):
		return self.window.evaluate_js(s)
