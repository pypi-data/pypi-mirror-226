#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Default PGP settings.
"""
import os
import sys
# from pyecharts.globals import NotebookType

DEBUG = False if str(os.environ.get("PGP_NOT_DEBUG")) == "1" else True
ISDEV = False if str(os.environ.get("PGP_NOT_DEV")) == "1" else True
ISJUPYTER = True if str(os.environ.get("PGP_JUPYTER")) == "1" else False
RUN_PERMISSION = True if str(os.environ.get("PGP_RUN_PERMISSION")) == "1" else False
CUSTOM_USER_PATH = False if str(os.environ.get("PGP_NOT_USER_PATH")) == "1" else True
PGP_SAVE_PATH = os.environ.get("PGP_SAVE_PATH", "/jtdata/products/data/JTLMOXVE/mlf")
RUN_MODEL_SAVE_PATH = os.environ.get("PGP_RUN_MODEL_SAVE_PATH", "/jtdata/products/data/JTLMOXVE/mlf/models")
PREDICT_MODEL_SAVE_PATH = os.environ.get("PGP_PREDICT_MODEL_SAVE_PATH", '/jtdata/products/data/JTLMOXVE/mlf/models')
PREDICT_RESULT_SAVE_PATH = os.environ.get("PGP_PREDICT_RESULT_SAVE_PATH", '/jtdata/products/data/JTLMOXVE/mlf/predict_result')
TEMP_SAVE_PATH = os.environ.get("PGP_TEMP_SAVE_PATH", "/jtdata/products/data/JTLMOXVE/mlf/temp/")
PGP_CACHE_PATH = os.environ.get("PGP_CACHE_PATH", '')
PGP_RPC_HOST = os.environ.get("PGP_RPC_HOST", "39.105.112.41:6290")
PGP_PREDICT_RPC_HOST = os.environ.get("PGP_PREDICT_RPC_HOST", '39.105.112.41:6290')
PGP_RUN_RPC_HOST = os.environ.get("PGP_RUN_RPC_HOST", '39.105.112.41:6290')
ONLINE_SERVER_HOST = os.environ.get("PGP_ONLINE_SERVER_HOST", '39.105.166.221:8182')
REDIS_HOST = os.environ.get("REDIS_HOST", '39.105.185.60')
REDIS_PORT = int(os.environ.get("REDIS_PORT", '6371'))
PGP_DB_HOST = os.environ.get("PGP_DB_HOST", '39.105.185.60')
PGP_DB_PORT = int(os.environ.get("PGP_DB_PORT", '33061'))
AMQP_URL = os.environ.get("AMQP_URL", 'amqp://10.1.255.1:32228')
RT_DB_HOST = os.environ.get("RT_DB_HOST") or "10.35.13.118"
RUN_TIMEOUT = int(os.environ.get("RUN_TIMEOUT", 60 * 60 * 6))   # 训练超时2小时
PREDICT_TIMEOUT = int(os.environ.get("PREDICT_TIMEOUT", 60 * 10))   # 预测超时5分钟
RT_DB_CONNECTOR = os.environ.get("RT_DB_CONNECTOR", '')
ISONLINE = True if str(os.environ.get("PGP_IS_ONLINE")) == "1" else False

# 运行模式 1: 包引用 2：grpc
RUN_PATTERN = 1

# redis设置
REDIS_DB = 3 if str(os.environ.get("PGP_NOT_DEV")) == "1" else 4
REDIS_KEY_TTL = 7 * 24 * 60 * 60  # 过期时间,默认7天

# celery 存储设置
CELERY_REDIS_HOST = None
CELERY_REDIS_PORT = None
CELERY_REDIS_DB = None


# 时间格式
DATETIME_FORMAT = "%H:%M:%S"
DATETIME_TOTAL_FORMAT = "%Y-%m-%d %H:%M:%S"
DATETIME_INPUT_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
]

# 计算存储引擎
STORAGE_ENGINE = "file"

# 结构数据库配置
DATABASES = {
    "ENGINE": "sqlite3",
    "NAME": "PipeGraphPy",
}

# 数据库配置
DATABASES_POOL = None
# 数据库名称
DATABASE_NAME = None

# 模型保存配置
HOME_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SDK_MODEL_SAVE_PATH = "/data/algo/applications/jupyter/AShare/PGP/PGP-sdk/sdkmodel/"
MODEL_SAVE_NAME = "graph_model_{graph_id}"
ALGO_MODEL_SAVE_NAME = "algo_model_{graph_id}_{node_id}_{algo_mod_type}_{idx}"

# 配置自定义算法代码的保存位置
if not PGP_CACHE_PATH:
    if CUSTOM_USER_PATH:
        PGP_CACHE_PATH = os.path.expanduser('~/.cache/PipeGraphPy/')
    else:
        PGP_CACHE_PATH = os.path.join(PGP_SAVE_PATH, '.cache/PipeGraphPy/')
if not os.path.exists(PGP_CACHE_PATH):
    os.makedirs(PGP_CACHE_PATH)
sys.path.append(PGP_CACHE_PATH)
PGP_CUSTOM_PATH = os.path.join(PGP_CACHE_PATH, 'custom')
if not os.path.exists(PGP_CUSTOM_PATH):
    os.makedirs(PGP_CUSTOM_PATH)
    _init_file = os.path.join(PGP_CUSTOM_PATH, "__init__.py")
    with open(_init_file, "w") as f:
        f.write("#")

# jupyter_type
# JUPYTER_TYPE = NotebookType.JUPYTER_LAB


# SDK是否显示log日志
SDK_SHOW_LOG = False

# RPC配置
RPC_MAX_MESSAGE_LENGTH             = 256*1024*1024   # RPC传输的最大数据量
RPC_MAX_WORKERG                    = 100             # RPC连接最大数量
RPC_KEEPALIVE_TIME_MS              = 10 * 60 * 1000  # 发送keepalive探测消息的频度
RPC_KEEPALIVE_TIMEOUT_MS           = 6 * 60 * 1000   # keepalive 探测应答超时时间
RPC_KEEPALIVE_PERMIT_WITHOUT_CALLS = 1               # 是否允许在没有任何调用时发送 keepalive

# 回测最大特征数量
FONT_MAX_FEATURE_NUM = 100
