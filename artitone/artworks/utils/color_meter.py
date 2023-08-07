import numpy as np
from PIL import Image
import scipy
import scipy.misc
import scipy.cluster

def rgb2hex(rgb):
    return '#%02x%02x%02x' % rgb

def hex2rgb(hex):
    hex = hex.lstrip('#')
    lv = len(hex)
    return np.array([int(hex[i:i+lv//3], 16) for i in range(0, lv, lv//3)])

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

def _get_dominant_color(image_file):
    """
    Take a file object and return the colour in hex code
    """

    im = image_file
    im = Image.open(im)
    im = im.resize((150, 150))  # optional, to reduce time
    colors = im.getcolors(im.size[0]*im.size[1])[:NUM_CLUSTERS]
    print(colors)
    colors = find_closet_colors(colors)
    colors = list(dict.fromkeys(colors))
    colors = [rgb2hex(tuple(color)) for color in colors]
    return colors

def find_closet_colors(colors):
    closest_palatte = []
    for c in colors:
        color = np.array([c[1][0], c[1][1], c[1][2]])
        distances = np.sqrt(np.sum((COLOR_PALETTE-color)**2,axis=1))
        index_of_smallest = np.where(distances==np.amin(distances))
        closest_palatte.append(tuple(COLOR_PALETTE[int(index_of_smallest[0])]))
    return closest_palatte
