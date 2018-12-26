#!/usr/bin/python
# -*- coding: utf-8 -*-  
#_test_log.py
import logging

# TODO: 测试使用，后续删除

local_logger = logging.getLogger(__name__)

def test_log():
    res = {"haha":1, "hoho":2, "hehe":3}
    local_logger.debug(("test xiao: ", res))
    local_logger.info("This is a info log.")
    local_logger.warning("This is a warning log.")
    local_logger.error("This is a error log.")
    local_logger.critical("This is a critical log.")
