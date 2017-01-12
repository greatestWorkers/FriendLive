# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.view import view_defaults
from pili import *
from pyramid.response import Response
from pyramid.security import remember , forget
from pyramid.httpexceptions import HTTPFound,HTTPNotFound
from mongodb_connect import *
from auth import *
import logging , shutil , os , sys , validators , hashlib , time , random , json , requests
import pymongo

access_key = "TUo-Zhi8ICQGKqHVuIzL1rYdb5itNEF4F6fQzJjr"
secret_key = "n0pp6ksP4TNEWZaVGfV4B6jLJIRkIt9G44Vk3R9R"
hub_name = "mrpyq"

pyc = PyConnect("127.0.0.1",27017)
pyc.use('foobar')


@view_config(route_name = 'home')
def my_home(request):
    return Response("change")

class APIError(Exception):
    '''
    the base APIError which contains error(required), data(optional) and message(optional).
    '''
    def __init__(self, error, data='', message=''):
        super(APIError, self).__init__(message)
        self.error = error
        self.data = data
        self.message = message


#手机号码注册功能
@view_defaults(route_name = 'register')
class register(object):
    def __init__(self,request):
	self.request = request

    def createPhoneCode(self):
	chars = ['0','1','2','3','4','5','6','7','8','9']
	x = random.choice(chars),random.choice(chars),random.choice(chars),random.choice(chars)
	verifyCode = ''.join(x)
	return verifyCode

    def send_sms_changzhuo(self,phone,code):
	#畅卓科技
	account = ''
	password = ''

	if phone.find('+')>= 0:
	    acount = ''
	    password = ''
	    content = 'Dear user,your verification code is %s [MingPeng]'%code
	content = '您的验证码是%s[名人朋友圈]'%code

	m = hashlib.md5()
	m.update(password)

	data = {
	    'account':account,
	    'password':m.hexdigest().upper(),
	    'mobile':phone,
	    'content':content,	    
	}


	r = requests.post('http://api.chanzor.com/send',data = data)
	if r.ok:
	    resp = r.json()
	    if resp.get('status')== 0:
		return True,str(resp.get('taskId'))
	    else:
		raise APIError(-1,u'发送手机验证码错误:%s'%resp.get('desc'),
			 self.request.path)
	return False,None

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
	if r.ok:
	    content = r.content.split(',')
	    print content
	    sys.stdout.flush() 
	    #测试，返回了错误码说明接口可用
	    if len(content) == 2 and len(content[0])>0:
		return True,str(content[1])
	return False,None


    @view_config(request_method = 'GET',renderer = 'json')
    def send_code(self):
	phone_number = self.request.params.get('userId',None)
	try:
	    pyc.setCollection("users")
	    user = pyc.find({"userId":phone_number},{"_id":0})[0]
	except IndexError:  
	    code = self.createPhoneCode()

	    #调用运营商提供的接口向此手机号发送验证码,这里仍然需要修改
	    res = self.send_sms_changzhuo(phone_number,code)
	    print phone_number,code
	    sys.stdout.flush()
	    if res[0]:
	        return {"result":"0000","message":code}
	    elif res[0]:
	        return {"result":"0002","message":code}
	return {"result":"0001","message":None}
    @view_config(request_method = 'POST',renderer = 'json')
    def verify_code(self):
	#code_v正确的验证码，code用户输入的验证码
	code_v = int(self.request.params.get('code_v',None))
	code = int(self.request.params.get('code',None))
	if code_v == code:
	    return {"result":"0000"}
	else:
	    return {"result":"0004"}


    @view_config(request_param = "register=1",request_method = 'POST',renderer = 'json') 
    def sign_up(self): 
	temp = {} 
	userId = self.request.params.get("userId",None) 

	headImage = self.request.params.get("headImage",None)

	password = self.request.params.get("password",None)
	gender = self.request.params.get("gender",None)
	nickname = self.request.params.get("nickname",None) 
	token = None 
	liveStatus = "off"
	isAdmin = 0
	messages = []
	
	temp["userId"]= userId
	temp["password"]= password
	temp["gender"]= gender
	temp["nickname"]= nickname
	temp["isAdmin"]= isAdmin
	temp["headImage"]= headImage
	temp["token"]= token
	temp["messages"] = messages
	temp["liveStatus"]= liveStatus

	
	pyc.setCollection('users')
	try:
	    pyc.update({"userId":userId},temp)
	except:
	    return {"result":"0006"}
	return {"result":"0000"}

