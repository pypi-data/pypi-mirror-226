from deskaone_requests.Requests import Requests
from deskaone_requests.Utils.Crypto import Crypto

from requests.cookies import RequestsCookieJar
from requests.auth import AuthBase
from requests import PreparedRequest, Response as Res

from urllib.parse import urlencode

import json, time, base64, hmac

from typing import Union, Dict, Mapping, List, Optional, Tuple

class Error(Exception): ...

class __Auth__(AuthBase):
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        timestamp   = str(int(time.time() * 1000))
        message     = str(timestamp + request.method + request.path_url + (request.body or ''))
        signature   = base64.b64encode(hmac.new(self.secret_key.encode(), message.encode(), 'SHA256').digest()).decode()
        request.headers.update({
            'User-Agent'    : f'DesKaOne-Requests@0.0.1',
            'SIGNATURE'     : signature,
            'TIMESTAMP'     : timestamp,
            'VERSION'       : '0.0.1'
        })
        return request

class Client:
    
    def __init__(self, url: str, secretKey: str, params = None, proxies = None, Local = True, method = 'GET', headers: Optional[dict] = None) -> None:
        self.__ipCheck__            = 'https://ipv4.webshare.io/'
        self.__crypto__             = Crypto.AES()
        self.__crypto__.randomIv()
        self.__crypto__.randomKey()
        self.__scraper__            = Requests.create_scraper()
        try: self.__myIp__          = self.__scraper__.get(self.__ipCheck__).text
        except Exception as e: raise Error(str(e))
        self.__scraper__.proxies    = dict() if proxies is None else proxies
        self.__params__             = params
        self.__secretKey__          = secretKey
        self.__url__                = url
        self.__local__              = Local
        self.__method__             = method
        self.__headers__            = dict() if headers is None else headers
    
    def setProxy(self, proxies: dict):
        self.__scraper__.proxies = dict() if proxies is None else proxies
        
    def setParamsLocal(self, params: dict):
        self.__crypto__.setData_FromString(json.dumps(params, separators=(',', ':')))
        DATA = f'{len(self.__crypto__.getIv_to_Hex())}|{len(self.__crypto__.getKey_to_Hex())}|{len(self.__crypto__.encrypt_to_hex())}|{self.__crypto__.getKey_to_Hex()}{self.__crypto__.getIv_to_Hex()}{self.__crypto__.encrypt_to_hex()}'
        self.__params__  = json.dumps(dict(DATA = DATA), separators=(',', ':'))
        
    def setParamsServer(self, Mode : int, params: dict):
        if Mode == 1: self.__params__ = urlencode(params)
        else: self.__params__ = json.dumps(params, separators=(',', ':'))
    
    def __decode__(self, response: Res):
        SPLIT   = str(response.content.decode()).split('|')
        self.__crypto__.setKey_from_Hex(SPLIT[3][:int(SPLIT[1])])
        self.__crypto__.setIv_from_Hex(SPLIT[3][int(SPLIT[1]):int(SPLIT[1]) + int(SPLIT[0])])
        self.__crypto__.setData_FromHex(SPLIT[3][int(SPLIT[1]) + int(SPLIT[0]):])    
        return self.__crypto__.decrypt_to_dict()
    
    @property
    def Server(self):
        if self.__method__ == 'GET':
            response = self.__scraper__.get(self.__url__, headers = self.__headers__)
        else:
            response = self.__scraper__.post(self.__url__, data=self.__params__, headers = self.__headers__)
        #return response.content.decode()
        return dict(
            result      = response.content.decode(),
            status_code = response.status_code,
            headers     = dict(
                request     = dict(response.request.headers),
                response    = dict(response.headers)
            ),
            method      = response.request.method,
            body        = response.request.body,
            proxies     = self.__scraper__.proxies,
            myIp        = self.__myIp__,
        )
    
    @property
    def Local(self) -> Union[Dict[str, Dict[any, any]], int, RequestsCookieJar, List[Res], str, bytes, Dict[str, str], Mapping]:
        if self.__local__ is True: 
            self.__scraper__.proxies = dict()
            self.__myProxy__   = self.__scraper__.get(self.__ipCheck__).text
        else:
            try: self.__myProxy__   = self.__scraper__.get(self.__ipCheck__).text
            except Exception as e: raise Error(str(e))
        if self.__params__ is None:
            response = self.__scraper__.get(self.__url__, auth=__Auth__(self.__secretKey__))
        else:
            response = self.__scraper__.post(self.__url__, data=self.__params__, auth=__Auth__(self.__secretKey__))
        return dict(
            result      = self.__decode__(response),
            status_code = response.status_code,
            headers     = dict(
                request     = response.request.headers,
                response    = response.headers
            ),
            cookies     = response.cookies,
            history     = response.history,
            method      = response.request.method,
            body        = response.request.body,
            proxies     = self.__scraper__.proxies,
            myIp        = self.__myIp__,
            myProxy     = self.__myProxy__
        )
  
    
    