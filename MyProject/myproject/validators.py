import re
import pymongo
import formencode

class UniqueName(formencode.FancyValidator):
    def _convert_to_python(self,value,state):
	conn = pymongo.MongoClient("127.0.0.1",27017)
	db = conn["foobar"]
	coll = db["users"]
	if re.search(r'[^a-zA-Z0-9]+',value):
            return {"status":"failed","message":"Invalid input"}
	try:
	    user = coll.find({"user_id":value})[0]
	except IndexError:
	    return None
	else:
	    return {"status":"failed","message":"User existed"}

class ValidInput(formencode.FancyValidator):
    def _convert_to_python(self,value,state):
	if re.search(r'[^a-zA-Z0-9]+',value):
	    return {"status":"failed","message":"existing space"}
	elif len(value)< 6:
	    return {"status":"failed","message":"too short"}
	return value

class ValidPhoneNumber(formencode.FancyValidator):
    def _convert_to_python(self,value,state):
	if re.match(r'^[1-9][0-9]{10,10}',value):
	    return value
	else:
	    return None
