# coding: utf-8

# 時間を測るデコレータ
def measure_time(func):
    import time
    import datetime
    import functools
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logfile = open('process.log', 'a')
        start = time.time()
        result = func(*args, **kwargs) # 関数の実行
        end = time.time()
        Date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        Name = func.__name__
        Time = end - start
        print "%s %s %f sec\n" % (Date, Name, Time)
        logfile.write("%s %s %f sec\n" % (Date, Name, Time))
        logfile.close()
        return result
    return wrapper


@measure_time
def test():
    for i in xrange(100000):
        print i


if __name__ == "__main__":
    test()


