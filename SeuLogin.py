# coding: utf-8
__author__ = 'lavenderArc'
__date__ = '2018/10/25 11:00'

import requests
import json
import base64
import sys


def decode_utf8(s):
    """encode utf8 to unicode"""
    return s.encode('utf-8').decode('unicode-escape')


class SeuLogin:
    """Seu login with usr pw"""
    def __init__(self):
        self.url_seu = 'https://w.seu.edu.cn/index.php/index'
        self.url_methods = {
            'enter': 'init?_=1540818027180',
            'login': 'login',
            'logout': 'logout'
        }
        self.config_format = {
            'username': '',
            'password': '',
            'enablemacauth': 0
        }
        self.session = requests.Session()
        self.config_fp = 'config.json'
        self.response = requests.Response()
        self.result = {}

        while True:
            if self.__read_config():
                break
            else:
                self.input_up()
        self.do()

    def __read_config(self):
        self.config_info = json.load(open(self.config_fp))
        for key, val in self.config_info.items():
            if key not in self.config_format.keys() or val == '':
                return False
        return True

    def do(self, method='enter'):
        if method in self.url_methods.keys():
            url = self.url_seu + '/' + self.url_methods[method]
            if method == 'login':
                data = self.config_info
                data['password'] = base64.b64encode(data['password'].encode('utf-8'))  # base64 encrypt pw
                self.response = self.session.post(url, data)
            else:
                self.response = self.session.get(url)
            self.result = eval(decode_utf8(self.response.text.replace('null', 'None')))
        else:
            raise Exception('seu method is wrong, check it.\nSupported method: ' + self.url_methods.keys().__str__())

    def status_ex(self):
        return self.result

    def status(self):
        res = self.result['info']
        if 'logout_username' in self.result.keys():
            res += ' [' + self.result['logout_username'] + ']'
        return res

    def input_up(self):
        raw = input('input username and password.\n')
        if raw.__contains__(' '):
            self.save_up(raw.split(' ')[0], raw.split(' ')[1])
        else:
            print('invalid, try again.[username password]\n')
            self.input_up()

    def save_up(self, usr, pw):
        self.config_info['username'] = usr
        self.config_info['password'] = pw
        json.dump(self.config_info, open(self.config_fp, 'w'), indent=4)


if __name__ == '__main__':
    args = sys.argv
    sl = SeuLogin()
    if args.__len__() == 2:
        sl.do(args[1])
    elif args.__len__() == 4:
        sl.save_up(args[2], args[3])
        sl.do(args[1])
    print(sl.status() + '\n')
