# -*- coding: utf-8 -*- 
"""
Project: Vue_project
Creator: Administrator
Create time: 2020-04-20 12:01
IDE: PyCharm
Introduction:
"""
from flask import Flask, render_template, jsonify, request, session,  make_response
from flask_cors import CORS
import random
import requests
import os
import logging
from flask_caching import Cache
import json
from datetime import timedelta

CACHE_CONFIG = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory',
    'CACHE_THRESHOLD': 200  # should be equal to maximum number of active users
}

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
cors = CORS(app, supports_credentials=False, resources={r"/api/*": {"origins": "*"}})
# 设置上传文件路径
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
app.secret_key = "LizzieDeng"
app.permanent_session_lifetime = timedelta(minutes=1)
# 创建缓存
cache = Cache()
cache.init_app(app, config=CACHE_CONFIG)

# log文件
logging.basicConfig(level=logging.DEBUG, filename='log/log.txt', filemode='w',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


randNumber = 90
@app.route('/api/getdata', methods=['GET', 'POST'])
def getdata():
    if request.method == 'POST':
        try:
            data = request.get_data()
            session.permanent = True
            data1 = json.loads(data.decode('utf-8'))
            print("request.cookies.get", request.cookies)
            uuid_1 = data1.get('uuid')
            if uuid_1:
                if session.get("uuid") == uuid_1:
                    data = generate_data()
                    success = True
                    message = "successfully"
                else:
                    session["uuid"] = uuid_1
                    data = generate_data()
                    success = True
                    message = "successfully"
            else:
                print('else', uuid_1)
                # logging.DEBUG('at getdata function, uuid failed')
                success = False
                data = {}
                message = 'uuid 为空'
        except Exception as e:
            logging.DEBUG('at getdata function, save file failed, exception {0}'.format(e))
            success = False
            data = None
            message = e
        return jsonify({'success': success, 'data': data, 'message': message})


def generate_data():
    x = [random.randint(1000, 3000) for i in range(randNumber)]
    y = [random.randint(3000, 8000) for i in range(randNumber)]
    z = [random.randint(0, 5000) for i in range(randNumber)]
    data = {'x': x, 'y': y, 'z': z}
    return data


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print("catch_all")
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
