from flask import Flask, jsonify
import requests, json
import xml.etree.ElementTree as ET
from datetime import date

app = Flask(__name__)  

@app.route('/currency')
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