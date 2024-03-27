# coding:utf-8
import time
import hmac
import base64
import hashlib
import random
# import urllib
from urllib.parse import *


def get_timestamp() -> str:
    """获取时间戳（后三位为小数部分）
    """
    time_value = time.time()
    second, millisecond = str(time_value).split('.')
    return f'{second}{millisecond[:3]}'


def gen_random_num(length: int = 10) -> str:
    """生成随机数

    Args:
        int (length, optional): 长度. Defaults to 10.
    """
    first_num = random.randint(1, 9)
    choices = list(range(0, 10))
    else_num = [str(i) for i in random.choices(choices, k=length - 1)]
    return f'{first_num}{"".join(else_num)}'


def gen_sign(app_secret: str, data: str) -> str:
    """生成App签名

    Args:
        str (app_secret): app_secret
        str (data): 数据
    """
    # sign_hex = hmac.new(key=app_secret.encode('utf-8'),
    #                     msg=data.encode('utf-8'),
    #                     digestmod=hashlib.sha256).hexdigest()
    # rs = base64.b64encode(sign_hex.encode('utf-8')).decode('utf-8')

    signature_hex = hmac.new(key=app_secret.encode('utf-8'),
                             msg=data.encode('utf-8'),
                             digestmod=hashlib.sha256).hexdigest()
    signature_hex_base64 = base64.b64encode(signature_hex.encode('utf-8'))
    signature_result = signature_hex_base64.decode('utf-8')

    return signature_result


def gen_api_sign(client_secret: str,method: str, path: str, params: dict, headers:dict, *kwargs: any) -> str:
    """生成api签名
    参考:https://open.jdy.com/#/files/api/detail?index=3&categrayId=316e1f5bd9d711ed8e36c17691e84ff5&id=88a64277da6611edbfb253e5081eb1e3
    X-Api-Signature生成规则部分

    Args:
        str (method): 请求方法 POST、GET、DELETE等，要求大写，方法已处理
        str (path): 请求path
        dict (params): 请求参数
        dict (headers): headers
    """
    # 方法名大写
    method_str = method.upper()

    # path url编码
    path_str = quote_plus(path)

    # params 的值 进行 两次url编码
    params_str = '&'.join(
        [f'{k}={quote(quote(v))}' for k, v in params.items()]) if params else ''

    # 提取需要参与签名的参数
    tmp_headers = {k.lower(): v for k, v in headers.items()}
    sign_headers = {
        'x-api-nonce':tmp_headers['x-api-nonce'],
        'x-api-timestamp':tmp_headers['x-api-timestamp']
    }
    # 拼接headers字符串
    headers_str = '\n'.join([f'{k}:{v}' for k,v in sign_headers.items()])

    # 拼接参与签名的字符串参数
    sign_str = '\n'.join([method_str,path_str,params_str,headers_str])
    # 再补充个换行符
    sign_str = f'{sign_str}\n'

    # 签名
    aaa= gen_sign(client_secret,sign_str)
    return aaa



