from math import ceil
from hashlib import sha512
from utils import sum_reward
from config import MAX_PROGRAMS_PER_PAGE

from dbinstance import db

class Programs(db.Model):
	# __table__ = db.Model.metadata.tables['programs']
	id = db.Column(db.Integer, primary_key=True)
	company = db.Column(db.String(50))
	link = db.Column(db.String(250))
	lab = db.Column(db.String(50))
	date = db.Column(db.String(50))

	def __init__(self, company, link, lab, date):
		self.company = company
		self.link = link
		self.lab = lab
		self.date = date

	@staticmethod
	def get_by_date():
		return Programs.query.with_entities(Programs.id, Programs.company, Programs.link, Programs.lab, Programs.date).order_by(Programs.date.desc()).all()

	''' Get programs | pagination 
		p: page number
		max_rows: max rows per page
	'''
	@staticmethod
	def get_by_date_limit(p):
		max_rows = MAX_PROGRAMS_PER_PAGE
		npage = ceil(Programs.count()/max_rows)
		p = npage if p > npage else p
		row = (p-1)*max_rows
		return Programs.query.with_entities(Programs.id, Programs.company, Programs.lab, Programs.link, Programs.date).order_by(Programs.date.desc()).limit(max_rows).offset(row).all()	

	@staticmethod
	def count():
		return Programs.query.count()

	@staticmethod
	def get_last_page():
		return ceil(Programs.count()/MAX_PROGRAMS_PER_PAGE) 

	@staticmethod
	def search(program, lab=None):
		if not lab:
			return Programs.query.with_entities(Programs.id, Programs.company, Programs.link, Programs.lab, Programs.date).filter(Programs.company.like("%{}%".format(program))).all()
		else:
			return Programs.query.with_entities(Programs.id, Programs.company, Programs.link, Programs.lab, Programs.date).filter(\
				Programs.company.like("%{}%".format(program))).filter(\
				Programs.lab.in_(lab)).all()	

class Bounties(db.Model):
	# __table__ = db.Model.metadata.tables['bounties']
	id = db.Column(db.Integer, primary_key=True)
	vuln = db.Column(db.String(50))
	title = db.Column(db.String(250))
	description = db.Column(db.Text())
	award = db.Column(db.String(50))
	status = db.Column(db.String(50))


	def __init__(self, vuln, title, description, award, status):
		self.vuln = vuln
		self.title = title
		self.description = description
		self.award = award
		self.status = status

	@staticmethod
	def count():
		return Bounties.query.count()

	@staticmethod
	def exist(id):
		return True if Bounties.query.filter(Bounties.id == id).count() == 1 else False

	@staticmethod
	def get():
		return Bounties.query.with_entities(Bounties.id, Bounties.vuln, Bounties.title, Bounties.description, Bounties.award, Bounties.status).all()

	@staticmethod
	def get_by_id(id):
		return Bounties.query.with_entities(Bounties.id, Bounties.vuln, Bounties.title, Bounties.description, Bounties.award, Bounties.status).filter(Bounties.id == id).all()

	@staticmethod
	def set_status(status, id):
		Bounties.query.filter(Bounties.id == id).update({'status':status})
		db.session.commit()

class Targets(db.Model):
	# __table__ = db.Model.metadata.tables['targets']

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50))
	description = db.Column(db.Text())
	date = db.Column(db.String(50))
	priority = db.Column(db.Integer)

	def __init__(self, title, description, priority):
		self.title = title
		self.description = description
		self.priority = priority

	@staticmethod
	def count():
		return Targets.query.count()

	@staticmethod
	def get():
		return Targets.query.with_entities(Targets.id, Targets.title, Targets.description, Targets.priority).all()

	@staticmethod
	def get_by_id(id):
		return Targets.query.with_entities(Targets.id, Targets.title, Targets.description, Targets.priority).filter(Targets.id == id).all()

class Xss(db.Model):
	# __table__ = db.Model.metadata.tables['xss']

	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.Text())
	screenshot = db.Column(db.Text())
	ip = db.Column(db.String(50))
	domhtml = db.Column(db.Text())
	cookie = db.Column(db.Text())
	useragent = db.Column(db.Text())

	def __init__(self, url, screenshot, ip, domhtml, cookie, useragent):
		self.url = url
		self.screenshot = screenshot
		self.ip = ip
		self.domhtml = domhtml
		self.cookie = cookie
		self.useragent = useragent


	@staticmethod
	def count():
		return Xss.query.count()

	@staticmethod
	def get():
		return Xss.query.with_entities(Xss.id, Xss.url, Xss.screenshot, Xss.ip, Xss.domhtml, Xss.cookie, Xss.useragent).all()


class Users(db.Model):
	# __table__ = db.Model.metadata.tables['users']

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50))
	password = db.Column(db.String(50))

	def __init__(self, username, password):
		self.username = username
		self.password = password

	@staticmethod
	def count():
		return Users.query.count()

	@staticmethod
	def get():
		return Users.query.with_entities(Users.id, Users.username, Users.password).all()

	@staticmethod
	def check_login(username, password):
		return True if Users.query.filter(Users.username == username, Users.password == sha512(password).hexdigest() ).count() > 0 else False



class Info():
	def __init__(self):
		self.nprograms = Programs.count()
		self.nbounties = Bounties.count()
		self.ndollars = sum_reward(Bounties.get())
		self.nxss = Xss.count()
		self.ntargets = Targets.count()

	def __str__(self):
		return "Nbounties: {} $:{} nXss:{} nTarget: {}".format(self.nbounties, self.ndollars, self.nxss, self.ntargets)


"""

if __name__ == '__main__':
	# print Users.check_login('admi', sha1('admin').hexdigest() )
	# Users.query.filter(Users.id==1).update(dict(username='admin'))
	# db.session.commit()
	# print Users.get()
	# print Targets.count()
	# user = Users('admin2', sha1('admin').hexdigest())
	# db.session.add(user)
	# db.session.commit()

	# print Programs.get_by_date()
	# print Programs.get_by_date_limit(1, 20)
	# print Users.count()
	# print Users.get()
	# print Programs.get_by_date()
	# print Programs.query.with_entities().all()
	# print Bounties.query.with_entities(Bounties.id, Bounties.vuln, Bounties.title, Bounties.description, Bounties.award, Bounties.status).all()
	# for program in programs:
	# 	print "ID: {}\n\t{}\n\t{}".format(program.id, program.company, program.lab)
"""