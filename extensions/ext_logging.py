# extensions/ext_logging.py

import logging
from fastapi import FastAPI
from logging.handlers import RotatingFileHandler

def is_enabled() -> bool:
    return True

def init_app(app: FastAPI):
    log_level = logging.INFO

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
    )

    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 文件输出
    file_handler = RotatingFileHandler(
        filename="app.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    # 设置日志
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    logging.getLogger().info("Logging has been initialized.")

def shutdown_app(app: FastAPI):
    logging.getLogger().info("Shutting down logging.")


# TODO

# JSON 日志格式化？

# 每个模块单独日志文件？

# 根据 ENV 切换日志级别？

# 添加错误捕获日志（全局异常处理）？