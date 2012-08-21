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

import re
import sys

import urlfetch

URL_INDEX = 'http://www.cnepub.com/discuz/'
URL_LOGIN = 'http://www.cnepub.com/discuz/logging.php?action=login'
URL_LOGIN_POST = 'http://www.cnepub.com/discuz/logging.php?action=login' \
    '&loginsubmit=yes&floatlogin=yes'
URL_TASKS_APPLY = 'http://www.cnepub.com/discuz/task.php?action=apply&id=%d'
URL_TASKS_DRAW = 'http://www.cnepub.com/discuz/task.php?action=draw&id=%d'
URL_TASKS_IDS = [34, 42, ]

FORMHASH_PATTERN = \
    re.compile(r'<input type="hidden" name="formhash" value="(\w+)" />')

def main():
    """Main Process"""
    session = urlfetch.Session()

    # login
    response = session.get(URL_LOGIN)
    result = FORMHASH_PATTERN.search(response.body)
    formhash = result.group(1)
    data = {
        'formhash': formhash,
        'referer': URL_INDEX,
        'username': sys.argv[1],
        'password': sys.argv[2],
    }
    response = session.post(URL_LOGIN_POST, data=data)
    body = session.get(URL_INDEX).body

    # tasks
    for task_id in URL_TASKS_IDS:
        url = URL_TASKS_APPLY % task_id
        response = session.post(url)
        url = URL_TASKS_DRAW % task_id
        response = session.post(url)

if __name__ == '__main__':
    main()
