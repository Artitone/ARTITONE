import logging

import cv2 as cv
import numpy as np
from sklearn.cluster import KMeans

# from rembg import remove


logger = logging.getLogger(__name__)


def rgb2hex(rgb):
    return "#%02x%02x%02x" % rgb


def hex2rgb(hex):
    hex = hex.lstrip("#")
    lv = len(hex)
    return np.array([int(hex[i : i + lv // 3], 16) for i in range(0, lv, lv // 3)])


NUM_CLUSTERS = 5
COLOR_PALETTE = [
    hex2rgb("#ffffff"),
    hex2rgb("#d9d9d9"),
    hex2rgb("#0d0907"),
    hex2rgb("#faefe3"),
    hex2rgb("#cfb299"),
    hex2rgb("#593d2d"),
    hex2rgb("#a69f7b"),
    hex2rgb("#535925"),
    hex2rgb("#bf923f"),
    hex2rgb("#b05717"),
    hex2rgb("#91b0cc"),
    hex2rgb("#5a6473"),
]

MODERN = [
    hex2rgb("#ffffff"),
    hex2rgb("#faefe3"),
    hex2rgb("#cfb299"),
    hex2rgb("#593d2d"),
]

SCANDINAVIAN = [
    hex2rgb("#ffffff"),
    hex2rgb("#d9d9d9"),
    hex2rgb("#cfb299"),
    hex2rgb("#0d0907"),
]

MINIMALIST = [
    hex2rgb("#faefe3"),
    hex2rgb("#cfb299"),
    hex2rgb("#b05717"),
    hex2rgb("#593d2d"),
]

BOHEMIAN = [
    hex2rgb("#cfb299"),
    hex2rgb("#b05717"),
    hex2rgb("#535925"),
    hex2rgb("#5a6473"),
]

INDUSTRIAL = [
    hex2rgb("#ffffff"),
    hex2rgb("#faefe3"),
    hex2rgb("#5a6473"),
    hex2rgb("#0d0907"),
]

CONTEMPORARY = [
    hex2rgb("#d9d9d9"),
    hex2rgb("#a69f7b"),
    hex2rgb("#535925"),
    hex2rgb("#0d0907"),
]

RUSTIC = [
    hex2rgb("#d9d9d9"),
    hex2rgb("#91b0cc"),
    hex2rgb("#593d2d"),
    hex2rgb("#0d0907"),
]


def _get_dominant_color(image_file):
    """
    Take a file object and return the colour in hex code
    """
    im = np.asarray(bytearray(image_file.file.getvalue()), dtype="uint8")
    im = cv.imdecode(im, cv.IMREAD_COLOR)

    im = cv.cvtColor(im, cv.COLOR_BGR2RGB)
    im = cv.resize(im, (150, 150), interpolation=cv.INTER_AREA)  # optional, to reduce time

    clt = KMeans(n_clusters=5)
    clt = clt.fit(im.reshape(-1, 3))
    colors = []
    for pallate in clt.cluster_centers_:
        colors.append(list(pallate))
    colors = find_closet_colors(colors)
    colors = list(dict.fromkeys(colors))
    colors = [rgb2hex(tuple(color)) for color in colors]
    return colors


def find_closet_colors(colors):
    closest_palatte = []
    for c in colors:
        color = np.array([c[0], c[1], c[2]])
        distances = np.sqrt(np.sum((COLOR_PALETTE - color) ** 2, axis=1))
        index_of_smallest = np.where(distances == np.amin(distances))
        closest_palatte.append(tuple(COLOR_PALETTE[int(index_of_smallest[0])]))
    return closest_palatte


def filter_by_color_pallate(pallate_name, artworks):
    if pallate_name == "modern":
        artworks = _filter_by_pallate(MODERN, artworks)
    elif pallate_name == "scandinavian":
        artworks = _filter_by_pallate(SCANDINAVIAN, artworks)
    elif pallate_name == "minimalist":
        artworks = _filter_by_pallate(MINIMALIST, artworks)
    elif pallate_name == "bohemian":
        artworks = _filter_by_pallate(BOHEMIAN, artworks)
    elif pallate_name == "industrial":
        artworks = _filter_by_pallate(INDUSTRIAL, artworks)
    elif pallate_name == "contemporary":
        artworks = _filter_by_pallate(CONTEMPORARY, artworks)
    else:
        logger.error(f"Undefined pallate name {pallate_name}")
    return artworks


def _filter_by_pallate(pallate, artworks):
    colors = [rgb2hex(tuple(color)) for color in pallate]
    artworks = artworks.filter(colors__name__in=colors)
    return artworks


# def remove_background(image_file):
#     im = Image.open(image_file)
#     im = remove(im)
#     return im
