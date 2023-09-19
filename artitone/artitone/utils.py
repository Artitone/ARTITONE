import io

from PIL import Image


def resize_image(image, height, width=None):
    base_height = height
    with Image.open(image.file).convert("RGB") as im:
        if im.size[1] < base_height:
            return image
        hpercent = base_height / float(im.size[1])
        if not width:
            width = int((float(im.size[0]) * float(hpercent)))
        im = im.resize((width, base_height))
        img_byte_arr = io.BytesIO()
        im.save(img_byte_arr, format="JPEG")
        image.file = img_byte_arr
    return image
