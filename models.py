from flask.ext.login import UserMixin

class User(UserMixin):
	def __init__(self,teamname,names,languages,email,password):
		self.email=email
		self.password=password
	def get_id(self):
		return unicode(self.email)
