import radix
import urllib.request
from datetime import date
import gzip

class FormRadixTree():
    def FetchData(self):
        ## Fetch today data

        today = date.today()
        year = today.year
        month = today.month
        day = today.day

        if month < 10:
            month = '0{}'.format(month)
        if day < 10:
            day = '0{}'.format(day)
        dateStr = '{}-{}-{}'.format(year, month, day)

        url = 'http://data1.labs.apnic.net/bgplog/{}/{}/{}/{}.dmp.gz'.format(year, month, day, dateStr)

        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        data = response.read()
        data = str(gzip.decompress(data))
        data = data.split('\\r\\n')
        header = data[0:6]
        body = data[7:]
        prefixes = []        
        print(body[0].split(' '))
        for line in body:
            tmp = line.split(' ')
            if len(tmp) < 2:
                continue
            c = ''
            if c in tmp:
                tmp.remove(c)
            tmp = tmp[1]
            if '/' in tmp:
                prefixes.append(tmp)
        
        return prefixes

    def IsVisible(self):

    def FormTree(self):

        rtree = 

    # def get(self):