from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from gensim.models import Word2Vec
import numpy as np
import re


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

def clean_string(input):
    # Make sure input is a string
    input = input if type(input) is str else ''

    # Turn everything into lower case
    input = input.lower().strip()

    # Remove unwanted characters
    input = re.sub(r"[^a-z\ ]", ' ', input, 0, re.MULTILINE)

    # Remove multiple spaces
    input = re.sub(r"\ +", ' ', input, 0, re.MULTILINE)

    # Return stripped output
    input = [word for word in input.split() if word in model.vocab]
    return input

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
    text = clean_string(text)
    a = np.array([model[word] for word in text if word in model.vocab])
    b = np.average(a, axis = 0)

    returnvector = np.absolute(np.rint(b*100))
    return render_template('vectorviz.html', len_v = len(returnvector), v = repr(returnvector)[7:-17].replace('\n',''))
    

if __name__ == "__main__":
    print('loading model...')
    model_tl = Word2Vec.load("model20191210/model20191210.model") #tagalog
    print('model loaded.')
    model = model_tl.wv
    app.run(host="0.0.0.0", port=80)