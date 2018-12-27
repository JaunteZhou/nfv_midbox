#!/usr/bin/python
# -*- coding: utf-8 -*-
#main.py

# init log settings
# 初始化log全局设置
import log_init
log_init.log_init()

# run main flask app
# 运行主程序flask的app
from midbox import plat
plat.app.run()