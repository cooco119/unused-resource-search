from flask import Flask, request

from FormRadixTree import FormRadixTree
from FormTable import FormTable

app = Flask(__name__, static_url_path='./static')

@app.route('/', methods=['GET'])
def Root(): # TODO: Serve statics
    app.send_static_file('index.html')
    app.send_static_file('index.js')
    
    return


@app.route('/api/v1/unused') #TODO: handle GET method with queryString parameter 'duration'
def UnusedResources():
    rtree = FormRadixTree().get()
    response = FormTable.getJson(rtree)

    return response
