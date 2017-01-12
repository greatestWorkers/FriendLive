# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow,unauthenticated_userid
import pymongo

'''
def groupfinder(userid , request):
    conn = pymongo.MongoClient("127.0.0.1" , 27017)
    db = conn.foobar
    coll = db.users
    user = coll.find({"user_id":userid})[0]
    if user:
        print ['g:'+user["is_admin"]]
        return ['g:'+user["is_admin"]]
    return None

class RootFactory(object):
    def __init__(self,request):
        self.__acl__ = []
        self.__acl__.append((Allow,'g:'+ '100' ,"100"))
        self.__acl__.append((Allow,'g:'+ '200' ,"200"))

def get_user(request):
    conn = pymongo.MongoClient("127.0.0.1" , 27017)
    db = conn.foobar
    coll = db.users
    try:
    	user_id = unauthenticated_userid(request)
    	user = coll.find({"user_id":user_id},{"_id":0})[0]
    except NameError:
	return None
    else:
	return user
'''

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    '''
    authn_policy =  AuthTktAuthenticationPolicy(
        'secret' , callback = groupfinder,hashalg = 'sha512'
        )
    authz_policy = ACLAuthorizationPolicy()
    '''

    config = Configurator(settings=settings)

    '''
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.set_request_property(get_user,'user',reify = True)
    '''

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('room','/room')
    config.add_route('user','/user')
    config.add_route('list','/list')
    config.add_route('register','/register')
    config.add_route('log','/log')
    config.add_route('test','/test')
    config.add_route('upload','/upload')
    config.add_route('friend','/friend')
    config.scan()
    return config.make_wsgi_app()
