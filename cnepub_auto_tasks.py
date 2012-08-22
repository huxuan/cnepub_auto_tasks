#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: cnepub_auto_tasks.py
Author: huxuan
E-mail: i(at)huxuan.org
Created: 2012-08-21
Last modified: 2012-08-21
Description:
    Auto Tasks in cnepub or 掌中书苑 in Chinese

Copyrgiht (c) 2012 by huxuan. All rights reserved.
License GPLv3
"""

import os
import re
import sys
import datetime

import urlfetch

URL_INDEX = 'http://www.cnepub.com/discuz/'
URL_LOGIN = 'http://www.cnepub.com/discuz/logging.php?action=login'
URL_LOGIN_POST = 'http://www.cnepub.com/discuz/logging.php?action=login' \
    '&loginsubmit=yes&floatlogin=yes'
URL_TASKS_APPLY = 'http://www.cnepub.com/discuz/task.php?action=apply&id=%d'
URL_TASKS_DRAW = 'http://www.cnepub.com/discuz/task.php?action=draw&id=%d'

ERR_USERNAME_PASSWORD = '[Error] Please input username & password!'

MSG_ALREADY = u'本期您已经申请过此任务，请下期再来申请吧！'
MSG_CANNOT = u'您所在的用户组不允许申请此任务！'
MSG_SUCCESS = u'恭喜您，任务已成功完成，您将收到奖励通知短消息，请注意查收！'

LOG_ALREADY = '[Already] Task %d for %s!'
LOG_CANNOT = '[Cannot] Task %d for %s!'
LOG_SUCCESS = '[Success] Task %d  for %s!'
LOG_FAIL = '[Fail] Task %d for %s!'

FORMHASH_PATTERN = \
    re.compile(r'<input type="hidden" name="formhash" value="(\w+)" />')

TASKS_IDS = [34, 42, ]

def main():
    """Main Process"""
    # init log
    LOG_DIR = os.path.join(os.path.expanduser("~"), '.log')
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    LOG_PATH = os.path.join(LOG_DIR, 'cnepub_auto_tasks.log')
    f = LOG_FILE = file(LOG_PATH, 'a')
    print >>f # add an empty line to seperate log

    # username and password
    if len(sys.argv) != 3:
        print ERR_USERNAME_PASSWORD
        return
    username = sys.argv[1]
    password = sys.argv[2]

    # login
    session = urlfetch.Session()
    response = session.get(URL_LOGIN)
    result = FORMHASH_PATTERN.search(response.body)
    formhash = result.group(1)
    data = {
        'formhash': formhash,
        'username': username,
        'password': password,
    }
    response = session.post(URL_LOGIN_POST, data=data)
    body = session.get(URL_INDEX).body

    # tasks
    for task_id in TASKS_IDS:
        # apply tasks
        url = URL_TASKS_APPLY % task_id
        response = session.post(url)
        if MSG_ALREADY in response.body.decode('gbk'):
            print >>f, LOG_ALREADY % (task_id, username)
        elif MSG_CANNOT in response.body.decode('gbk'):
            print >>f, LOG_CANNOT % (task_id, username)
        else:
            # draw tasks
            url = URL_TASKS_DRAW % task_id
            response = session.post(url)
            if MSG_SUCCESS in response.body.decode('gbk'):
                print >>f, LOG_SUCCESS % (task_id, username)
            else:
                print >>f, LOG_FAIL % (task_id, username)
        print >>f, datetime.datetime.now()

if __name__ == '__main__':
    main()
