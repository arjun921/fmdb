
import logging
import functools
import datetime
from utils.helpers import log_line

def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        docstring = func.__doc__
        function_parent = docstring.split()[-1]
        logger = logging.getLogger(function_parent+'.'+func.__name__)
        log_line(logger,level='info',extras={'status':'started'})
        start = datetime.datetime.now()
        original_result = func(*args, **kwargs)
        end = datetime.datetime.now()
        log_line(logger,level='info',extras={'status':'ended'})
        log_line(logger,level='info', extras={'exec_time':str(end-start)})
        return original_result
    return wrapper