# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.view import view_defaults
from pili import *
from pyramid.response import Response
from pyramid.security import remember , forget
from pyramid.httpexceptions import HTTPFound,HTTPNotFound
from mongodb_connect import *
from auth import *
import shutil , os , sys , validators , hashlib , time , random , json , requests
import pymongo

access_key = "TUo-Zhi8ICQGKqHVuIzL1rYdb5itNEF4F6fQzJjr"
secret_key = "n0pp6ksP4TNEWZaVGfV4B6jLJIRkIt9G44Vk3R9R"
hub_name = "mrpyq"

pyc = PyConnect("127.0.0.1",27017)
pyc.use('foobar')
pyc.setCollection('users')

@view_config(route_name = 'home')
def my_home(request):
    return Response("test")

@view_defaults(route_name='room',renderer='json')
class room_logic(object):
    def __init__(self,request):
        self.request = request
    
    #创建房间
    @view_config(request_method = 'GET')
    @auth_interface
    def create_room(self,**args):

        #向七牛直播空间申请推流stream，并将其以json格式返回
        credentials = Credentials(access_key,secret_key)
        hub = Hub(credentials,hub_name)
        stream = hub.create_stream(title=None , publishKey=None , 
                    publishSecurity="static")
        pilipili = {}
        if(stream):
            userid = self.request.user["userid"]
            pilipili['room_id'] = stream.id
            pilipili['publish_url'] = stream.rtmp_publish_url()
            pilipili['play_url'] = stream.rtmp_live_urls()
            pilipili['title'] = stream.title
            pilipili['live_status']= 'on' 
            pyc.update({"user_id":userid},pilipili)

        return json.loads(stream.to_json())

    #关闭房间
    @view_config(request_method = 'DELETE')
    def my_exitroom(self):
        
        #主播离开房间，删除相对应的stream，更新数据库

        credentials = Credentials(access_key,secret_key)
        hub = Hub(credentials,hub_name)

        userid = self.request.user["user_id"]
        roomid = pyc.find({"user_id":userid},{"_id":0})[0]["room_id"]
        stream = hub.get_stream(stream_id = roomid)

        try:
            stream.delete()
        except Exception,e:
            if(pyc.find({"room_id":roomid})[0]):
                print 'dead stream'
                pyc.update({"user_id":userid},{"live_status":"off"})
            return Response('0')
        else:
            pyc.update({"user_id":userid},{"live_status":"off"},True)
            return Response('1')


@view_defaults(route_name = 'Livelist' , renderer = 'json')
class Live_list(object):
    def __init__(self,request):
        self.request = request

    @view_config(request_method = 'GET')
    def Newest(self):

        #列出所有活跃的直播流
        pilipili = {}
        pilipili['count']= 0
        pilipili['list']= []

        cursor = pyc.find({"live_status":"on"},{"_id":0,"live_status":0})
        for s in  cursor:
            pilipili['list'].append(s)
            pilipili['count']+= 1
        return Response(json.dumps(pilipili , ensure_ascii = False))
'''
@view_config(route_name = 'Logout')
@connect_mongodb
def account_logout(request,pyc):

    #注销账户，删除数据前需先从七牛删除相应的steam
    credentials = Credentials(access_key,secret_key)
    hub = Hub(credentials,hub_name)

    userid = request.matchdict["userid"]
    roomid = pyc.find({"useridx":userid},{"_id":0})[0]["roomid"]
    stream = hub.get_stream(stream_id = roomid)
    try:
        stream.delete()
    except Exception,e:
        if(pyc.find({"roomid":roomid},{"_id":0})[0]["roomid"]):
            print 'dead stream'
            pyc.remove({"useridx":userid})
        exit(0)
    else:
    	pyc.remove({"useridx":userid})
    	return Response("logout")
'''


