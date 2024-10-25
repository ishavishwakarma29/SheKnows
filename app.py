import flask
from werkzeug.utils import secure_filename
import os
# start flask
app = flask.Flask(__name__, template_folder='./templates', static_folder='./static')

app.config['UPLOAD_FOLDER'] = 'uploads/'  # Define a folder to save uploaded files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit upload size to 16MB

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# render default webpage
@app.route('/', methods=['GET', 'POST']) 
def index(): 
    if flask.request.method == 'POST':
        if 'image' not in flask.request.files:
            return "No file part in the request"
        
        file = flask.request.files['image']
        
        if file.filename == '':
            return "No selected file"
        
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f"Image {filename} uploaded successfully!"

    return flask.render_template('index.html') 
 
if __name__ == '__main__': 
    app.run(debug=True) 