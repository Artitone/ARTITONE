from io import BytesIO
import os

from PIL import Image as PilImage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.uploadedfile import TemporaryUploadedFile


def resize_image(image, height, width=None):
    max_height = height
    with PilImage.open(image.file).convert("RGB") as im:
        if im.size[1] < max_height:
            return
        hpercent = max_height / float(im.size[1])
        if not width:
            max_width = int((float(im.size[0]) * float(hpercent)))
        else:
            max_width = width
    size = (max_width, max_height)

    # Uploaded file is in memory
    if isinstance(image, InMemoryUploadedFile):
        pil_image = PilImage.open(image.file)
        img_format = os.path.splitext(image.name)[1][1:].upper()
        img_format = "JPEG" if img_format == "JPG" else img_format

        if pil_image.width > max_width or pil_image.height > max_height:
            pil_image.thumbnail(size)

        new_image = BytesIO()
        pil_image.save(new_image, format=img_format)

        new_image = ContentFile(new_image.getvalue())
        return InMemoryUploadedFile(new_image, None, image.name, image.content_type, None, None)

    # Uploaded file is in disk
    elif isinstance(image, TemporaryUploadedFile):
        path = image.temporary_file_path()
        pil_image = PilImage.open(path)

        if pil_image.width > max_width or pil_image.height > max_height:
            pil_image.thumbnail(size)
            pil_image.save(path)
            image.size = os.stat(path).st_size

    return image
