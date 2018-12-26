#!/usr/bin/python
# -*- coding: utf-8 -*-
#main.py

from log import log_init
log_init.log_init()

# just for test
# 只是测试使用，后续删除
from midbox import _test_log
_test_log.test_log()

# run main flask app
# 运行主程序flask的app
# from midbox import plat
# plat.app.run()