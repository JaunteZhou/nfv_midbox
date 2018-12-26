#!/usr/bin/python
# -*- coding: utf-8 -*-
#central_unit.py
import logging
logger = logging.getLogger(__name__)

from midbox import chain, function, status

F_MAP = {
    "STATUS":{
        "GET":status.showAllStatus
    },
    "FUNCTION": {
        "GET":{},
        "POST":function.setFunction,
        "DELETE":function.delFunction
    },
    "CHAIN": {
        "GET":{},
        "POST":chain.setChain,
        "DELETE":chain.delChain
    }
}

def proc(para):
    """
    功能：核心处理函数，完成函数之间的映射
    参数：
        method：字符串，请求处理的方式，有SHOW，ADD，DELETE，可添加UPDATE
        south_agent：字符串，南向服务代理
        item：字符串，请求处理的元素，镜像、容器、虚拟机等等
        para：字典类型，输入参数
    """
    logger.debug('Start.')

    method = para['method']
    item = para['item']
    json_para = para['json']

    logger.debug((item, method, json_para))
    
    return F_MAP[item][method](json_para)
