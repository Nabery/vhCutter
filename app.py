from flask import Flask, request, render_template
import os
import subprocess

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'mxf'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_file(input_path, output_path, start_time, duration):
    # Define the ffmpeg command to execute
    command = f'ffmpeg -y -ss {start_time} -t {duration} -i "{input_path}" -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 128k -movflags +faststart "{output_path}"'
    # Execute the ffmpeg command and wait for it to finish
    subprocess.run(command, shell=True)


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('file')
        if files:
            for file in files:
                if file and allowed_file(file.filename):
                    filename = file.filename
                    input_path = os.path.join('./Files', filename)
                    start_time = request.form['start_time']
                    duration = request.form['duration']
                    output_path = os.path.join('./Files', f'{os.path.splitext(filename)[0]}_{start_time}_{duration}.mp4')
                    file.save(input_path)
                    convert_file(input_path, output_path, start_time, duration)
            return f'{len(files)} video files uploaded and converted successfully'
        else:
            return 'No video files uploaded'
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
