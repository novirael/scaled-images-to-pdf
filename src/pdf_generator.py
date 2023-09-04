import os
from pathlib import Path
from PIL import Image
from fpdf import FPDF

from data_types import Orientation


def get_orientation(width: int, height: int) -> Orientation:
    return Orientation.LANDSCAPE.value if width > height else Orientation.PORTRAIT.value


def generate_pdf_from_path(path: Path, filename: str, scale_ratio=None) -> None:

    # Get the list of images
    image_list: list[Path] = os.listdir(path)

    # Create a PDF object
    pdf = FPDF(format='A4')

    # Iterate over the images, add new page and image on it
    for image in image_list:
        image_file: Path = os.path.join(path, image)
        image_obj = Image.open(image_file)
        w, h = image_obj.size
        orientation: Orientation = get_orientation(w, h)

        if scale_ratio:
            width = w / scale_ratio
            height = h / scale_ratio
        else:
            width = 297 if orientation == Orientation.LANDSCAPE.value else 0
            height = 210 if orientation == Orientation.PORTRAIT.value else 0

        pdf.add_page(orientation=orientation)
        pdf.image(image_file, 0, 0, width, height, keep_aspect_ratio=True)

    # Save the PDF file
    pdf.output(f"{path}/{filename}.pdf")