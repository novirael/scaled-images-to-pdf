import os
from flask import Flask, render_template, request, send_file
from fpdf import FPDF
from PIL import Image
from uuid import uuid4
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def get_orientation(width, height):
    return "landscape" if width > height else "portrait"


def generate_pdf_from_path(path):
    # Get the list of images
    image_list = os.listdir(path)

    # Create a PDF object
    pdf = FPDF(format='A4')

    scale_ratio = 11.6

    # Iterate over the images
    for image in image_list:
        image_file = os.path.join(path, image)

        image_obj = Image.open(image_file)
        w, h = image_obj.size
        orientation = get_orientation(w, h)

        pdf.add_page(orientation=orientation)
        pdf.image(image_file, 0, 0, w / scale_ratio, h / scale_ratio, keep_aspect_ratio=True)

    # Save the PDF file
    pdf.output(f"{path}/output.pdf")


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, f"images/{uuid4()}")

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)

    generate_pdf_from_path(target)

    return send_file(f"{target}/output.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
