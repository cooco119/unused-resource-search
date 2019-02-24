import json

class FormTable():
    def getJson(self):

        start = '2019-02-22'
        duration = 5

        # result = _replace_with_diff_method(start, duration)
        result = [{
            'prefix': 'test prefix',
            'duration': 10,
            'prefix_length': 16
        },
        {
            'prefix': 'test prefix',
            'duration': 10,
            'prefix_length': 16
        }]

        data = []

        for e in result:
            tmp = {
                'prefix': e['prefix'],
                'duration': e['duration'],
                'prefix_length': e['prefix_length']
            }
            data.append(tmp)

        result = json.dumps(data)

        return result

    def getJsonFromTree(self, rtree):

        result = []
        for node in rtree:
            if node.data['visibility'] != True :
                tmp = {
                    "prefix": node.prefix,
                    "last_seen": node.data['last_seen'],
                    "prefixlen": node.prefixlen 
                }
                result.append(tmp)

        result = json.dumps(result)

        return result