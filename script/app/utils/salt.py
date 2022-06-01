import json
import copy
import requests
# from crypt import crypt
from requests.adapters import HTTPAdapter

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class SaltApi(object):

    def __init__(self, url=None, username=None, password=None, eauth=None):
        self.__url = url
        self.__user = username
        self.__password = password
        self.__eauth = eauth
        self.__headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
        self.__data = {'client': 'local', 'tgt': None, 'fun': None, 'arg': None}
        self.__token = None
        self.get_token()
    def get_token(self):
        """
        用户登陆和获取token
        :return:
        """
        params = {'eauth': self.__eauth, 'username': self.__user, 'password': self.__password}
        content = self.postRequest(params, self.__headers, prefix='login')
        try:
            self.__token = content['return'][0]['token']
            self.__headers['X-Auth-Token'] = self.__token
        except Exception as e:
            print(e)
            return content

    def get_grains(self, target=None):
        """
        获取系统基础信息
        :return:
        """
        data = copy.deepcopy(self.__data)
        if target:
            data['tgt'] = target
        else:
            data['tgt'] = '*'
        data['fun'] = 'grains.items'
        content = self.postRequest(data, self.__headers)
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
        data = copy.deepcopy(self.__data)
        data['client'] = 'wheel'
        data['fun'] = 'key.list_all'
        content = self.postRequest(data, self.__headers)
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
        data = copy.deepcopy(self.__data)
        data['client'] = 'runner'
        data['fun'] = 'manage.status'
        data.pop('tgt')
        data.pop('arg')
        content = self.postRequest(data, self.__headers)
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

        data = copy.deepcopy(self.__data)
        data['client'] = 'wheel'
        data['fun'] = 'key.delete'
        data['match'] = minion
        content = self.postRequest(data, self.__headers)

        try:
            return {'success': content['return'][0]['data']['success']}
        except Exception as e:
            print(e)
            return content

    def minion_alive(self, minion=None):
        '''
        Minion主机存活检测
        '''
        data = copy.deepcopy(self.__data)
        if minion:
            data['tgt'] = minion
        else:
            data['tgt'] = '*'
        data['fun'] = 'test.ping'
        data.pop('arg')
        content = self.postRequest(data, self.__headers)
        try:
            if content['return'][0]:
                return content['return'][0]
            else:
                return {minion: False}
        except Exception as e:
            print(e)
            return content

    # def passwd(self, target=None, user=None, password=None):
    #     """
    #     修改密码
    #     :param target: 目标客户端
    #     :param user: 目标客户端的系统用户名
    #     :param password: 新的密码,必须大于等于12位
    #     :return:
    #     """
    #     if not target: return {'success': False, 'msg': 'target is none.'}
    #     if not user: return {'success': False, 'msg': 'user is none.'}
    #     if not password: return {'success': False, 'msg': 'password is none.'}
    #     if len(password) < 12: return {'success': False, 'msg': 'password must be greater than or equal to 12 bits.'}
    #     if password.isalpha() or password.isdigit() or password.islower() or password.isupper(): return {
    #         'success': False, 'msg': 'password must be have lowercase, uppercase and digit.'}
    #     password = crypt(password, 'cmdb')
    #     content = self.cmd(target=target, arg='usermod -p "{}" {}'.format(password, user))

    #     return {'success': True,
    #             'msg': 'Changing password for user {}.'
    #                    'all authentication tokens updated successfully.'.format(user)
    #             }

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
        :param target: 目标客户端, 为空return False
        :param fun: 模块
        :param arg: 参数，可为空
        :param async: 异步执行，默认非异步
        :return:
        """
        data = copy.deepcopy(self.__data)
        if not target: return {'success': False, 'msg': 'target is none'}
        if not arg: data.pop('arg')
        if isasync: data['client'] = 'local_async'
        data['tgt'] = target
        data['fun'] = fun
        data['arg'] = arg
        content = self.postRequest(data, self.__headers)
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
        content = self.postRequest(data, self.__headers)
        try:
            return content['return'][0]
        except Exception as e:
            print(e)
            return content

    def postRequest(self, data, headers, prefix=None):
        if prefix:
            url = '{}/{}'.format(self.__url, prefix)
        else:
            url = self.__url
        try:
            s = requests.Session()
            s.mount('https://', HTTPAdapter(max_retries=10))
            ret = s.post(url, data=json.dumps(data), headers=headers, verify=False, timeout=(30, 60))
            # print(ret.request.url)
            # print(ret.request.body)
            # print(ret.request.headers)
            if ret.status_code == 401:
                print('401 Unauthorized')
                return {'return': [{'success': False, 'msg': '401 Unauthorized'}]}
            elif ret.status_code == 200:
                return ret.json()
        except Exception as e:
            print(e)
            return {'return': [{'success': False, 'msg': e}]}