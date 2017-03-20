#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname

import app

sys.path.insert(0, abspath(dirname(__file__)))
# wsgi 文件所在目录的绝对路径 插入到 sys.path 的最顶层
# 确保 import app 模块的时候优先搜索

application = app.configured_app()
