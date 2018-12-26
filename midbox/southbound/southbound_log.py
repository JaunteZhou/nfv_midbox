import logging
import logging.handlers
# my_logger = logging.getLogger('nfv_midbox.northbound')
my_logger = logging.getLogger('nfv_midbox.'+__name__)
# my_logger.setLevel(logging.INFO)
# f_handler = logging.FileHandler('log/error.log')
# # my_logger.setLevel('INFO')
# def _set_logger_level(str_level):
#     my_logger.setLevel(str_level)

# def logger_add_handler(handler_list):
#     for handler in handler_list:
#         my_logger.addHandler(handler)

def test_log():
    my_logger.debug("This is a debug log.")
    my_logger.info("This is a info log.")
    my_logger.warning("This is a warning log.")
    my_logger.error("This is a error log.")
    my_logger.critical("This is a critical log.")

    # print(__name__)