#登录和注销功能
@view_defaults(route_name = 'log')
class SignInOut(object):
    def __init__(self,request):
	self.request = request
	self.token = request.params.get('token',None)
	self.login = request.params.get('userId',None)
	self.passwd = request.params.get('password',None)

    def check_user(self,token):
    	try:
	    pyc.setCollection('users')
	    user = pyc.find({"userId":self.login},{"_id":0})[0] 
	except IndexError:
	    return 1,None
	if self.passwd != user["password"]:
	    return 2,None
	token = auth.encode(self.login,
		     time.time()+ int(self.request.params.get('expire_in',None)))
	pyc.update({"userId":self.login},{"token":token})
	return 0,token

    @view_config(request_method = 'POST',renderer = 'json')
    def sign_in(self):
	res = self.check_user(self.token)
	if res[0] == 0:
	    return {"result":"0000","message":res[1]}

	if res[0] == 1:
	    return {"result":"0007","message":None}

	if res[0] == 2:
	    return {"result":"0008","message":None}
	
    @view_config(request_method = 'DELETE')
    def logout(self):
	pass

#消息处理
#接受申请
#拒绝申请

#用户管理
#1.搜索用户
#2.好友搜索
#3.添加好友
#4.删除好友
#5.显示好友列表

#好友搜索策略还未确定
@view_defaults(route_name = "friend")
class FriendManage(object):
    def __init__(self,request):
	self.request = request

    #用户搜索

    @auth_interface
    @view_config(request_method = 'POST',request_param = 'search=1',renderer = 'json')
    def serach(self,**kws):
	object_id = self.request.params.get("userId",None)
	count = 0
	pyc.setCollection('users')
	try:
	    user = pyc.find({"userId":object_id},{"_id":0,"password":0,"isAdmin":0,"messages":0})[0]
	except IndexError:
	    return {"result":"0007","message":None,"flag":None}

	#判断目标用户是否为用户自己,以flag作为识别标示

	if user["userId"]== kws["userid"]:
	    return {"result":"0000","message":user,"flag":"-1"}
	
	#判断目标用户是否为好友
	pyc.setCollection('relationships')
	cur = pyc.find({"userId1":kws["userid"],"userId2":object_id})
	for s in cur:
	    count+= 1
	if count == 1:
	    return {"result":"0000","message":user,"flag":"1"}
	else:
	    cur = pyc.find({"userId1":object_id,"userId2":kws["userid"]})
	    for s in cur:
		count+= 1
	    if count == 1:
	        return {"result":"0000","message":user,"flag":"1"}
	    else:
		return {"result":"0000","message":user,"flag":"0"}

    #添加好友
    @auth_interface
    @view_config(request_method = 'POST',renderer = 'json',request_param='add=1')
    def add_friend(self,**kws):
	object_id = self.request.params.get("userId",None)
	try:
	    pyc.setCollection('relationships')
	    rel = pyc.find({"userId1":kws["userid"],"userId2":object_id})[0]
	except IndexError:
	    pyc.setCollection('users')
	    #好友消息有4种，被申请者0:待接受，1:已接受;   申请者2:等待验证，3:已同意 
	    #被申请人添加好友申请信息
	    mes = pyc.find({"userId":kws["userid"]},
			{"_id":0,"userId":1,"headImage":1,"gender":1,"nickname":1})[0]
	    mes["flag"] = 0
	    pyc.update({"userId":object_id},{"messages":{'$each':[mes]}},1)
	    #申请人添加等待验证信息
	    mes = pyc.find({"userId":object_id},
			{"_id":0,"userId":1,"headImage":1,"gender":1,"nickname":1})[0]
	    mes["flag"]= 2
	    print mes
	    pyc.update({"userId":kws["userid"]},{"messages":{'$each':[mes]}},1)
	    return {"result":"0000","mes":None}
	return {"result":"0010","mes":None}

    #消息处理
    @auth_interface
    @view_config(request_method = 'POST',request_param = 'dealMessage=1',renderer='json')
    def deal_messages(self,**kws):
	behaviour = self.request.params.get("behaviour",None)
	object_id = self.request.params.get("userId",None)
	#如果同意申请，则将被申请方消息状态设置为已接受1,申请方消息状态设置为已同意3,并更新好友关系表
	if behaviour == 'accept':
	    pyc.setCollection("users")
	    pyc.update({"userId":kws["userid"],"messages.userId":object_id},
			{"messages.$.flag":1})
	    pyc.update({"userId":object_id,"messages.userId":kws["userid"]},
			{"messages.$.flag":3})

	    pyc.setCollection("relationships") 
	    pyc.update({"userId1":kws["userid"]},
			{"userId1":kws["userid"],"userId2":object_id})
	    '''
	    pyc.update({"userId1":object_id},
			{"userId1":object_id,"userId2":kws["userid"]})
	    '''
	    return {"result":"0000"}

	#删除申请信息
	if behaviour == 'delete':
	    pyc.setCollection("users")
	    pyc.update({"userId":kws["userid"]},{"messages":{"userId":object_id}},2)
	    return {"result":"0000"}

    #删除好友
    @auth_interface
    @view_config(request_method = 'POST',request_param='delete=1',renderer = 'json')
    def del_friend(self,**kws):
	object_id = self.request.params.get("userId",None)
	pyc.setCollection('relationships')
	count = pyc.remove({"userId1":kws["userid"],"userId2":object_id})
	if count== 0:
	    count = pyc.remove({"userId1":object_id,"userId2":kws["userid"]})
	if count != 0:
	    return json.dumps({"status":"true","mes":"已删除"},
			ensure_ascii= False)
	else:
	    return json.dumps({"status":"false","mes":"不存在"},
			ensure_ascii= False)


