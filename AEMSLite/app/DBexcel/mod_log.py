import logging.handlers

class Logger(logging.Logger):
    def __init__(self,filename=None):
        super(Logger,self).__init__(self)

        #日志文件名
        if filename is None:
            filename = 'DBexcel/log.log'
        self.filename = filename

        #创建handler(每天生成一个,保留30天的日志)
        fh = logging.handlers.TimedRotatingFileHandler(self.filename,'D',1,30)
        fh.suffix = "%Y%m%d-%H%m.log"
        fh.setLevel(logging.DEBUG)

        #这个handler用于输出控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        #定义handler的输出格式
        formatter = logging.Formatter('[%(asctime)s] - %(filename)s - [Line:%(lineno)d] - [%(levelname)s] - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        #给Logger添加handler
        self.addHandler(fh)
        self.addHandler(ch)
logger = Logger()