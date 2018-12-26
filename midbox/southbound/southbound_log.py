import logging

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
    local_logger.debug("This is a debug log.")
    local_logger.info("This is a info log.")
    local_logger.warning("This is a warning log.")
    local_logger.error("This is a error log.")
    local_logger.critical("This is a critical log.")

    # print(__name__)