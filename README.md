# scaled_images_to_pdf

This is simple online app for generating pdf from multiple images.

It allows you to scale your images to fit ar any provided ratio. You can also read it from query params eg. http://127.0.0.1:8000/?scale=11.6

## Demo

![Scaled images to PDF screen](/demo.png)

## Development

Use poetry for keeping python dependency isolated.
```
poetry shell
poetry install
python ./src/app.py
```
