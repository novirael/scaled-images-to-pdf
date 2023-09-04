import os
import time
from pathlib import Path
from typing import Optional
from flask import Flask, Response, render_template, send_file, request
from uuid import uuid4
from pdf_generator import generate_pdf_from_path


app = Flask(__name__)
APP_ROOT: Path = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index() -> Response:
    return render_template("upload.html")


@app.route("/upload", methods=['POST'])
def upload() -> Response:

    # Get the scale ratio from form
    try:
        scale_ratio: float = float(request.form.get('scale', '').replace(',', '.'))
    except (TypeError, ValueError):
        scale_ratio = None

    # Get the file from form
    target: Path = os.path.join(APP_ROOT, f"images/{uuid4()}")
    if not os.path.isdir(target):
        os.makedirs(target)

    for file in request.files.getlist("file"):
        filename: Optional[str] = file.filename
        if filename:
            destination: Path = "/".join([target, filename])
            file.save(destination)
        else:
            message = "Have you uploaded the image ? Reload the page and try again"
            return render_template('error.html', error_message=message)

    filename = time.strftime("%Y%m%d-%H%M%S")
    generate_pdf_from_path(target, filename, scale_ratio)
    return send_file(f"{target}/{filename}.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port="8000", debug=True)
