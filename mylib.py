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
        FileName = __file__
        FuncName = func.__name__
        Time = end - start
        print "%s %s:%s() %f sec\n" % (Date, FileName, FuncName, Time)
        logfile.write("%s %s:%s() %f sec\n" % (Date, FileName, FuncName, Time))
        logfile.close()
        return result
    return wrapper


# ディレクトリ配下の全ファイルへの絶対パスを,リスト形式で取得
def getFileList(dir_path):
    import os
    fileList = []
    for root, dirs, fnames in os.walk(dir_path):
        for fname in fnames:
            fileList.append( os.path.join(root, fname) )

    return fileList


# 3次元プロット
def plot3d(xs, ys, zs, c="b"):
    import matplotlib.pyplot as plt
    from mpl_toolkits import axes3d
    fig = plt.figure()
    ax = axes3d
    ax.scatter3D(xs, ys, zs, color=c)
    plt.show()


# 2次元プロット
def plot2d(xs, ys, c=u'b', m=u'o'):
    import matplotlib.pyplot as plt
    plt.scatter(xs, ys, c=c, marker=m)
    plt.show()


@measure_time
def test():
    for i in xrange(100000):
        print i


if __name__ == "__main__":
    test()


