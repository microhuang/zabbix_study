#!/usr/bin/env python
#-*- coding: utf-8 -*-

#author: huang
#date: 2018-04-20
#comment: zabbix接入微信报警脚本
#python huang 服务故障 无法连接服务器

import requests
import sys
import os
import json
import logging

#===============config==============

import edata

corpid=edata.corpid#微信企业ID
appsecret=edata.appsecret#微信应用KEY
agentid=edata.agentid#微信应用ID

log_path='/tmp/'
#===================================

logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s, %(filename)s, %(levelname)s, %(message)s',
                datefmt = '%a, %d %b %Y %H:%M:%S',
                filename = os.path.join(log_path,'weixin.log'),
                filemode = 'a')

#获取accesstoken
token_url='https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + appsecret
req=requests.get(token_url)
accesstoken=req.json()['access_token']

#发送消息
msgsend_url='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + accesstoken

touser=sys.argv[1]
#toparty='3|4|5|6'
toparty=sys.argv[2]
subject=sys.argv[3]
message=sys.argv[4]

params={
        "touser": touser,#企业微信号
        "toparty": toparty,#企业微信部门
        "msgtype": "markdown",
        "agentid": agentid,
        "markdown": {
                "content": message
        },
        "safe":0
}

if not touser and not toparty:
  raise Exception('缺少参数！')
if not touser:
  del(params['touser'])
if not toparty:
  del(params['toparty'])

req=requests.post(msgsend_url, data=json.dumps(params, ensure_ascii=False))

logging.info('sendto:' + touser + ';;subject:' + subject + ';;message:' + message)
