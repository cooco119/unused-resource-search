from flask import Flask, request, render_template

from FormRadixTree import FormRadixTree
from FormTable import FormTable

app = Flask(__name__)

@app.route('/static/<path:path>', endpoint='serveStatic')
def serveStatic(path):
    print(path)
    return url_for('static', filename=path)

@app.route('/api/v1/unused', endpoint='UnusedResources') 
def UnusedResources():
    rtree = FormRadixTree().get()
    # response = FormTable().getJson()
    response = FormTable().getJsonFromTree()

    return response

@app.route('/')
def Root(): 
    return render_template('index.html', name=None)
