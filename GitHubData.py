import json
import datetime
import urllib.request as urllib2
import socks
import time
from SocksProxy import SocksiPyHandler

class GitHubData:

    def __init__(self, proxy_hostname, proxy_port):
        self._proxy_hostname = proxy_hostname
        self._proxy_port = proxy_port
        self.initConnection()

    def initConnection(self):
        self._connection = urllib2.build_opener(SocksiPyHandler(socks.PROXY_TYPE_SOCKS5, self._proxy_hostname, self._proxy_port))

    def getGitHubDataTry(self, request):
        response = self._connection.open(fullurl='https://api.github.com' + request)
        headers = response.getheaders()
        body = response.read().decode()

        status = [item[1] for item in headers if item[0] == 'Status']

        if len(status) == 0 or status[0] == '403 Forbidden':
            print(headers)
            print(body)
            print(request)
            rate_limit_reset_time = int([item[1] for item in headers if item[0] == 'X-RateLimit-Reset'][0])
            print(datetime.datetime.utcfromtimestamp(rate_limit_reset_time))
            raise BaseException('403 Forbidden')

        if len(status) == 0 or not status[0] == '200 OK':
            print(headers)
            print(body)
            print(request)
            raise 'Bad Header Status'

        try:
            return json.loads(s=body)
        except:
            print(headers)
            print(body)
            print(request)
            raise 'Cant parse json'


    def getGitHubData(self, request):
        tries = 30
        while tries > 0:
            try:
                return self.getGitHubDataTry(request)
            except:
                tries -= 1
                time.sleep(10)
                print('Try refetch data {}'.format(request))
                self.initConnection()

        raise BaseException('Cant fetch data')

