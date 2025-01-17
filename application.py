from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from gensim.models import Word2Vec
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
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

# @app.route("/", methods=['GET'])
# def welcome():
#     return "Hi jenny!!!!"


@app.route("/")
def hello():
    return render_template('get_text.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    text = clean_string(text)

    #star
    input_vector = np.array([model[word] for word in text if word in model.vocab])
    input_vector = np.average(input_vector, axis = 0)
    star_vector = np.absolute(np.rint(input_vector*100))
    
    #color3
    matrix_to_pca3 = np.vstack((text1a, input_vector))
    matrix_pca3 = pca3.fit_transform(matrix_to_pca3)
    scaler = MinMaxScaler(feature_range=(0, 255)).fit(matrix_pca3)
    color_vector3 = np.rint(scaler.transform([matrix_pca3[-1]]))


    #color6
    matrix_to_pca6 = np.vstack((text2a, input_vector))
    matrix_pca6 = pca6.fit_transform(matrix_to_pca6)
    scaler = MinMaxScaler(feature_range=(0, 255)).fit(matrix_pca6)
    color_vector6 = np.rint(scaler.transform([matrix_pca6[-1]]))

    print(color_vector3)
    print(color_vector6)

    return render_template('vectorviz.html', 
                            len_v = 100, 
                            v = repr(star_vector)[7:-17].replace('\n',''), 
                            bg3 = repr(color_vector3)[8:-3].replace('\n',''),
                            bg6 = repr(color_vector6)[8:-3].replace('\n',''))
    

if __name__ == "__main__":
    print('loading model...')
    model_tl = Word2Vec.load("model20191210/model20191210.model") #tagalog
    print('model loaded.')
    model = model_tl.wv
    pca6 = PCA(n_components=6)
    pca3 = PCA(n_components=3)

    with open('textfiles/nakpilessay.txt', 'r') as f:
        text1 = f.read()
    text1 = text1.lower()
    text1 = re.sub(re.compile('[^a-z\ ]'), '', text1).split()

    with open('textfiles/ninoyessay.txt', 'r') as f:
        text2 = f.read()
    text2 = text2.lower()
    text2 = re.sub(re.compile('[^a-z\ ]'), '', text2).split()

    text1a = np.array([model[word] for word in text1 if word in model.vocab])
    text2a = np.array([model[word] for word in text2 if word in model.vocab])
    app.run(host="0.0.0.0", port=80)