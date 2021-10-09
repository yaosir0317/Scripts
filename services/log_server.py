# build-in
import os
import sys
import json
import traceback
import logging.handlers
import logging
from logging import Handler
from threading import Thread
from datetime import datetime
# third-party
import requests


# 飞书接收报警url
URL = "https://open.feishu.cn/open-apis/bot/hook/15bb27b5e4f7454eab8816b080ef99bd"
# 出发飞书报警的日志级别
LOG_LEVEL = 40


def postpone(function):
    def postpone_decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = False
        t.start()

    return postpone_decorator


class SendFeiShuHandler(Handler):
    """
    An exception log handler that emails log entries to settings.EXCEPTION_MAIL_LIST.
    """
    active_count = 0

    @postpone
    def send_exceptions(self, title, content):
        txt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "\r\n" + content
        requests.post(url=URL, data=json.dumps({
            "title": title,
            "text": txt
        }))

    def emit(self, record):
        subject = '%s: %s %s' % (
            'Daily Script Exception',
            record.levelname,
            record.getMessage()
        )

        def format_subject(subject_info):
            """
            Escape CR and LF characters.
            """
            return subject_info.replace('\n', ' ').replace('\r', ' ')

        subject = format_subject(subject)  # 邮件标题
        # sourceInfo是放于extra的信息
        extra = getattr(record, "sourceInfo") if hasattr(record, "sourceInfo") else ""
        message = record.getMessage() + '\n' + traceback.format_exc() + "\n" + extra
        self.send_exceptions(subject, message)


# 读取日志文件保存路径
log_path = ""  # TODO
# 读取日志文件容量，转换为字节
log_size = 1024 * 1024 * 64
# 读取日志文件保存个数
log_num = 1
# 日志文件名：由用例脚本的名称，结合日志保存路径，得到日志文件的绝对路径
log_name = os.path.join(log_path, "{}.log".format(sys.argv[0].split('/')[-1].split('.')[0]))
# 初始化logger
logger = logging.getLogger()
# 日志格式，可以根据需要设置
fmt = logging.Formatter('%(asctime)s\t%(filename)s\tline:%(lineno)d\t%(levelname)s\t%(message)s',
                        '%Y-%m-%d %H:%M:%S')
# 日志输出到文件，这里用到了上面获取的日志名称，大小，保存个数
handle1 = logging.handlers.RotatingFileHandler(log_name, maxBytes=log_size, backupCount=log_num)
handle = logging.handlers.TimedRotatingFileHandler(log_name, when="D", interval=1, backupCount=15)
handle.setFormatter(fmt)
# 同时输出到屏幕，便于实施观察
handle2 = logging.StreamHandler(stream=sys.stdout)
handle2.setFormatter(fmt)
# 飞书报警
handle3 = SendFeiShuHandler(LOG_LEVEL)
logger.addHandler(handle)
logger.addHandler(handle2)
logger.addHandler(handle3)
# 设置日志基本，这里设置为INFO，表示只有INFO级别及以上的会打印
logger.setLevel(logging.INFO)
