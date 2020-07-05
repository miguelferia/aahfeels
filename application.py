from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from gensim.models import Word2Vec
import numpy as np

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])

@app.route("/", methods=['GET'])
def welcome():
    return "Hi jenny!!!!"

@app.route("/vector", methods=['GET'])
def vector():
    word = request.args.get("word")
    return str(model[word])

@app.route("/radii", methods=['GET'])
def radii():
    word = request.args.get("word")
    vec = model[word]
    return str(np.rint(vec*100))

@app.route("/page")
def page():
    return render_template('index.html')

@app.route("/form")
def hello():
    return render_template('get_text.html')

@app.route('/form', methods=['POST'])
def my_form_post():
    text = request.form['text']
    vec = model[str(text)]
    returnvector = np.absolute(np.rint(vec*100))
    return render_template('vectorviz.html', len_v = len(vec), v = repr(returnvector)[7:-17].replace('\n',''))
    

if __name__ == "__main__":
    print('loading model...')
    model_tl = Word2Vec.load("model20191210/model20191210.model") #tagalog
    print('model loaded.')
    model = model_tl.wv
    app.run(host="0.0.0.0", port=80)