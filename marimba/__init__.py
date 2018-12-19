from flask import Flask

app = Flask(__name__)

VERSION = '0.1'
UPLOAD_FOLDER = 'tmp'
ALLOWED_EXTENSIONS = set(['wav'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 0.25 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

import marimba.views