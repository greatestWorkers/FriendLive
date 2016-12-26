import hashlib
import time
from pyramid.response import Response

class authentication(object):
    def decode(self,token):
        params = str(token).split('.')
        userid = params[0]
        expire_in = int(params[1])
        sign = params[2]
        if expire_in>time.time():
            if sign == self._to_sign(userid,expire_in):
                return dict(userid=userid,expire_in=expire_in)
        return None
    def encode(self,userid,expire_in):
        userid = str(userid)
        return "%s.%d.%s" % (userid,expire_in,
                    self._to_sign(userid,expire_in))
    def _to_sign(self,userid,expire_in):
        unsigned_data = 'userid=%s&expire_in=%d&secret=%s'%(userid,
                expire_in,'sha512')
        m = hashlib.md5()
        m.update(unsigned_data)
        return m.hexdigest()

auth = authentication()

def auth_interface(method):
    def authed(self):
	token = self.request.params["token"]
	struct = auth.decode(token)
        if struct is None:
            return Response({"status":"failed","message":"please signup"})
	return method(self,**struct)
    return authed
