from typing import Dict, List, Optional

from .Database import Database, declarative, db
from .Typer import Typer
from .Color import Color

from sqlalchemy.dialects.sqlite import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InterfaceError

import json, requests, re, random

from deskaone_requests.Exceptions import Error
from bs4 import BeautifulSoup


Base = declarative()

class DatabaseProxy:
    
    class Base:
        
        def __init__(self) -> None:
            self.DB = Database.Connection('Proxy', Base)
        
        
        class Proxy(Base):
            
            __tablename__   = 'Proxy'    
            id              = db.Column(INTEGER(), primary_key=True)
            country         = db.Column(VARCHAR(255), nullable=False)
            countryCode     = db.Column(VARCHAR(255), nullable=False)
            IpPort          = db.Column(VARCHAR(255), unique=True, nullable=False)
            Proxies         = db.Column(VARCHAR(255), nullable=False)
        
            def __repr__(self) -> str:
                return  json.dumps(dict(
                    id              = self.id,
                    country         = self.country,
                    countryCode     = self.countryCode,
                    IpPort          = self.IpPort,
                    Proxies         = json.loads(self.Proxies)
                ), indent=4)
    
    class Proxys:
        
        class Connection:
        
            def __init__(self) -> None:
                self.Func        = DatabaseProxy.Base()
                self.Con         = self.Func.DB
                self.Engine      = self.Con.Engine
                self.Metadata    = self.Con.Metadata
        
        class SaveProxy(Connection):
            
            def Set(self, *args, **kwargs):
                if kwargs.get('IpPort') is None or kwargs.get('IpPort') == '':raise Error('IpPort Required')
                Session     = sessionmaker(bind=self.Engine)
                Session.configure(bind=self.Engine)
                session     = Session()
                try:
                    ed_user = self.Func.Proxy(
                        country         = kwargs.get('country'),
                        countryCode     = kwargs.get('countryCode'),
                        IpPort          = kwargs.get('IpPort'),
                        Proxies         = json.dumps(kwargs.get('Proxies')) if type(kwargs.get('Proxies')) == dict else kwargs.get('Proxies')
                    )
                    session.add(ed_user)
                    session.commit()
                    session.close()
                    return True
                except (IntegrityError, InterfaceError) as e:
                    return False
                
            def Get(self):
                Session     = sessionmaker(bind=self.Engine)
                Session.configure(bind=self.Engine)
                session     = Session()
                result  = session.query(self.Func.Proxy).filter().all()
                session.close()
                return [dict(json.loads(str(Dict))) for Dict in result]

            def GetByIpPort(self, IpPort: str):
                if IpPort is None or IpPort == '':raise Error('IpPort Required')
                Session     = sessionmaker(bind=self.Engine)
                Session.configure(bind=self.Engine)
                session     = Session()
                result  = session.query(self.Func.Proxy).filter_by(IpPort=IpPort).first()
                session.close()
                return dict(json.loads(str(result)))
            
            def Up(self, IpPort: str, Values: dict):
                try:
                    if IpPort is None or IpPort == '':raise Error('IpPort Required')
                    Session     = sessionmaker(bind=self.Engine)
                    Session.configure(bind=self.Engine)
                    session     = Session()
                    result  = session.query(self.Func.Proxy).filter_by(IpPort=IpPort).update(Values)
                    session.commit()
                    session.close()
                    return result
                except InterfaceError:
                    return 0
        
            def Del(self, IpPort: str):
                if IpPort is None or IpPort == '':raise Error('IpPort Required')
                Session     = sessionmaker(bind=self.Engine)
                Session.configure(bind=self.Engine)
                session     = Session()
                result  = session.query(self.Func.Proxy).filter_by(IpPort=IpPort).delete()
                session.commit()
                session.close()
                return result
        
            def DelAll(self):
                Session     = sessionmaker(bind=self.Engine)
                Session.configure(bind=self.Engine)
                session     = Session()
                result  = session.query(self.Func.Proxy).filter().delete()
                session.commit()
                session.close()
                return result