@view_defaults(route_name = 'user')
class User_logic(object):
    def __init__(self,request):
        self.request = request

    @view_config(request_method = 'GET',renderer = 'templates/login.pt')
    def login_view(self):
        login_url = self.request.route_url('user')
        referrer = self.request.url
        if referrer == login_url:
            referrer = '/' # never use the login form itself as came_from
        came_from = self.request.params.get('came_from', referrer)
        message = ''
        login = ''
        password = ''
        if 'form.submitted' in self.request.params:
            login = self.request.params['login']
            password =self.request.params['password']
        try:
            user = pyc.find({"user_id":login},{"_id":0})[0]
        except IndexError as e:
            message = 'User does not exist'
	else:
            if user["user_password"] == password:
                token = auth.encode(login,time.time()+888)
                pyc.update({"user_id":login},{"user_token":token})
                login = token
                return HTTPFound(location = came_from)
                #return Response(json.dumps(user,ensure_ascii = False))
            else:
                message = 'Password does not match'

        return dict(
            message = message,
            url = self.request.application_url + '/user',
            came_from = came_from,
            login = login,
            password = password,
            )    

    #注销
    @view_config(request_method = 'DELETE')
    def logout_view(self):
        headers = forget(self.request)
        return HTTPFound(location = '/list' , headers = headers)

    #修改个人信息
    @view_config(request_method = "POST",renderer = 'templates/signup.pt') 
    def edit_information(self): 
	base_path = os.path.abspath('.')
	seq = base_path.split('/')
	path = '/'.join([base_path,seq[-1].lower(),'static'])
        '''
        validator1 = validators.ValidInput()
        validator2 = validators.UniqueName()
        login = validator2.to_python(self.request.params.get("login",None))
        passwd = validator1.to_python(self.request.params.get("passwd",None))
        '''

        city = self.request.params.get("passwd",None)
        nick_name = self.request.params.get("nick_name",None)
	
	field = self.request.POST['img']
	input_file = field.file
	
        if 'submit' in self.request.params:
            temp = {"point":0}
            temp["user_id"]= login
            temp["user_passward"]= passwd
            temp["user_birthday"]= self.request.params.get("birth",None)
            temp["user_city"]= city
            temp["user_email"]= self.request.params.get("email",None)
            temp["user_gender"]= self.request.params.get("gender",None)

	    #保存头像到项目的static asset
	    file_path = '/'.join([path,'user_imgs',login+'.png'])
	    try:
	        with open(path,'wb') as output_file:
		    shutil.copyfileobj(input_file,output_file)
	    except IOError:
		print '写入文件失败'
		return Response({status:'failed'})
            temp["user_img"]=  file_path

            temp["user_nick_name"]= nick_name 
            temp["user_phone"]= self.request.params.get("phone",None)
            temp["user_token"]= self.request.params.get("token",None)
            temp["is_admin"]= self.request.params.get("permissin",None)
	    temp["user_subscribe"]= []
	    temp["user_fans"]= []
	    temp["user_gifts"]= {}
        pyc.update({'user_id':login},temp)
        #return Response({"status":"success"})
        return {
            "login":login,
            "nick_name":nick_name,
            "passwd":passwd,
            "city":city
        }
'''
    #获取订阅列表和粉丝列表
    @view_config(request_method = 'HEAD')
    @auth_interface
    def subscribe_fans_list(self,**kws):
	if self.request.params.get('ask',None)== 'subscribe_list':
	    return Response(pyc.find({'user_id':kws['userid']},
		{"user_subscribe":1}))
	elif self.request.params.get('ask',None)== 'fans_list':
	    return Response(pyc.find({'user_id':kws['userid']},
                {"user_fans":1}))
	else:
	    return Response({'status':'failed'})

    #订阅和取消订阅
    @view_config(request_method = 'PUT')
    @auth_interface
    def subscribe_unsubscribe(self,**kws):
	list = pyc.find({'user_id':kws['userid']},
                {"user_subscribe":1})
	if self.request.params.get('ask',None)== 'subscribe':
	    list.append(request.params.get('anchorman',None))
	    pyc.update({"user_id":kws["userid"]},{"user_subscribe":list})
	elif self.request.params.get('ask',None)== 'unsubscribe':
	    list.remove(request.params.get('anchorman',None))
	    pyc.update({"user_id":kws["userid"]},{"user_subscribe":list})
	else:
	    return Response({'status':'failed'})

    #搜索主播
    @view_config(request_method = 'HEAD')
    @auth_interface
    def search_anchorman(self,**kws):
	try:
            user = pyc.find({"user_id":request.params.get("userid",None)},
		{"_id":0})[0]
	except IndexError:
	    return Response({"status":"the anchorman does not exist"})
	else:
	    return Response(json.dumps(user,ensure_ascii=False))
'''

