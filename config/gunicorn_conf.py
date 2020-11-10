import os

currentRootPath = os.getcwd()
workers = 5  # 可以理解为进程数，会自动分配到你机器上的多CPU，完成简单并行化
worker_class = 'eventlet'  # worker的类型，如何选择见：http://docs.gunicorn.org/en/stable/design.html#choosing-a-worker-type （后续实践发现eventlet有一定概率存在兼容问题，如发现Gunicorn无法启动，可以先注释掉）
bind = '0.0.0.0:5000'  # 服务使用的端口
pidfile = currentRootPath + '/logs/gunicorn.pid'  # 存放Gunicorn进程pid的位置，便于跟踪
accesslog = currentRootPath + '/logs/gunicorn.log'  # 存放访问日志的位置，注意首先需要存在logs文件夹，Gunicorn才可自动创建log文件
errorlog = currentRootPath + '/logs/gunicorn.log'  # 存放错误日志的位置，可与访问日志相同
reload = False  # 如果应用的代码有变动，work将会自动重启，适用于开发阶段
daemon = True  # 是否后台运行
timeout = 5  # server端的请求超时秒数

loglevel = 'info' #日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
# access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'    #设置gunicorn访问日志格式，错误日志无法设置
