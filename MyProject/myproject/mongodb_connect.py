# -*- coding: utf-8 -*-
import pymongo

class PyConnect(object):
     
    def __init__(self, host, port):
        #conn 类型<class 'pymongo.connection.Connection'>
        try:
            self.conn = pymongo.MongoClient(host, port)
        except  Error:
            print 'connect to %s:%s fail' %(host, port)
            exit(0)
    '''
    def __del__(self):
        self.conn.close()
    '''
    def use(self, dbname):
        # 这种[]获取方式同样适用于shell,下面的collection也一样
        #db 类型<class 'pymongo.database.Database'>
        self.db = self.conn[dbname]
 
    def setCollection(self, collection):
        if not self.db:
            print 'don\'t assign database'
            exit(0)
        else:
            self.coll = self.db[collection]
    
    #查询数据，query查寻条件，showkey为指定健值
    def find(self, query = {},showkey = {}):
        if type(query) is not dict or type(showkey) is not dict :
            print 'the type of query isn\'t dict'
            exit(0)
        try:
            #result类型<class 'pymongo.cursor.Cursor'>
            if not self.coll:
                print 'don\'t assign collection'
            else:
                result = self.coll.find(query,showkey)
        except Exception:
            print 'some fields name are wrong in ',query
            exit(0)
        return result
    
    #插入数据
    def insert(self, data):
        if type(data) is not dict:
            print 'the type of insert data isn\'t dict'
            exit(0)
        self.coll.insert(data)

    #删除指定数据
    def remove(self,data):
	if type(data) is not dict:
	    print 'the type of remove dadta isn\'t dict'
	    exit(0)
	result = self.coll.delete_one(data)
	return result.deleted_count

    #更新数据
    def update(self,query = {},data={},flag= 0):
	if type(query) is not dict or type(data) is not dict:
	    print 'the type of update isn\'t dict'
	    exit(0)
	#$set
	if flag == 0:
	    self.coll.update(query,{'$set':data},True)
	#$addToSet
	if flag == 1:
	    self.coll.update(query,{'$addToSet':data})
	#$pull
	if flag == 2:
	    self.coll.update(query,{'$pull':data})
