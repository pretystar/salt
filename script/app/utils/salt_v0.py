#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# __author__: 'junxing'


import requests
import json
# import app
# try:
#     import cookielib
# except:
#     import http.cookiejar as cookielib

import ssl
import copy
# from crypt import crypt
from requests.adapters import HTTPAdapter
context = ssl._create_unverified_context()

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# salt_api = "https://salt-master:8080/"


class SaltApi:
    """
    """
    def __init__(self, url, username, password):
        self.url = url
        self.username = username #"diana"
        self.password = password #"secret"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Content-type": "application/json"
            # "Content-type": "application/x-yaml"
        }
        self.get_token()
        # self.params = {'client': 'local', 'fun': '', 'tgt': ''}
        self.params = {'client': 'local', 'fun': '', 'tgt': '', 'arg': ''}
        # self.login_url = self.url + "login"
        # self.login_params = {'username': self.username, 'password': self.password, 'eauth': 'mysql'}
        # self.token = self.get_data(self.login_url, self.login_params)['token']
        # print("====token: ", self.token)
        # self.headers['X-Auth-Token'] = self.token
    def get_token(self):
        """
        用户登陆和获取token
        :return:
        """
        params = {'eauth': 'mysql', 'username': self.username, 'password': self.password}
        content = self.get_data(params, prefix='login')
        try:
            self.token = content['return'][0]['token']
            self.headers['X-Auth-Token'] = self.__token
        except Exception as e:
            print(e)
            return content

    def get_data(self,  params, prefix=None):
        if prefix:
            url = '{}/{}'.format(self.url, prefix)
        else:
            url = self.url
        send_data = json.dumps(params)
        request = requests.post(url, data=send_data, headers=self.headers, verify=False)
        # response = request.text
        # response = eval(response)     
        # print(response)
        print("=====header: ", self.headers)
        print(request.status_code)
        # print type(request)
        response = request.json()
        result = dict(response)
        # print result
        return result['return'][0]

    def salt_command(self, tgt, method, arg=None):
        """salt 'client1' cmd.run 'free -m'"""
        if arg:
            params = {'client': 'local', 'fun': method, 'tgt': tgt, 'arg': arg}
        else:
            params = {'client': 'local', 'fun': method, 'tgt': tgt}
        print('parameter: ', params)
        result = self.get_data(params)
        return result
    def salt_async_command(self, tgt, method, arg=None):  
        """"""
        if arg:
            params = {'client': 'local_async', 'fun': method, 'tgt': tgt, 'arg': arg}
        else:
            params = {'client': 'local_async', 'fun': method, 'tgt': tgt}
        jid = self.get_data(params)['jid']
        return jid

    def look_jid(self, jid):  
        params = {'client': 'runner', 'fun': 'jobs.lookup_jid', 'jid': jid}
        print(params)
        result = self.get_data(params)
        return result
