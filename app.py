from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Add the new home route here
@app.route('/')
def index():
    return render_template('index.html')

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')  # your upload form

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('file')
    num_labels = int(request.form.get('num_labels', 8))

    image_urls = []

    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            ext = os.path.splitext(filename)[1].lower()
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Convert TIFF to PNG if needed
            if ext in ['.tif', '.tiff']:
                img = Image.open(filepath)
                filename = os.path.splitext(filename)[0] + '.png'
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                img.save(filepath, 'PNG')

            image_urls.append(os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\', '/'))

    # Now render your annotation page
    return render_template('display_multiple.html', image_urls=image_urls, num_labels=num_labels)



