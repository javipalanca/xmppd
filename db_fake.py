# Distributed under the terms of GPL version 2 or any later
# Copyright (C) Alexey Nezhdanov 2004
# AUTH_db interface example for xmppd.py

# $Id: db_fake.py,v 1.4 2004/10/24 04:49:09 snakeru Exp $

from xmpp import *
import os

try:
	from xml.marshal.generic import *
	marshal = Marshaller()
	unmarshal = Unmarshaller()
except:
	pass

db={}
#db['localhost']={}
#db['thx1138.dsic.upv.es']={}
#db['__admin__']={}
#db['localhost']['test']='test'
#db['localhost']['test2']='test'
#db['localhost']['gusarba']='kakatua'
#db['localhost']['jpalanca']='kakatua'
#db['localhost']['acc']='secret'
#db['localhost']['ams']='secret'
#db['localhost']['df']='secret'
#db['localhost']['rma']='secret'
#db['localhost']['ping']='secret'
#db['thx1138.dsic.upv.es']['gusarba']='kakatua'
#db['thx1138.dsic.upv.es']['jpalanca']='kakatua'
#db['thx1138.dsic.upv.es']['test']='test'
#db['thx1138.dsic.upv.es']['acc']='secret'
#db['thx1138.dsic.upv.es']['ams']='secret'
#db['thx1138.dsic.upv.es']['df']='secret'
#db['thx1138.dsic.upv.es']['rma']='secret'
#db['thx1138.dsic.upv.es']['ping']='secret'
#db['__admin__'] = ['gusarba']

class AUTH(PlugIn):
    NS=''
    def getpassword(self, username, domain):
        try: return db[domain][username]
        except KeyError: pass

    def isuser(self, username, domain):
        try: return db[domain].has_key(username)
        except KeyError: pass

    def isadmin(self, username):
	try:
		global db
		if username in db['__admin__']:
			return True
		else:
			return False
	except:
		pass

class DB(PlugIn):
    NS=''
    def store(self,domain,node,stanza,id='next_unique_id'): pass
    def plugin(self, server):
	global db
	self.userdbfile = server.spoolpath + os.sep + 'user_db.xml'
	try:
		if self.loaddb():
			print '#### DB: User database loaded'
		else:
			print '#### DB: Could NOT load user database. Building own'
			try:
				for name in server.servernames:
					db[name] = {}
				db['__admin__'] = {}
				if self.savedb():
					print '#### DB: User database built and saved'
				else:
					print '#### DB: Could not save built database'
			except:
				print '#### DB: Could not build user database. We are all doomed!'

	except:
		pass

    def registeruser(self,domain,username,password):
	try:
		db[domain][str(username)] = str(password)
		self.savedb()
		#print "#### Trying to save database"
		return True
	except:
		return False

    def printdb(self):
	print db

    def savedb(self):
	try:
		global db
		print "#### userdbfile = " + str(self.userdbfile)
		print "#### spoolpath = " + str(server.spoolpath)
		if not os.path.exists(server.spoolpath):
			print "#### SpoolPath does no exist!!!"
			p = server.spoolpath.split(os.sep)
			tmpitem=""
			print "#### p = " + str(p)
			for item in p:
				tmpitem+=str(item)
				if not os.path.exists(tmpitem):
					print "#### mkdir " + str(tmpitem)
					os.mkdir(tmpitem)
		print "#### open " + str(self.userdbfile)
		fh = open(self.userdbfile, 'w')
		marshal.dump(db, fh)
		fh.close()
		print '#### savedb: User database saved!'
		return True
	except:
		print '#### savedb: Could not save user database'
		return False

    def loaddb(self):
	try:
		global db
		fh = open(self.userdbfile, 'r')
		db = unmarshal.load(fh)
		fh.close()
		print '#### loaddb: User database loaded'
		return True
	except:
		print '#### loaddb: Could not load user database'
		return False

    def listdb(self):
	try:
		global db
		return str(db)
	except:
		pass

