import os

from flask import Flask, request, jsonify, abort, render_template, send_file
from flask.helpers import url_for
# from flask.templating import render_template
from werkzeug.utils import redirect
from joblib import load
import numpy as np
from flask_wtf import FlaskForm
from wtforms import StringField
from flask_wtf.file import FileField

import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = "asdfasdasdsds"


knn = load("knn.pkl")

@app.route('/ping')
def ping():
    return 'pong', 200

@app.route('/badrequest400')
def bad_request():
    return abort(400)

def show_image(flower_class):
    flower_images = {
        0: "setosa",
        1: "versicolor",
        2: "virginica"
    }
    return flower_images[flower_class]

@app.route('/iris/<args>')
def iris(args):
    try:
        params = [float(arg) for arg in args.split(',')]
    except:
        return redirect(url_for('bad_request'))
    params = np.array(params).reshape(1,-1)
    return jsonify({
        "class": str(knn.predict(params)[0])
        })

@app.route('/iris_post', methods=['POST'])
def iris_post():
    """
    POST query example:

    curl -d '{
        "sepal_length":"1", 
        "sepal_width":"2", 
        "petal_length": "3", 
        "petal_width": "4"
        }' -H "Content-Type: application/json" -X POST http://ec2-18-221-245-142.us-east-2.compute.amazonaws.com/iris_post
    
    For more information: https://gist.github.com/subfuzion/08c5d85437d5d4f00e58
    """
    data = request.get_json()
    param_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    try:
        params = [float(data[param]) for param in param_names]
    except:
        return redirect(url_for('bad_request'))
    params = np.array(params).reshape(1,-1)
    return jsonify({
        "class": str(knn.predict(params)[0])
    })

class UsernameForm(FlaskForm):
    sepal_length = StringField()
    sepal_width = StringField()
    petal_length = StringField()
    petal_width = StringField()
    fileobject = FileField()



@app.route('/submit', methods=['GET', 'POST'])
def login_form():
    form = UsernameForm()
    style = "style=width:100px;height:100px;"
    if request.method == 'POST' and form.validate():
        try:
            f = form.fileobject.data
            df = pd.read_csv(f, header=None)
            answer = pd.DataFrame(knn.predict(df))
            answer.to_csv('predictions.csv', index=False, header=['class'])
            return send_file('predictions.csv', './')
        except:
            params = [form.sepal_length.data,
            form.sepal_width.data,
            form.petal_length.data,
            form.petal_width.data]
            params = [float(param) for param in params]
            params = np.array(params).reshape(1, -1)
            flower_class = knn.predict(params)[0]
            form.sepal_length.data = ''
            form.sepal_width.data = ''
            form.petal_length.data = ''
            form.petal_width.data = ''
            image = show_image(flower_class)
            return render_template('index.html', form=form, image=image, style=style)
    else:
        return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run()
