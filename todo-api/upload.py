import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import face_recognition
import time


UPLOAD_FOLDER1 = './known'
UPLOAD_FOLDER2 = './unknown'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/user_form_submit', methods=['GET', 'POST'])
def submit_form(user_name, email, missing_person_name, missing_person_pic):
    return upload_file1(missing_person_name, missing_person_pic)

def upload_file1(missing_person_name, missing_person_pic):
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER1

    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        os.rename(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['UPLOAD_FOLDER'], "%s-%s.jpeg" % (missing_person_name, str(time.time()))))
        return 'SUCCESS'

@app.route('/api/user_upload', methods=['GET', 'POST'])
def upload_file1():
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER1
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'SUCCESS'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/api/admin_upload', methods=['GET', 'POST'])
def upload_file2():
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER2
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return match_found(filename)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

def match_found(picture):
    unknown_picture = face_recognition.load_image_file(picture)
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

    for picture in os.listdir(UPLOAD_FOLDER1):
        known_picture = face_recognition.load_image_file(picture)
        known_face_encoding = face_recognition.face_encodings(known_picture)[0]

        # Now we can see the two face encodings are of the same person with `compare_faces`!
        is_match = face_recognition.compare_faces([unknown_face_encoding], known_face_encoding)

        if is_match[0] == True:
            os.remove('%s/%s' % (UPLOAD_FOLDER1, picture))
            return 'Missing Person Name: %s' % (picture)

    return 'No facial recognition matches yet.'

#
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)


if __name__ == "__main__":
    app.run()