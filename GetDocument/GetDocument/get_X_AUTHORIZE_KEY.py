import random
import hashlib
import time


def getWW():
    return str(1000 * 1000 * random.random())[0:6]


def getV():
    return str(time.time())[0:10]


def getTime():
    return str(time.time())[5:8]


def getX_AUTHORIZE_KEY(ww, v):
    a = int(v[-1])
    b = int(v[-2])
    S_key = "7veTpnogkH6LG7JPK5kW0JBF8bFJTM8I"
    md5Key = "createElement" + ww + v + S_key + S_key[a:a + b]
    print(md5Key)
    md5 = hashlib.md5()
    md5.update(md5Key.encode('utf-8'))
    return md5.hexdigest()