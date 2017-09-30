#!flask/bin/python
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

UPLOAD_DIRECTORY = '/ShellHacks/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

def allowed_file(filename):
    return '.' in filename and filename.rsplit(
		'.', 1)[1].lower() in ALLOWED_EXTENSIONS

def uploadPicture(picture, is_known=True):
    if is_known is True:
        UPLOAD_DIRECTORY += 'known'
    else:
        UPLOAD_DIRECTORY += 'unknown'

    app.config['UPLOAD_DIRECTORY'] = UPLOAD_DIRECTORY
    
    filename = secure_filename(picture.filename)
    picture.save(os.path.join(app.config['UPLOAD_DIRECTORY'], filename))
    return redirect(url_for('uploaded_file', filename = filename))

@app.route('/unknown_upload', methods=['POST'])
def unknown_upload():
    if 'file' not in request.files:
        flash('No file uploaded')
        return redirect(request.url)
    file = request.files['file']
    
    if file.filename == '':
        flash('No file uploaded')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        return uploadPicture(file, False)

if __name__ == '__main__':
    app.run(debug=True)