############################
    def get_grains(self, target=None):
        """
        获取系统基础信息
        :return:
        """
        data = copy.deepcopy(self.params)
        if target:
            data['tgt'] = target
        else:
            data['tgt'] = '*'
        data['fun'] = 'grains.items'
        content = self.get_data(data)
        try:
            return content['return'][0]
        except Exception as e:
            print(e)
            return content
 
    def get_auth_keys(self):
        """
        获取所有已认证的主机
        :return:
        """
        data = copy.deepcopy(self.params)
        data['client'] = 'wheel'
        data['fun'] = 'key.list_all'
        content = self.get_data(data)
        try:
            return content['return'][0]['data']['return']['minions']
        except Exception as e:
            print(e)
            return content
 
    def get_minion_status(self):
        """
        获取所有主机的连接状态
        :return:
        """
        data = copy.deepcopy(self.params)
        data['client'] = 'runner'
        data['fun'] = 'manage.status'
        data.pop('tgt')
        data.pop('arg')
        content = self.get_data(data)
        try:
            return content['return'][0]
        except Exception as e:
            print(e)
            return content
 
    def delete_key(self, minion=None):
        '''
        删除指定主机的认证信息
        '''
        if not minion:
            return {'success': False, 'msg': 'minion-id is none'}
 
        data = copy.deepcopy(self.params)
        data['client'] = 'wheel'
        data['fun'] = 'key.delete'
        data['match'] = minion
        content = self.get_data(data)
 
        try:
            return {'success': content['return'][0]['data']['success']}
        except Exception as e:
            print(e)
            return content
 
    def minion_alive(self, minion=None):
        '''
        Minion主机存活检测
        '''
        data = copy.deepcopy(self.params)
        if minion:
            data['tgt'] = minion
        else:
            data['tgt'] = '*'
        data['fun'] = 'test.ping'
        data.pop('arg')
        content = self.get_data(data)
        try:
            if content['return'][0]:
                return content['return'][0]
            else:
                return {minion: False}
        except Exception as e:
            print(e)
            return content
 
    def passwd(self, target=None, user=None, password=None):
        """
        修改密码
        :param target: 目标客户端
        :param user: 目标客户端的系统用户名
        :param password: 新的密码,必须大于等于12位
        :return:
        """
        if not target: return {'success': False, 'msg': 'target is none.'}
        if not user: return {'success': False, 'msg': 'user is none.'}
        if not password: return {'success': False, 'msg': 'password is none.'}
        if len(password) < 12: return {'success': False, 'msg': 'password must be greater than or equal to 12 bits.'}
        if password.isalpha() or password.isdigit() or password.islower() or password.isupper(): return {
            'success': False, 'msg': 'password must be have lowercase, uppercase and digit.'}
        password = crypt(password, 'cmdb')
        content = self.cmd(target=target, arg='usermod -p "{}" {}'.format(password, user))
 
        return {'success': True,
                'msg': 'Changing password for user {}.'
                       'all authentication tokens updated successfully.'.format(user)
                }
 
    def get_users(self, target=None):
        """
        获取系统用户
        :param target: 目标客户端
        :return:
        """
        if not target: return {'success': False, 'msg': 'target is none.'}
        content = self.cmd(target=target, arg="grep /bin/bash /etc/passwd|awk -F ':' '{print $1}'")
        return content
 
    def cmd(self, target=None, fun='cmd.run', arg=None, isasync=False):
        """
        远程执行任务
        :param target: 目标客户端，为空return False
        :param fun: 模块
        :param arg: 参数，可为空
        :param async: 异步执行，默认非异步
        :return:
        """
        data = copy.deepcopy(self.params)
        if not target: return {'success': False, 'msg': 'target is none'}
        if not arg: data.pop('arg')
        if isasync: data['client'] = 'local_async'
        data['tgt'] = target
        data['fun'] = fun
        data['arg'] = arg
        content = self.get_data(data)
        try:
            return content['return'][0]
        except Exception as e:
            print(e)
            return content
 
    def jobs(self, fun=None, jid=None):
        """
        任务
        :param fun: active,detail
        :param jid: Job ID
        :return:
        """
        data = {'client': 'runner'}
        if fun == 'active':
            data['fun'] = 'jobs.active'
        elif fun == 'detail':
            if not jid: return {'success': False, 'msg': 'job id is none'}
            data['fun'] = 'jobs.lookup_jid'
            data['jid'] = jid
        else:
            return {'success': False, 'msg': 'fun is active or detail'}
        content = self.get_data(data)
        try:
            return content['return'][0]
        except Exception as e:
            print(e)
            return content
 
    # def postRequest(self, data, headers, prefix=None):
    #     if prefix:
    #         url = '{}/{}'.format(self.__url, prefix)
    #     else:
    #         url = self.__url
    #     try:
    #         s = requests.Session()
    #         s.mount('https://', HTTPAdapter(max_retries=10))
    #         ret = s.post(url, data=json.dumps(data), headers=headers, verify=False, timeout=(30, 60))
    #         if ret.status_code == 401:
    #             print('401 Unauthorized')
    #             return {'return': [{'success': False, 'msg': '401 Unauthorized'}]}
    #         elif ret.status_code == 200:
    #             return ret.json()
    #     except Exception as e:
    #         print(e)
    #         return {'return': [{'success': False, 'msg': e}]}

def main():
    print
    print('==================')
    print('')
    url="https://localhost:8080"
    username="diana"
    password="secret"
    salt1 = SaltApi(url, username, password)
    salt_client = '*'
    salt_method = 'cmd.run'
    salt_params = 'df -hT'
    jid1 = salt1.salt_async_command(salt_client, salt_method, salt_params)
    result1 = salt1.look_jid(jid1)
    print("Result: ")
    for i in result1.keys():
        print(i, ': ', result1[i])

    # jid2 = salt1.salt_async_command(salt_client, salt_method, salt_params)
    # result2 = salt1.look_jid(jid2)
    # for i in result2.keys():
    #     print(i)
    #     print(result2[i])
    #     print()


if __name__ == '__main__':
    main()