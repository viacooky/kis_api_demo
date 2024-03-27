# coding:utf-8
import requests
import utils

client_id = '272913'
client_secret = 'c13e5ae8fa744bbc13128cb945fbaaa0'
app_key = 'oIDAZXAr'
app_secret = '2a279e79545f67d062c73b58018469b6a013e7a2'
instance_id = '254378485894746112'

host = 'https://api.kingdee.com'

headers_base = {
    'Content-Type': 'application/json',
    'X-Api-Auth-Version': '2.0',
    'X-Api-SignHeaders': 'X-Api-TimeStamp,X-Api-Nonce',
    'X-Api-ClientID': '',
    'X-Api-TimeStamp': '',
    'X-Api-Nonce': '',
    'X-Api-Signature': '',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
}


def kingdee_auth_token() -> None:
    """获取KIS-Authdata
    https://open.jdy.com/#/files/api/detail?index=3&categrayId=dded94c553614747b2c9b8b49c396aa6&id=c26bb0d8171a11eebf32e51b6b676a52
    """

    path = '/jdyconnector/app_management/kingdee_auth_token'

    # 构建params
    params = {
        'app_key': app_key,
        'app_signature': utils.gen_sign(app_secret, app_key),
    }

    # 构建headers
    headers = headers_base.copy()
    headers.update({
        'X-Api-ClientID': client_id,
        'X-Api-TimeStamp': utils.get_timestamp(),
        'X-Api-Nonce': utils.gen_random_num()
        # 'X-Api-TimeStamp': '1711574854959',
        # 'X-Api-Nonce': '1424555405'
    })

    api_sign = utils.gen_api_sign(client_secret=client_secret,
                                  method='get',
                                  path=path,
                                  params=params,
                                  headers=headers)
    headers.update({
        'X-Api-Signature': api_sign,
    })

    # 请求
    url = f'{host}{path}'
    resp = requests.get(url, params=params, headers=headers)
    return resp.json()


def push_app_authorize():
    """主动获取授权
    https://open.jdy.com/#/files/api/detail?index=4&categrayId=5403e0fd6a5811eda819b759130d6d33&id=801d558dda9d11edbfb2d572de04f9ce
    """

    path = '/jdyconnector/app_management/push_app_authorize'

    # 构建params
    params = {
        'outerInstanceId': instance_id,  # 第三方实例ID
    }

    # 构建headers
    headers = headers_base.copy()
    headers.update({
        'X-Api-ClientID': client_id,
        'X-Api-TimeStamp': utils.get_timestamp(),
        'X-Api-Nonce': utils.gen_random_num()
    })

    api_sign = utils.gen_api_sign(client_secret=client_secret,
                                  method='post',
                                  path=path,
                                  params=params,
                                  headers=headers)
    headers.update({
        'X-Api-Signature': api_sign,
    })

    # 请求
    url = f'{host}{path}'
    resp = requests.post(url, params=params, headers=headers)
    return resp.json()


def material_list(auth_data: str, access_token: str, gw_addr: str):
    """批量查询物料基础资料详情
    https://open.jdy.com/#/files/api/detail?index=3&categrayId=dded94c553614747b2c9b8b49c396aa6&id=fa051e46753111ed86f7a5f91c861e59

    https://api.kingdee.com/koas/APP006992/api/Material/List?access_token=xxxxx

    POST

    备注：
    URL:
        access_token : kingdee_auth_token 接口结果的 access_token
    headers:
        KIS-AuthData : kingdee_auth_token 接口结果的 auth_data
        X-GW-Router-Addr : push_app_authorize 接口结果的 domain
    params:
        不用签名，直接写
    """
    path = '/koas/APP006992/api/Material/List'

    # 构建params
    params = {
        'CurrentPage': 1,
        'ItemsOfPage': 10,
        'ParentId': 0,
        'Detail': True,
        'SearchKey': '',
        'Ids': [],
    }

    # 构建headers
    headers = {
        'Content-Type': 'application/json',
        'KIS-Timestamp': utils.get_timestamp(),
        'KIS-State': utils.gen_random_num(length=16),
        'KIS-TraceID': 'py-api-test',
        'KIS-AuthData': auth_data,
        'KIS-Ver': '1.0',
        'X-GW-Router-Addr': gw_addr,
    }
    url = f'{host}{path}?access_token={access_token}'
    resp = requests.post(url, params=params, headers=headers)
    return resp.json()


