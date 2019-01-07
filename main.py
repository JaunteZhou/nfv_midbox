#!/usr/bin/python
# -*- coding: utf-8 -*-
#main.py

# init log settings
# 初始化log全局设置
import log_init
from midbox.southbound.docker import registry
log_init.log_init()

# just for test
# TODO:只是测试使用，后续删除
# from midbox import _test_log
# _test_log.test_log()

# run main flask app
# 运行主程序flask的app
from midbox import plat
registry.registry_start()
plat.app.run()