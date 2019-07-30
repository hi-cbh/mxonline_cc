import pymysql

pymysql.install_as_MySQLdb()

# import os
#
# PATH = lambda p: os.path.abspath(
#     os.path.join(os.path.dirname(os.path.dirname(__file__)), p)
# )

import sys,os
# pa = "/Users/apple/djangoProject/extra_apps"
# sys.path.append(pa)
# sys.path.insert(0,pa)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(BASE_DIR,'extra_apps'))
