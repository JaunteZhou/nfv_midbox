#!/usr/bin/python
# -*- coding: utf-8 -*-
#main.py

from log import log_init
from midbox import plat

from midbox.southbound import southbound_log
southbound_log.test_log()

plat.app.run()