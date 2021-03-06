import os
from os.path import join, dirname, realpath
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from static.py.generate_calendar import create_calendar

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/image/uploads/')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/landing.html', methods=['GET', 'POST'])
def create_calendar_schedule():
    if request.method == 'POST':
        term = request.form['term']
        year = int(request.form['year'])
        if request.files:
            image = request.files["scheduleFile"]

            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            create_calendar(term, year, os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('landing.html')

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
