import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # Show files to the client
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            return redirect(url_for('admin'))
    
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('admin.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    # as_attachment=True ensures the browser downloads the file instead of trying to open it
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/delete/<filename>')
def delete_file(filename):
    os.remove(os.path.join(UPLOAD_FOLDER, filename))
    return redirect(url_for('admin'))

if __name__ == '__main__':
    # host='0.0.0.0' allows other devices on your Wi-Fi to connect
    app.run(host='0.0.0.0', port=5000, debug=True)