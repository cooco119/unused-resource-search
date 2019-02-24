import radix
import urllib.request
from datetime import date, timedelta
import gzip
import json
import pickle

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
        print("Fetched {} numbers of prefixes, proccessing start".format(len(prefixes)))
        
        return prefixes

    def IsVisible(self, prefix):
        MAX_TIMEDIFF_THRESHOLD_DECIDE_VISIBLE = timedelta(days=1)

        try:
            ripeUrl = 'https://stat.ripe.net/data/routing-status/data.json?resource={}'.format(prefix)
            req = urllib.request.Request(ripeUrl)
            response = urllib.request.urlopen(req)
            data = json.loads(response.read())
            lastSeen = data['data']['last_seen']['time']
            [ year, month, day ] = lastSeen.split('-')
            day = day.split('T')[0] 
            lastSeenDate = date(int(year), int(month), int(day))
            today = date.today()

            diff = today - lastSeenDate
        except Exception as e:
            print(e)
            raise Exception('Error while handling visibility check')

        if (diff <= MAX_TIMEDIFF_THRESHOLD_DECIDE_VISIBLE):
            return {'visibility': True, 'last_seen': lastSeenDate}

        return {'visibility': False, 'last_seen': lastSeenDate}


    def FormTree(self, prefixes):
        filePath = './data/' + str(date.today())

        rtree = radix.Radix()
        i = 0
        for prefix in prefixes[:1000]:
            i += 1
            rnode = rtree.add(prefix)
            rnode.data['visibility'] = None
            rnode.data['last_seen'] = None
            rnodeParent = rtree.search_worst(prefix)
            if (rnodeParent.data['visibility'] == False):
                rnode.data['visibility'] = False
                print("Handling {}th prefix, Parent is already not visible".format(i))
            else:
                visibility = self.IsVisible(prefix)
                rnode.data['visibility'] = visibility['visibility']
                rnode.data['last_seen'] = visibility['last_seen']
                print("Handling {}th prefix, visibility: {}, last seen: {}".format(i, visibility['visibility'], visibility['last_seen']))
            if (i % 100 == 0):
                print("Processed " + str(i) + " prefixes, saving intermediate data.")
                f = open(filePath, 'wb+')
                pickle.dump(rtree, f)
                f.close()
        print("Processed " + str(i) + " prefixes, saving intermediate data.")
        

        return rtree

    def get(self):
        prefixes = self.FetchData()
        rtree = self.FormTree(prefixes)

        return rtree