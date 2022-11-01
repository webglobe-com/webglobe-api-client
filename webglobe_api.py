import urllib,requests,json
import sys, re, signal, os
import logging

class WebglobeAPI(object):
    def __init__(self, url, token = None,fn = None):
        self.token = token
        self.fn = fn
        self.url = url
    
    def __getattr__(self, name):
        return self.endpoint(name)
    
    def endpoint(self, name):
        if name == 'auth/login':
            return self.login
        elif name == 'auth/logout':
            return self.logout
        
        attr = type(self)(self.url,self.token, name)
        
        return attr
    
    def get(self, name):
        return self.endpoint(name)()
    
    def post(self, name, **kwargs):
        return self.endpoint(name)(**kwargs)
    
    def __call__(self,**kwargs):
        """docstring for __call"""
        if self.fn == None:
            return None
        headers = {
            'Content-Type': 'application/json',
        }
        if self.token != None:
            headers['Authorization'] = f'Bearer {self.token}'
        myurl = self.url+'/'+self.fn
        if kwargs == {}:
            u = requests.get(myurl, headers=headers)
            text = u.content
        else:
            u = requests.post(myurl, headers=headers, json=kwargs)
            text = u.content
        
        ret = json.loads(text)
        
        if ret['success']:
            return ret['data']
        else:
            # TODO
            raise Exception((ret['error']['code'], ret['error']['message']))
    
    def logout(self):
        self.fn = 'auth/logout'
        ret = self.__call__(sid=self.sid)
        self.sid = None
        return ret
    
    def login(self,login,password, otp=None, sms = None):
        self.fn = 'auth/login'
        self.token = None
        ret = self.__call__(login=login,password=password, otp = otp, sms = sms)
        
        self.token = ret['token']
        return self