class SearchProxy:
    
    class Request:
        
        def __init__(self, Search: bool) -> None:
            self.Session    = requests.Session()
    
    class WebShare(Request):
        
        def __init__(self, Search: bool, Authorization: str) -> None:
            super().__init__(Search)
            self.BASE_URL   = 'https://proxy.webshare.io/api/v2/'
            self.HEADERS    = dict(Authorization = Authorization)
            if Search:
                SProxy: List[Dict[str, any]]
                SProxy = list()
                for I in range(1, 100000):
                    try:
                        URL     = self.BASE_URL + f'proxy/list/?mode=direct&page={I}&page_size=100'
                        Result  = self.Session.get(URL, headers=self.HEADERS).json()
                        for P in Result.get('results'):
                            SProxy.append(P)
                    except TypeError as e:
                        X = re.search('NoneType', str(e))
                        if X:
                            break
                for Proxy in SProxy:
                    USERNAME        = Proxy.get('username')
                    PASSWORD        = Proxy.get('password')
                    IP              = Proxy.get('proxy_address')
                    PORT            = Proxy.get('port')
                    SCHEMA      = 'http'
                    try:
                        set = DatabaseProxy.Proxys.SaveProxy().Set(
                            country         = '',
                            countryCode     = '',
                            IpPort          = f'{IP}:{PORT}',
                            Proxies         = dict(
                                http    = f'{SCHEMA}://{USERNAME}:{PASSWORD}@{IP}:{PORT}',
                                https   = f'{SCHEMA}://{USERNAME}:{PASSWORD}@{IP}:{PORT}',
                            )
                        )
                        if set is False: DatabaseProxy.Proxys.SaveProxy().Up(IpPort = f'{IP}:{PORT}', Values = dict(
                            country         = '',
                            countryCode     = '',
                            Proxies         = dict(
                                http    = f'{SCHEMA}://{USERNAME}:{PASSWORD}@{IP}:{PORT}',
                                https   = f'{SCHEMA}://{USERNAME}:{PASSWORD}@{IP}:{PORT}',
                            )
                        ))
                    except Error:pass

    class ProxyScrape(Request):
        
        def __init__(self, Search: bool) -> None:
            super().__init__(Search)
            if Search:
                URL     = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all'
                Result  = self.Session.get(URL).text
                Saves = [Proxy for Proxy in Result.replace(' ', '').replace('\r', '').split('\n')]
                for i in range(len(Saves)):
                    Proxy = Saves[random.randint(0, len(Saves) - 1)]
                    try:
                        DatabaseProxy.Proxys.SaveProxy().Set(
                            country         = '',
                            countryCode     = '',
                            IpPort          = Proxy,
                            Proxies         = dict(
                                http    = f'http://{Proxy}',
                                https   = f'http://{Proxy}',
                            )
                        )
                    except Error:pass
                
                URL     = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=5000&country=all&ssl=all&anonymity=all'
                Result  = self.Session.get(URL).text
                Saves = [Proxy for Proxy in Result.replace(' ', '').replace('\r', '').split('\n')]
                for i in range(len(Saves)):
                    Proxy = Saves[random.randint(0, len(Saves) - 1)]
                    try:
                        DatabaseProxy.Proxys.SaveProxy().Set(
                            country         = '',
                            countryCode     = '',
                            IpPort          = Proxy,
                            Proxies         = dict(
                                http    = f'socks4://{Proxy}',
                                https   = f'socks4://{Proxy}',
                            )
                        )
                    except Error:pass
                
                URL     = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=5000&country=all&ssl=all&anonymity=all'
                Result  = self.Session.get(URL).text
                Saves = [Proxy for Proxy in Result.replace(' ', '').replace('\r', '').split('\n')]
                for i in range(len(Saves)):
                    Proxy = Saves[random.randint(0, len(Saves) - 1)]
                    try:
                        DatabaseProxy.Proxys.SaveProxy().Set(
                            country         = '',
                            countryCode     = '',
                            IpPort          = Proxy,
                            Proxies         = dict(
                                http    = f'socks5://{Proxy}',
                                https   = f'socks5://{Proxy}',
                            )
                        )
                    except Error:pass
        
    class Geonode(Request):
        
        def __init__(self, Search: bool) -> None:
            super().__init__(Search)
            if Search:
                self.BASE_URL   = 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&speed=medium&protocols=http%2Chttps%2Csocks4%2Csocks5'
                Result  = self.Session.get(self.BASE_URL).json()
                data    = list(Result.get('data'))
                Saves: List[dict] = [List for List in data]
                for i in range(len(Saves)):
                    Proxy = Saves[random.randint(0, len(Saves) - 1)]
                    IP      = Proxy.get('ip')
                    PORT    = Proxy.get('port')
                    SCHEMA  = Proxy.get('protocols')[0]
                    try:
                        DatabaseProxy.Proxys.SaveProxy().Set(
                            country         = '',
                            countryCode     = '',
                            IpPort          = f'{IP}:{PORT}',
                            Proxies         = dict(
                                http    = f'{SCHEMA.lower()}://{IP}:{PORT}',
                                https   = f'{SCHEMA.lower()}://{IP}:{PORT}',
                            )
                        )
                    except Error:pass
    
    class FreeProxyList(Request):
        
        def __init__(self, Search: bool) -> None:
            super().__init__(Search)
            if Search:
                self.BASE_URL   = 'https://free-proxy-list.net/'
                r  = self.Session.get(self.BASE_URL)
                Result = BeautifulSoup(r.content, 'html5lib')
                Saves = [List for List in Result.findAll('tbody')[0].findAll('tr')]
                for i in range(len(Saves)):
                    Proxy = Saves[random.randint(0, len(Saves) - 1)]
                    SPLIT   = str(Proxy).split('td>')
                    IP      = SPLIT[1].split('</')[0]
                    PORT    = SPLIT[3].split('</')[0]
                    try:
                        DatabaseProxy.Proxys.SaveProxy().Set(
                            country         = '',
                            countryCode     = '',
                            IpPort          = f'{IP}:{PORT}',
                            Proxies         = dict(
                                http    = f'http://{IP}:{PORT}',
                                https   = f'http://{IP}:{PORT}',
                            )
                        )
                    except Error:pass
    
    class ProxyList(Request):
        
        def __init__(self, Search: bool) -> None:
            super().__init__(Search)
            if Search:
                r  = self.Session.get('https://www.proxy-list.download/HTTP')
                Result = BeautifulSoup(r.content, 'html5lib')
                Saves = [List for List in Result.findAll('tbody', attrs={'id': 'tabli'})[0].findAll('tr')]
                for i in range(len(Saves)):
                    Proxy = Saves[random.randint(0, len(Saves) - 1)]
                    SPLIT   = str(Proxy).split('td>')
                    IP      = SPLIT[1].replace(' ', '').replace('\n', '').replace('\r', '').split('</')[0]
                    PORT    = SPLIT[3].replace(' ', '').replace('\n', '').replace('\r', '').split('</')[0]
                    try:
                        DatabaseProxy.Proxys.SaveProxy().Set(
                            country         = '',
                            countryCode     = '',
                            IpPort          = f'{IP}:{PORT}',
                            Proxies         = dict(
                                http    = f'http://{IP}:{PORT}',
                                https   = f'http://{IP}:{PORT}',
                            )
                        )
                    except Error:pass
                
                r  = self.Session.get('https://www.proxy-list.download/HTTPS')
                Result = BeautifulSoup(r.content, 'html5lib')
                Saves = [List for List in Result.findAll('tbody', attrs={'id': 'tabli'})[0].findAll('tr')]
                for i in range(len(Saves)):
                    Proxy = Saves[random.randint(0, len(Saves) - 1)]
                    SPLIT   = str(Proxy).split('td>')
                    IP      = SPLIT[1].replace(' ', '').replace('\n', '').replace('\r', '').split('</')[0]
                    PORT    = SPLIT[3].replace(' ', '').replace('\n', '').replace('\r', '').split('</')[0]
                    try:
                        DatabaseProxy.Proxys.SaveProxy().Set(
                            country         = '',
                            countryCode     = '',
                            IpPort          = f'{IP}:{PORT}',
                            Proxies         = dict(
                                http    = f'http://{IP}:{PORT}',
                                https   = f'http://{IP}:{PORT}',
                            )
                        )
                    except Error:pass
                    
                r  = self.Session.get('https://www.proxy-list.download/SOCKS4')
                Result = BeautifulSoup(r.content, 'html5lib')
                Saves = [List for List in Result.findAll('tbody', attrs={'id': 'tabli'})[0].findAll('tr')]
                for i in range(len(Saves)):
                    Proxy = Saves[random.randint(0, len(Saves) - 1)]
                    SPLIT   = str(Proxy).split('td>')
                    IP      = SPLIT[1].replace(' ', '').replace('\n', '').replace('\r', '').split('</')[0]
                    PORT    = SPLIT[3].replace(' ', '').replace('\n', '').replace('\r', '').split('</')[0]
                    try:
                        DatabaseProxy.Proxys.SaveProxy().Set(
                            country         = '',
                            countryCode     = '',
                            IpPort          = f'{IP}:{PORT}',
                            Proxies         = dict(
                                http    = f'socks4://{IP}:{PORT}',
                                https   = f'socks4://{IP}:{PORT}',
                            )
                        )
                    except Error:pass

                r  = self.Session.get('https://www.proxy-list.download/SOCKS5')
                Result = BeautifulSoup(r.content, 'html5lib')
                Saves = [List for List in Result.findAll('tbody', attrs={'id': 'tabli'})[0].findAll('tr')]
                for i in range(len(Saves)):
                    Proxy = Saves[random.randint(0, len(Saves) - 1)]
                    SPLIT   = str(Proxy).split('td>')
                    IP      = SPLIT[1].replace(' ', '').replace('\n', '').replace('\r', '').split('</')[0]
                    PORT    = SPLIT[3].replace(' ', '').replace('\n', '').replace('\r', '').split('</')[0]
                    try:
                        DatabaseProxy.Proxys.SaveProxy().Set(
                            country         = '',
                            countryCode     = '',
                            IpPort          = f'{IP}:{PORT}',
                            Proxies         = dict(
                                http    = f'socks5://{IP}:{PORT}',
                                https   = f'socks5://{IP}:{PORT}',
                            )
                        )
                    except Error:pass
        
    class HideMy(Request) :
        
        def __init__(self, Search: bool) -> None:
            super().__init__(Search)
            if Search:
                URL = 'https://hidemy.name/en/proxy-list/'
                r = self.Session.get(URL, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'})
                SOUP = BeautifulSoup(r.content, 'html5lib')
                Saves = [List for List in SOUP.findAll('tbody')[0].findAll('tr')]
                for i in range(len(Saves)):
                    Proxy = Saves[random.randint(0, len(Saves) - 1)]
                    TD = str(Proxy).split('td>')
                    IP = TD[1].split('</')[0]
                    PORT = TD[3].split('</')[0]
                    TYPE = 'http' if TD[9].split('</')[0].lower() == 'https' else TD[9].split('</')[0].lower()
                    try:
                        DatabaseProxy.Proxys.SaveProxy().Set(
                            country         = '',
                            countryCode     = '',
                            IpPort          = f'{IP}:{PORT}',
                            Proxies         = dict(
                                http    = f'{TYPE}://{IP}:{PORT}',
                                https   = f'{TYPE}://{IP}:{PORT}',
                            )
                        )
                    except Error:pass
    
    class PremiumProxy(Request):
        
        def __init__(self, Search: bool) -> None:
            super().__init__(Search)
            if Search:
                self.__url__ = [
                    "https://premiumproxy.net/anonymous-proxy-list",
                    'https://premiumproxy.net/elite-proxy-list',
                    'https://premiumproxy.net/http-proxy-list',
                    'https://premiumproxy.net/https-ssl-proxy-list',
                    'https://premiumproxy.net/mikrotik-proxy-list',
                    'https://premiumproxy.net/socks-proxy-list',
                    'https://premiumproxy.net/squid-proxy-list',
                    'https://premiumproxy.net/transparent-proxy-list',
                    'https://premiumproxy.net/top-country-proxy-list'
                ]
                self.__payload__={}
                self.__headers__ = {}
                
                Proxys = list()
                for url in self.__url__:
                    response    = requests.request("GET", url, headers=self.__headers__, data=self.__payload__)
                    Result      = BeautifulSoup(response.text, features='html.parser')
                    Saves   = [List for List in Result.findAll('tbody')[0].findAll('tr', attrs={'class': 'pp1x'})]
                    for S in Saves:
                        I_P = S.findAll('td', attrs={'colspan': 1})[0].findAll('font')
                        SCHEMA = 'http' if S.findAll('td', attrs={'colspan': 1})[1].findAll('font')[0].text.lower() == 'https' else S.findAll('td', attrs={'colspan': 1})[1].findAll('font')[0].text.lower()
                        Proxys.append(dict(
                            http    = f'{SCHEMA}://{I_P[0].text}',
                            https   = f'{SCHEMA}://{I_P[0].text}',
                        ))
                    for proxy in Proxys:
                        PR = proxy.get('http')
                        if PR is None:
                            PR = proxy.get('socks4')
                            if PR is None:
                                PR = proxy.get('socks5')
                                if PR is None:
                                    PR = ''
                        try:
                            IpPort  = str(PR).split('//')[1]
                            DatabaseProxy.Proxys.SaveProxy().Set(
                                    country         = '',
                                    countryCode     = '',
                                    IpPort          = f'{IpPort}',
                                    Proxies         = proxy,
                                    BProgrammers    = False,
                                    Givvy           = False,
                                    Viker           = False,
                                    PlayFabapi      = False,
                                    Zebedee         = False
                                )
                        except Error:pass
                        except:pass

    class Get(Request):
        
        def __init__(self, Search: bool, Authorization: Optional[str] = None, *args, **kwargs) -> None:
            super().__init__(Search)
            WebShare, ProxyScrape, Geonode, FreeProxyList, ProxyList, HideMy, PremiumProxy = True, True, True, True, True, True, True
            while True:
                if Search:
                    Typer.Print(f'{Color.RED}=> {Color.WHITE}Please Wait {Color.GREEN}Scraping New Proxy', Refresh=True)
                    if Authorization is not None or Authorization != '': SearchProxy.WebShare(Search, Authorization)
                    else: WebShare = False
                    try:
                        if kwargs.get('ProxyScrape') is True or kwargs.get('ProxyScrape') is None: SearchProxy.ProxyScrape(Search)
                        else: ProxyScrape = False
                    except:pass
                    try:
                        if kwargs.get('Geonode') is True or kwargs.get('Geonode') is None:SearchProxy.Geonode(Search)
                        else: Geonode = False
                    except:pass
                    try:
                        if kwargs.get('FreeProxyList') is True or kwargs.get('FreeProxyList') is None:SearchProxy.FreeProxyList(Search)
                        else: FreeProxyList = False
                    except:pass
                    try:
                        if kwargs.get('ProxyList') is True or kwargs.get('ProxyList') is None:SearchProxy.ProxyList(Search)
                        else: ProxyList = False
                    except:pass
                    try:
                        if kwargs.get('HideMy') is True or kwargs.get('HideMy') is None:SearchProxy.HideMy(Search)
                        else: HideMy = False
                    except:pass
                    try:
                        if kwargs.get('PremiumProxy') is True or kwargs.get('PremiumProxy') is None:SearchProxy.PremiumProxy(Search)
                        else: PremiumProxy = False
                    except:pass
                
                self.ListProxy = DatabaseProxy.Proxys.SaveProxy().Get()
                if len(self.ListProxy) == 0:
                    if WebShare is True or ProxyScrape is True or Geonode is True or FreeProxyList is True or ProxyList is True or HideMy is True or PremiumProxy is True: Search = True
                    else: raise Error('No Proxy')
                else: break