@view_defaults(route_name='room')
class room_logic(object):
    def __init__(self,request):
        self.request = request
    
    #创建房间
    @auth_interface
    @view_config(request_method = 'POST',request_param = "live=1",renderer = 'json')
    def create_room(self,**kws):

	title = self.request.params.get('title',None)
        #向七牛直播空间申请推流stream，并将其以json格式返回
	try:
            credentials = Credentials(access_key,secret_key)
            hub = Hub(credentials,hub_name)
            stream = hub.create_stream(title=None , publishKey=None , 
                    publishSecurity="static")
	except:
	    return {"result":"0009","message":None}
        pilipili = {}
        if(stream):
	    pilipili['userId']= kws["userid"]
            pilipili['roomId'] = stream.id
            pilipili['publishUrl'] = stream.rtmp_publish_url()
            pilipili['playUrl'] = stream.rtmp_live_urls()
            pilipili['title'] = title
	    
	    pyc.setCollection('user_room')
            pyc.update({"userId":kws["userid"]},pilipili)

	    pyc.setCollection('users')
	    pyc.update({"userId":kws["userid"]},{"liveStatus":"on"})

        return {"result":"0000","message":json.loads(stream.to_json())}

    #关闭房间
    @auth_interface
    @view_config(request_method = 'POST',renderer = 'string',request_param="leave=1")
    def my_exitroom(self,**kws):
        
        #主播离开房间，删除相对应的stream，更新数据库

	try:
            credentials = Credentials(access_key,secret_key)
            hub = Hub(credentials,hub_name)

	    pyc.setCollection('user_room')
            roomid = pyc.find({"userId":userid},{"_id":0})[0]["roomId"]
            stream = hub.get_stream(stream_id = roomid)
	except:
	    return {"result":"0009"}

        try:
            stream.delete()
        except Exception,e:
            return {"result":"0009"}
	pyc.setCollection('user_room')	
        pyc.update({"userId":kws["userid"]},{"liveStatus":"off"})
	return {"result":"0000"}


@view_defaults(route_name = 'list' , renderer = 'json')
class List(object):
    def __init__(self,request):
        self.request = request

    def my_cmp(x,y):
	if x["liveStatus"]== "on":
	    return -1
	if y["liveStatus"]== "on":
	    return 1
	return 0

    def get_friends(self,userid):
	i = 0
	li = []
	temp = {"count":i,"friends":li}
	pyc.setCollection('relationships')
	users = pyc.find({"$or":[{"userId1":userid},{"userId2":userid}]},{"_id":0})
	for s in users:
	    i+= 1
	    if s["userId1"]== userid:
		id_ = s["userId2"]
	    else:
		id_ = s["userId1"]
	    pyc.setCollection('users')
	    info = pyc.find({"userId":id_},{"_id":0,"userId":1,"headImage":1,"gender":1,"nickname":1,"liveStatus":1})[0]
	    pyc.setCollection('user_room')
	    try:
	        info["playUrl"]= pyc.find({"userId":id_},{"_id":0,"playUrl":1})[0].get("playUrl",None)
	    except IndexError:
		info["playUrl"]= None
	    li.append(info)
	li.sort(self.my_cmp)
	temp["friends"]= li
	print temp
	sys.stdout.flush()
	return temp


    #显示好友列表
    @auth_interface
    @view_config(request_method = 'POST',renderer = 'json',request_param='friendlist=1')
    def show_list_friend(self,**kws):
	temp = self.get_friends(kws["userid"])
	return {"result":"0000","message":temp}

    #显示消息列表
    @auth_interface
    @view_config(request_method = 'POST',renderer = 'json',request_param='messagelist=1')
    def show_list_message(self,**kws):
	count = 0
	pyc.setCollection('users')
	user = pyc.find({"userId":kws["userid"]},{"_id":0})[0]
	messages = user["messages"]
	return {"result":"0000","message":messages}

@view_config(route_name = 'upload',renderer = 'json')
def image_upload(request):
	pic = request.POST['img']
	filename = pic.filename
	file_path = '/'.join(['static','user_imgs',filename]) 
	input_file = pic.file
	try:
	    with open('/env/workspace/PyramidProject/MyProject/myproject/'+file_path,'wb') as output_file: 
	    	shutil.copyfileobj(input_file,output_file) 
	except:
	    return {"result":"0006","message":None}
	return {"result":"0000","message":file_path}	





