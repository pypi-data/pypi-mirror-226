# BackTrack 
# GhostWeb IDE
# VS Code

from colorama import Fore as f, init
from colorama import Fore


print(f'{f.WHITE}Please Wait ... {f.CYAN} ->  {f.LIGHTYELLOW_EX}BackTrack\n\n{f.WHITE}Perparing to {f.RED}Setup{f.WHITE} Libray\n\n')

import os  
import socket 
import pyfiglet
import time 
import requests
from fuzzywuzzy import fuzz
from googlesearch import search
from bs4 import BeautifulSoup
import sys

class CryptoX:
    global key
    key = 'FzgnTlMaMgRMWz4ANExbPmBwGQ4='
    def __init__(self, PassWord : str):
        self.password = str(PassWord)
        self.headers = {'Content-Type': 'Application/json', 'Accept': 'Application/json'}
   
    def createBanner(self, text : str):
        if self.password == key:
            return str(pyfiglet.figlet_format(text=text))
        else:return 'password error'

    def createBannerWithFont(self, text : str = None , font : str = None):
        if self.password == key:
            if text == None or font == None:
                return "text or font is empty"
            else:
                return str(pyfiglet.figlet_format(text=text, font=font))
        else:return "password error"

    def getHostIP(self, domain : str = None):
        if self.password == key:
            if domain == None:
                return "domain is empty"
            else:
                return socket.gethostbyname(domain)
        else:return "password error"


    def Hour(self):
        if self.password == key:
            return time.strftime("%H")
        else:return "password error"


    def Min(self):
        if self.password == key:
            return time.strftime("%M")
        else:return "password error"

    def Sec(self):
        if self.password == key:
            return time.strftime("%S")
        else:return "password error"


    def sendRequestTelegram(self, token : str = None, chatID : str = None, message : str = None):
        if self.password == key:
            if token == None or chatID == None or message == None:
                return "token or chatID or message is empty"
            else:
                url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chatID}&text={message}"
                req = requests.post(url)
                return req

        else:return "password error"


    def sendRequestTelegramWithPayload(self, token : str = None, chatID : str = None, message : str = None):
        if self.password == key:
            if token == None or chatID == None or message == None:
                return "token or chatID or message is empty"
            else:
                url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chatID}&text={message}"
                mypay = {
                    "UrlBox" : url,
                    "AgentList" : "Google Chrome",
                    "VersionList" : "HTTP/1.1",
                    "MethodList" : "POST"
                }
                req = requests.post("https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx", data=mypay)
                return req

        else:return "password error"

    def sendRequest(self, url: str = None, data = None):
        if self.password == key:
            if url == None:
                return "url is empty"
            else:
                req = requests.post(url, data=data if not data == None else '' or None)
                return req
        else:return "password error"

    def sendRequestWithPayload(self, url : str = None):
        if self.password == key:
            if url == None:
                return "url is empty"
            else:
                mypay = {
                    "UrlBox" : url,
                    "AgentList" : "Google Chrome",
                    "VersionList" : "HTTP/1.1",
                    "MethodList" : "POST"
                }
                req = requests.post("https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx", data=mypay)
                return req
        else:return "password error"

    def getTextUrl(self, url : str, Type : str):
        if self.password == key:
            if Type == 'post':
                return requests.post(url).text
            elif Type == 'get':
                return requests.get(url=url).text
            else:return 'Type error'
        else:return 'password error'
        
    def getDataWithJsonApplocation(self, url : str = None, Type : str = None):
        if self.password == key:
            if (url == None or Type == None):
                raise ValueError("'url' parameter cannot be empty\n'Type' parameter cannot be empty")
            else:
                if Type == 'post' or Type == "POST":
                    return requests.post(url=url, headers=self.headers)
                elif Type == "get" or Type == "GET":
                    return requests.get(url=url, headers=self.headers)
                else:raise ValueError(f"the 'Type' parameter should be [ get / GET || post / POST ]\ncannot be this : {Type}")
        else:raise ValueError('password error')

    def changeDir(self, path : str):
        if self.password == key:
            os.chdir(path=path)
            
        else:return 'password error'
    
    @property
    def sysName(self):
        if self.password == key:
            import os

            for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
                user = os.environ.get(name)
                if user:
                    return user
                
            import pwd
            return pwd.getpwuid(os.getuid())[0]
        else:return 'password error'
        
    def unzipLinux(self, fileName : str, downloadPackage = False):
        if self.password == key:
            if downloadPackage == False:
                os.system(f"unzip {fileName}")
            elif downloadPackage == True:
                os.system('pkg install zip')
                os.system(f'unzip {fileName}')
                
            else:return 'downloadPackage must be True or False'
            
        else:return 'password error'
        
    def readFile(self, fileName : str):
        if self.password == key:
            try:
                File = open(fileName, 'r').read()
                return File
            except:return 'error in openning file'
        else:return 'password error'
        
    def writeFile(self, fileName : str, message : str):
        if self.password == key:
            try:
                with open(fileName, 'a') as myFile:
                    myFile.write(str(message))
                    myFile.close()
            except:return 'error in openning file'
        else:return 'password error'    
        
    def osint(self, query : str):

        if self.password == key:

            # colorama
            init(autoreset=True)

            for url in search(query):
                print('\n' + Fore.CYAN + '[+] Url detected: ' + url)
                try:
                    text = requests.get(url, timeout = 1).text
                except:
                    continue
                soup = BeautifulSoup(text, "html.parser")
                links_detected = []
                try:
                    print(Fore.MAGENTA + '[?] Title: ' + soup.title.text.replace('\n', ''))
                except:
                    print(Fore.RED + '[?] Title: null')
                # Find by <a> tags
                try:
                    for link in soup.findAll('a'):
                        href = link['href']
                        if not href in links_detected:
                            if href.startswith('http'):
                                # Filter
                                if url.split('/')[2] in href:
                                    links_detected.append(href)
                                # If requested data found in url
                                elif query.lower() in href.lower():
                                    print(Fore.GREEN + '--- Requested data found at link : ' + href)
                                    links_detected.append(href)
                                # If text in link and link location is similar
                                elif fuzz.ratio(link.text, href) >= 60:
                                    print(Fore.GREEN + '--- Text and link are similar : ' + href)
                                    links_detected.append(href)

                except:
                    continue
                if links_detected == []:
                    print(Fore.RED + '--- No data found')



        else:return 'password error'
        
                
    def checkImport(libName : list, filePath : str = None):
        if filePath == None:
            raise ValueError("the 'filePath' Parametr cannot be empty")
        else:
            try:
                data = open(file=filePath, mode='r').read()
                for libs in list(libName):
                    if libs in data:
                        print(f"{libs} : True")
                    else:print(f"{libs} : False")
            except Exception as error:
                print(error)
                    
                    