def user_list(auth_data: str, access_token: str, gw_addr: str):
    """批量查询用户
    https://open.jdy.com/#/files/api/detail?index=3&categrayId=dded94c553614747b2c9b8b49c396aa6&id=da5973be754211ed86f7cfa07425bf5d

    https://api.kingdee.com/koas/APP006992/api/User/List?access_token=xxxxx

    POST
    """
    path = '/koas/APP006992/api/User/List'

    # 构建params
    params = {
        'CurrentPage': 1,
        'ItemsOfPage': 10,
        # 'Search':'',
    }

    # 构建headers
    headers = {
        'Content-Type': 'application/json',
        'KIS-Timestamp': utils.get_timestamp(),
        'KIS-State': utils.gen_random_num(length=16),
        'KIS-TraceID': 'py-api-test',
        'KIS-AuthData': auth_data,
        'KIS-Ver': '1.0',
        'X-GW-Router-Addr': gw_addr,
    }
    url = f'{host}{path}?access_token={access_token}'
    resp = requests.post(url, params=params, headers=headers)
    return resp.json()


if __name__ == '__main__':

    # ------------- 获取KIS-Authdata -------------
    data_kingdee_auth = kingdee_auth_token()
    uid = data_kingdee_auth['data']['uid']
    app_token = data_kingdee_auth['data']['app-token']
    access_token = data_kingdee_auth['data']['access_token']

    # app_token = 'ZVVGSFUySkRjRTF3UkhWblduVkxiSEZrTUdoa1REWTRlVlZvZVZka1pXeGhhSHAwV1VOWGNqaFVVVVozUlZwdVIzcE9lVGhKZVM5NWQwdHBkbXR5YUc5MlZIWlpSVVI2UzJwbFdFcEhXRUpRU25CdFRXdzNWWFI2VlV4T1ZsRjZkMnhsZFhsTVZsUTBTVlp2YzJ0U1NIcGxhRk15TXpsb2NqVm9TMnROU2pkUVN6aFBSQzh5ZUZwbGFGUkdkVWRLV0VKdlkzRk1kRGxpTTNOa1UzcFRiR3B2UjJNeVlqUmpNakJZYVdKV1NUaGtZMEpwT1daWE5HUnpPRzFhUm0wME5HODNlVlp2Y21RM016Z3ljVmREWW5KNGRHZE5iMnB2TjFreEszVTJXbmN2WjJwVVQwSmlSVlV5ZVZsVlpVZDFWV0prZEVWYU1HNURNelUyZFhSQ2NGVlhhVzlhUTBkMWNEaE9hMHRHUTFCVVdqbFNSeXRLYWpjM2VGbFdZMUZDVFRGT0swSjJZbU54U0VweFMwdHBVRFpFY0ZoUGNtZDBkRTh3UWs1bmVISXJURXg1VkVwUVFXeENjbGNyU1hKbFpVZElhR2hxVld0RVJXUnNhVkExV2tSSWNqUllhMGh0YVVWaGNVc3pZVkY0VDNSeFRURmxiR3QwUWpONGQwVjRWRVZLTTJnellVcEpTMVE1VGk5MVZpOHpSa0ZNU21wblUwUkxkRlJFVjNKRlRVTTRhRkJTZWpoaWF6MD0ja29hczE3MTE1NzU2NDN5bGNuamh5ZnNpdmhnbm1qbWNqdmV3'
    # access_token = '17114728197ead93c14acd6c96190cd6'

    # ------------- 获取KIS-Authdata -------------


    # ------------- 主动获取授权 -------------
    # data_app_auth = push_app_authorize()

    accountId = data_app_auth['data'][0]['accountId']
    serviceId = data_app_auth['data'][0]['serviceId']
    domain = data_app_auth['data'][0]['domain']

    # accountId = 'SDBOX149779911688435438829'
    # serviceId = '1710488587a13ab617dbb6d34a5b4bee'
    # domain = 'http://101.42.132.11'

    # ------------- 主动获取授权 -------------

    # ------------- 业务数据接口 -------------
    data_material_list = material_list(
        auth_data=app_token,
        access_token=access_token,
        gw_addr=domain)

    # 这里应该是帐套没有物料 或是沙箱的数据问题
    # 'errcode': 10201, 'description': '业务接口返回失败结果，失败原因：403-ParseRequestContent:{"AuthData":{"EID":"16140594","Timestamp":"56207-09-26 01:55:35","Source":"","OpenID":0,"IsEncrypt":"N","Method":"kis.APP006992.api.Material.List","Sign":"91c59aa76d860eef4c90fdc05ed6c38f","State":"2375492168968470","Ver":"1.0"},"BizData":}\r\n请求参数转换成JSON对象异常
    # ------------- 业务数据接口 -------------

    data_user_list = user_list(
        auth_data=app_token,
        access_token=access_token,
        gw_addr=domain)

    # 可能是沙箱的数据问题
    # 'errcode': 10201, 'description': '业务接口返回失败结果，失败原因：403-ParseRequestContent:{"AuthData":{"EID":"16140594","Timestamp":"56207-09-26 01:55:35","Source":"","OpenID":0,"IsEncrypt":"N","Method":"kis.APP006992.api.Material.List","Sign":"91c59aa76d860eef4c90fdc05ed6c38f","State":"2375492168968470","Ver":"1.0"},"BizData":}\r\n请求参数转换成JSON对象异常
    
    
    # ------------- 业务数据接口 -------------
    
