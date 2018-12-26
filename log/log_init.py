#!/usr/bin/python3
# -*- coding: utf-8 -*-
#log.py

import logging
import logging.handlers
import datetime
# from southbound import southbound_log

# LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
# logging.basicConfig(filename='log/nfv_midbox.log', level=logging.ERROR, format=LOG_FORMAT)
# # logger = logging.getLogger('nfv_midbox')

logger = logging.getLogger('nfv_midbox')
logger.setLevel(logging.DEBUG)

rf_handler = logging.handlers.TimedRotatingFileHandler('log/all.log', when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s"))

f_handler = logging.FileHandler('log/error.log')
f_handler.setLevel(logging.ERROR)
f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

logger.addHandler(rf_handler)
logger.addHandler(f_handler)

logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('error message')
logger.critical('critical message')

# southbound_log.logger_add_handler([f_handler, rf_handler])
# southbound_log.test_log()