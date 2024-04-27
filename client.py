from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

baseUrl = 'http://127.0.0.1:5000'

@app.route('/', methods=['get'])
def index():
    response = requests.get(baseUrl + '/employee')
    employees = response.json()
    return render_template('index.html', employees=employees)


if __name__ == '__main__':
    app.run(debug=True, port=5003)