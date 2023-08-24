

# 获取几个环境变量
# EZCONFIG_ENV
# EZCONFIG_APPID
# EZCONFIG_SECRET

import os
import requests
import sys
import json

# 获取环境变量
_EZCONFIG_ENV = os.getenv('EZCONFIG_ENV', 'DEV')
_EZCONFIG_APPID = os.getenv('EZCONFIG_APPID', '')
_EZCONFIG_SECRET = os.getenv('EZCONFIG_SECRET', '')
_EZCONFIG_HOST = os.getenv('EZCONFIG_HOST', 'http://localhost:8080')

# 获取最新配置的URL Path
_config_path = "/api/config/{APPID}/{ENV}"
# 获取配置最新版本号的URL Path
_config_version_path = "/api/version/{APPID}/{ENV}"

# 获取最新配置的URL
_config_url = _EZCONFIG_HOST + _config_path.format(APPID=_EZCONFIG_APPID, ENV=_EZCONFIG_ENV)
# 获取配置最新版本号的URL
config_version_url = _EZCONFIG_HOST + _config_version_path.format(APPID=_EZCONFIG_APPID, ENV=_EZCONFIG_ENV)
# Authorization header 值
auth_token = "Bearer {}:{}".format(_EZCONFIG_APPID, _EZCONFIG_SECRET)


# 从ezconfig获取配置
def get_latest_config() -> {"version": int, "config_data": dict, "config_hash": str}:
    """
    从ezconfig获取配置
    :return: {"version": int, "config_data": dict, "config_hash": str}
    """
    # 获取最新配置
    response = requests.get(_config_url, headers={'Authorization': auth_token})
    if response.status_code != 200:
        print("获取最新配置失败，错误码：{}".format(response.status_code))
        exception = Exception("获取最新配置失败，http请求status code错误码：{}".format(response.status_code))
        raise exception
    response_data = response.json()
    if response_data['errno'] != 0:
        exception = Exception("获取最新配置失败，错误码：{}, 错误信息：".format(response_data['errno'], response_data['errmsg']))
        raise exception
    return response.json()["data"]

