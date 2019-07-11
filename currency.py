from flask import Flask, jsonify
import requests, json
import xml.etree.ElementTree as ET
from datetime import date
from flask.ext.cache import Cache

app = Flask(__name__)  

cache = Cache(app, config={
    'CACHE_TYPE': 'memcached',
    'CACHE_MEMCACHED_SERVERS': ['127.0.0.1:11212'],
    'CACHE_DEFAULT_TIMEOUT': 0
})

@app.route('/currency')
@cache.cached(timeout=15 * 60)
def currency():
    root = getResp()

    if root:
        liste = list()
        
        for i in root[1]:
            cur = {
                 'key': i.attrib['Code'], 
                 'value': i[2].text
            }
            liste.append(cur)
        
        return jsonify(liste)
    else:
        return 'Bad Request'

@app.route('/currency/<string:id>')
@cache.cached(timeout=15 * 60)
def oneCurrency(id):

    root = getResp()

    if root:
        for i in root[1]:
            if i.attrib['Code'] == id.upper():
                dictionary = {
                    'key': id,
                    'value': i[2].text
                }
                return jsonify(dictionary)

        return 'Currency not found'
    else:
        return 'Bad request'

def getResp():
    today = date.today()
    day = today.strftime("%d.%m.%Y")
    url = f"https://www.cbar.az/currencies/{day}.xml"

    result = requests.get(url)

    if result.status_code == 200:
        root = ET.fromstring(result.text)

        return root

    return False

if __name__ == "__main__":
    app.run(debug=True)