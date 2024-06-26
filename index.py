# 2024/5/3
import os

import requests
from flask import Flask, request, Response

app = Flask(__name__)

if not os.environ.get('host'):
    os.environ.setdefault('host', 'http://flask-web.351529.xyz')
host = os.environ["host"]


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'HEAD', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'HEAD', 'DELETE'])
def proxy(path):
    if not host:
        return '请先设置 host'

    url = f'{host}/{path}'  # 替换为目标地址
    print(url)
    headers = dict(request.headers)
    headers.pop('Host')
    # headers.pop('content-disposition')
    params = dict(request.args)
    method = request.method

    if method == 'GET':
        response = requests.get(url, headers=headers, params=params)
        if len(response.text) < 200:
            print(response.text)
    elif method == 'POST':
        response = requests.post(url, headers=headers, params=params, data=request.data)
    elif method == 'HEAD':
        response = requests.head(url, headers=headers, params=params)
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers, params=params)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, params=params, data=request.data)

    if 'Content-Disposition' in response.headers:
        response.headers.pop('Content-Disposition')
    # print(response.headers)
    response = Response(response.content, status=response.status_code, headers=dict(response.headers.items()))
    return response


if __name__ == '__main__':
    app.run(debug=False)
