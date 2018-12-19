from flask import request, redirect, url_for, render_template, send_from_directory, send_file, flash
import time
import os
from werkzeug.utils import secure_filename
from marimba import app, allowed_file
import subprocess
from tempfile import NamedTemporaryFile, TemporaryFile, mkstemp
from marimba.image_creator import ImageGenerator

@app.route("/")
def hello():
    return render_template('main.html')


@app.route('/upload')
def load_upload():
    return render_template('main.html')
    
    
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        f = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if f and allowed_file(f.filename):
            try:
                pre, ext = os.path.splitext(f.filename)
                time_stamp = str(int(time.time()))
                filename = secure_filename(pre + time_stamp + ext)
                if not os.path.isdir(app.config['UPLOAD_FOLDER']): 
                    os.mkdir(app.config['UPLOAD_FOLDER'])
                fd, tmp_path = mkstemp()
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                f.save(upload_path)
          
                if request.form["file_type"] == 'image':
                    ig = ImageGenerator(upload_path, app.config['UPLOAD_FOLDER'])
                    ig.create_wave()
                    time_stamp = str(int(time.time()))
                    wav_path = f'waveform{time_stamp}.png'
                    ig.write_plot(wav_path)
                    ig.create_spectrogram()
                    spectro_path = f'spectrogram{time_stamp}.png'
                    ig.write_plot(spectro_path)
                    return render_template('main.html', waveform_path=wav_path, spectrogram_path=spectro_path)

                elif request.form["file_type"] == 'midi':
                    # subprocess.run(['/Users/pinea/WaoN/waon', '--cutoff', '-6.0', '-i', f'{upload_path}', '-o', f"{tmp_path}"])
                    subprocess.run(['/WaoN/waon', '--cutoff', '-6.0', '-i', f'{upload_path}', '-o', f"{tmp_path}"])
                    return send_file(tmp_path,
                                    as_attachment=True,
                                    mimetype='application/x-midi',
                                    attachment_filename='output.mid')
                
            finally:
                os.remove(tmp_path)
                os.remove(upload_path)
    return '''
    <p>
Sorry, your file couldn't be uploaded or converted. Are you sure it was a .wav file?
</p>
    '''

@app.route('/uploads/<filename>')
def send_img_file(filename):
    filename = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print(f"sending file {filename}")
    return send_file(filename,
                    mimetype='image/png')
    # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
