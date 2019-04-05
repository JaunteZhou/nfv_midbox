#!/usr/bin/python
# -*- coding: utf-8 -*-
# central_unit.py

import logging
logger = logging.getLogger(__name__)

from midbox import chain, function, status

F_MAP = {
    "STATUS": {
        "GET": status.showAllStatus
    },
    "FUNCTION": {
        "POST": function.setFunction,
        "DELETE": function.delFunction,
        "MOVE": function.moveFunction
    },
    "CHAIN": {
        "POST": chain.setChain,
        "DELETE": chain.delChain
    }
}


def proc(para):
    """
    核心处理函数，完成函数之间的映射
    :param para: 字典类型，包含以下内容
            {
                'item'：字符串，请求处理的元素，有资源状态、功能、链等等
                'method'：字符串，请求处理的方式，有GET,POST,DELETE，可添加UPDATE
                'json'：字典类型，具体服务输入参数
            }
    :return:
    """
    logger.debug('Start.')

    item = para['item']
    method = para['method']
    json_para = para['json']

    logger.debug((item, method, json_para))
    
    return F_MAP[item][method](json_para)
