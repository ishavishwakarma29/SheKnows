import flask
from werkzeug.utils import secure_filename
import os
import numpy as np
from PIL import Image
import pickle

app = flask.Flask(__name__, template_folder='./templates', static_folder='./static')

app.config['UPLOAD_FOLDER'] = './uploads/' 
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
model = pickle.load(open("G:/SheKnows/SheKnows/models/breast.sav", "rb"))


@app.route('/', methods=['GET', 'POST']) 
def index(): 
    if flask.request.method == 'POST':
        file = flask.request.files['image']
        
        if file.filename == '':
            return "No selected file"

        if file:
           filename = secure_filename(file.filename)
           filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
           file.save(filepath)
           prediction = make_prediction(filepath)
           if prediction==1:
               return flask.redirect('positive')
           else :
               return flask.redirect('negative')
               

    return flask.render_template('index.html') 
 
@app.route('/positive', methods=['GET', 'POST']) 
def rspos(): 
    return flask.render_template('positive.html')

@app.route('/negative', methods=['GET', 'POST']) 
def rsneg(): 
    return flask.render_template('negative.html')


def make_prediction(image_path):
    img_array = preprocess_image(image_path, target_size=(50, 50))
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)[0]
    return int(predicted_class)

def preprocess_image(image_path, target_size=(50, 50)):
    img = Image.open(image_path)
    img = img.resize(target_size)
    img_array = np.array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

if __name__ == '__main__': 
    app.run(debug=True) 