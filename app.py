from flask import Flask, request, jsonify
from flask.app import _make_timedelta
from joblib import load
import numpy as np

app = Flask(__name__)

knn = load("knn.pkl")

@app.route('/')
def ping():
    print('11111')
    return 'ok', 200

@app.route('/user/<var>')
def suare(var):
    return str(int(var)*var)

def show_image(flower_class):
    flower_images = {
        0: "<img src='/static/setosa.jpg' alt='setosa'>",
        1: "<img src='/static/versicolor.jpg' alt='versicolor'>",
        2: "<img src='/static/virginica.jpg' alt='virginica'>"
    }
    return flower_images[flower_class]

@app.route('/iris/<args>')
def iris(args):
    params = [float(arg) for arg in args.split(',')]
    params = np.array(params).reshape(1,-1)
    return show_image(knn.predict(params)[0])

@app.route('/iris_post', methods=['POST'])
def iris_post():
    wtf = request.get_json()
    return jsonify(wtf)

if __name__ == '__main__':
    app.run()