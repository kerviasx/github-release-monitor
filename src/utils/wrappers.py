# 定义装饰器time
import functools,time
from inspect import signature

def MyTimeWrapper(func):
    """
        函数执行前后打印时间
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('-'*40)
        time_local = time.localtime()
        dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        print('[时间]: '+dt)
        ret = func(*args, **kwargs)
        time_local = time.localtime()
        dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        print('[时间]: '+dt)
        print('-'*40+"\n")
        return ret
    return wrapper




def TypeAssert(*type_args, **type_kwargs):
    """
    函数参数类型检查
    """
    def decorate(func):
        sig = signature(func)
        bound_types = sig.bind_partial(*type_args, **type_kwargs).arguments

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError('Argument {} must be {}'.format(name, bound_types[name]))
            return func(*args, **kwargs)
        return wrapper
    return decorate


@MyTimeWrapper
def test():
    pass





if __name__ == '__main__':
    test()

