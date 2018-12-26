import logging

# 测试使用，后续删除

local_logger = logging.getLogger(__name__)
# local_logger.setLevel(logging.INFO)
# f_handler = logging.FileHandler('log/error.log')
# # local_logger.setLevel('INFO')
# def _set_logger_level(str_level):
#     local_logger.setLevel(str_level)

# def logger_add_handler(handler_list):
#     for handler in handler_list:
#         local_logger.addHandler(handler)

def test_log():
    res = {"haha":1, "hoho":2, "hehe":3}
    local_logger.debug(("test xiao: ", res))
    local_logger.info("This is a info log.")
    local_logger.warning("This is a warning log.")
    local_logger.error("This is a error log.")
    local_logger.critical("This is a critical log.")

    # print(__name__)

from midbox import _config_test
print(_config_test.config1)
print(_config_test.config2)
print(_config_test.config3)