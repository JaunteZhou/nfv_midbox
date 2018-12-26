#!/usr/bin/python
# -*- coding: utf-8 -*-
#log_init.py

import logging
import logging.handlers
import datetime

from log.log_config import debug_rotating_log_dir, error_log_dir

logger = logging.getLogger('midbox')
logger.setLevel(logging.DEBUG)

# set handler to file for all(debug) logs, and rotated at midnight
# 设置针对所有(DEBUG级)日志信息的写入日志文件的handler，并且在每天午夜进行分割
drf_handler = logging.handlers.TimedRotatingFileHandler(debug_rotating_log_dir, when='midnight', interval=1, backupCount=7) #, atTime=datetime.time(0, 0, 0, 0))
drf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - [%(name)s] - %(message)s"))

# set handler to file for error logs
# 设置针对ERROR级别及以上的日志信息的写入日志文件的handler
ef_handler = logging.FileHandler(error_log_dir)
ef_handler.setLevel(logging.ERROR)
ef_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - [%(name)s:%(lineno)d] - %(message)s"))

# add handlers to logger
logger.addHandler(drf_handler)
logger.addHandler(ef_handler)

# write init logs
logger.debug('debug init')
logger.info('info init')
logger.warning('warning init')
logger.error('error init')
logger.critical('critical init')