@view_config(route_name = 'test')
def upload(request):
    base = "/env/workspace/PyramidProject/MyProject/myproject/static/user_imgs"
    filename = request.POST['img'].filename
    file_path = '/'.join([base,filename])
    input_file = request.POST['img'].file
    login = request.params.get("login",None)
    with open(file_path,'wb') as output_file:
	shutil.copyfileobj(input_file,output_file)
    path = os.path.abspath('.')
    application_path = request.application_url
    print path ,'\n',application_path
    return Response(json.dumps({"sus":login},ensure_ascii = False))



#手机号码注册功能
@view_defaults(route_name = 'register')
class register(object):
    def __init__(self,request):
	self.request = request

    def send_sms_chuanglan(self,phone,code):
	account = "jk_cs_cs1"
	password = "Chuanglan888"

	msg = u'您好，您本次的注册验证码是%s'%(code)
	host = "sapi.253.com"
	sms_send_uri = "/msg/HttpBatchSendSM"

	data = {
	    'account':account,
	    'pswd':password,
	    'msg':msg,
	    'mobile':phone,
	    'needstatus':'false',
	    'extno':''
	}
	headers = {
	    "Content-type":"application/x-www-form-urlencoded",
	    "Accept":"text/plain"
	}
	url = 'http://%s%s'%(host,sms_send_uri)

	#使用会话对象提升性能,verify表示是否验证ssl证书（默认为true）
	r = requests.session().request('POST',url,verify=False,
		headers=headers,data=data,)
	print r.content
	if r.ok:
	    content = r.content.split(',')
	    print content
	    #测试，返回了错误码说明接口可用
	    if len(content) == 2 and len(content[0])>0:
		return True,str(content[0])
	return False,None

    @view_config(request_method = 'GET')
    def send_code(self):
	phone_number = self.request.params.get('userId',None)
	code = int(random.random()*10000)

	#调用运营商提供的接口向此手机号发送验证码
	res = self.send_sms_chuanglan(phone_number,code)
	print code
	if res[0] and res[1]== 0:
	    return Response(str(code))
	else:
	    print res[1]
	    return Response('0')
    @view_config(request_method = 'POST')
    def verify_code(self):
	code_v = int(self.request.params.get('code_v',None))
	code = int(self.request.params.get('code',None))
	if code_v == code:
	    return Response('1')
	else:
	    return Response('0')
    @view_config(request_param = "register=1",request_method = 'POST') 
    def sign_up(self): 
	temp = {} 
	userId = request.params.get("userId",None) 

	base_path = os.path.abspath('.')
	seq = base_path.split('/')
	path = '/'.join([base_path,seq[-1].lower(),'static'])
	filename = '.'.join([self.phone_number,request.POST['img'].filename.split('.')[1]]) 
	file_path = '/'.join([path,'imgs',filename]) 
	input_file = request.POST['img'].file 
	with open(file_path,'wb') as output_file: 
	    shutil.copyfileobj(input_file,output_file) 
	
	headImage = file_path

	password = self.params.get("password",None)
	gender = self.params.get("gender",None)
	nickname = self.params.get("nickname",None) 
	token = None 
	LiveStatus = 0
	isAdmin = 0
	
	temp["userId"]= userId
	temp["password"]= password
	temp["gender"]= gender
	temp["nickname"]= nickname
	temp["isAdmin"]= isAdmin
	temp["headImage"]= headImage

	pyc.update({"userId":userId},temp)

#登录和注销功能
@view_defaults(route_name = 'log')
class SignInOut(object):
    def __init__(self,request):
	self.request = request
	self.token = request.params.get('token',None)
	self.login = request.params.get('userid',None)
	self.passwd = request.params.get('password',None)

    def check_token(token):
    	try:
	    user = pyc.find({"userId":event.login},{"_id":0})[0] 
	except IndexError:
	    return 1
	if self.passwd != user["password"]:
	    return 2
	token = auth.encode(event.login,
		     time.time()+ event.request.params.get('expire_in',None))
	pyc.update({"user_id":self.login},{"user_token":token})
	return 0

    def sign_in(self,request_method = 'GET')
	res = self.check_token(self.token)
	if res == 0:
	    return Response("登录成功")
	if res == 1:
	    return Response("用户不存在")
	if res == 2:
	    return Response("密码错误")
	
    @view_config(request_method = 'DELETE')
    def logout(self):
	pass

