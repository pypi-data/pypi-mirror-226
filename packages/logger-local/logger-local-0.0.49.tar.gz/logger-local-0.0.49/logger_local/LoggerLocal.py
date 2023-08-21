import os
from functools import wraps
from logger_local.LoggerService import LoggerService
from logger_local.LoggerComponentEnum import LoggerComponentEnum


loggers={}
@staticmethod
def logger(**kwargs):
    if(os.getenv("ENVIRONMENT_NAME") is None):
        raise Exception("logger-local-python-package LoggerLocal.py please add Environment Variable called ENVIRONMENT_NAME=local or play1 (instead of ENVIRONMENT)")
    if('component_id' not in kwargs['object'] or "component_name" not in kwargs['object'] or "component_category" not in kwargs['object'] or "developer_email" not in kwargs['object']):
        raise Exception("please insert component_id, component_name, component_category and developer_email in your object")
    component_id=kwargs['object']['component_id']
    if component_id in loggers:
        return loggers.get(component_id)
    else:
        logger=LoggerService()
        loggers[component_id]=logger
        logger.init(**kwargs)
        return logger
@staticmethod
def log_function_execution(func):
    @wraps(func)
    def wrapper(component_id:int,*args, **kwargs):
        logger_local=logger(component_id)
        object1 = {
            'args': str(args),
            'kawargs': str(kwargs),
        }
        logger_local.start(object=object1)
        result = func(*args, **kwargs)  # Execute the function
        object2 = {
            'result': result,
        }
        logger_local.end(object=object2)
        return result
    return wrapper