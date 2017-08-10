#!/usr/bin/env python
# coding: utf-8

from db import Storage
import sys
import json

# {
#   "MsgId": "", // 无用
#   "FromUserName": "", // 发消息的人, 可以用于回复消息
#   "ToUserName": "", // 接收消息的人, 就是自己, 无用
#   "MsgType": 1, // 无用
#   "Content": "hhh", // 原始消息内容 (可能包含@)
#   "AtMe": false, // 是否@我, 在 FromGroup 为 true 时有效
#   "FromGroup": true, // 是否组消息
#   "FromGroupMember": {    // 组消息的实际发消息的人
#     "UserName": "", // 用户id, 和 FromUserName 格式一样
#     "NickName": "", // 用户昵称
#     "RemarkName": "", // 备注名称
#     "Type": 0
#   },
#   "MsgBodyWitoutAt": "" // Content 删掉@信息之后的内容
# }

def main():
    if len(sys.argv) != 2:
        return
    try:
        msg = json.loads(sys.argv[1])
        user = msg['FromUserName']
        cmd = msg['Content']

        if not cmd in ['smzdm/start', 'smzdm/stop']:
            print json.dumps({'to': msg['FromUserName'], 'content': '不支持此命令, 只支持 smzdm/start, smzdm/stop'})
            return

        s = Storage()
        s.set_user(user, {'state':cmd})
        print json.dumps({'to': msg['FromUserName'], 'content': 'ok %s' % cmd})

    except Exception as e:
        print e
        pass


if __name__ == '__main__':
    main()