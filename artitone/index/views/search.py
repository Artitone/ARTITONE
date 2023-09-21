from django.db.models import Q

from artworks.models import Artwork
from artworks.models import Category
from artworks.utils.color_meter import filter_by_color_pallate


class Filter:
    def __init__(self, category=None, color=None, texture=None, keyword=None):
        self.category = category
        self.color = color
        self.texture = texture
        self.keyword = keyword

    def gen_dict(self):
        return {
            "category": self.category,
            "color": self.color,
            "texture": self.texture,
            "keyword": self.keyword,
        }

    def search(self):
        artworks = Artwork.objects.all()
        if self.category is not None:
            artworks = filter_by_category(self.category, artworks)
        if self.color is not None:
            artworks = filter_by_color_pallate(self.color, artworks)
        if self.texture is not None:
            artworks = filter_by_texture(self.texture, artworks)
        if self.keyword is not None:
            artworks = artworks.filter(
                Q(title__icontains=self.keyword)
                | Q(content__icontains=self.keyword)
                | Q(tags__name__icontains=self.keyword)
            )
        return artworks


def filter_by_category(category, artworks):
    return artworks.filter(category=category)


def parse_search_filter(post):
    """Check if the input filters are valid:
    category(default empty string)
    duration(default empty string)
    distance(default 0)
    """
    # Category/Duration filter
    category = post.get("category")
    color = post.get("color")
    keyword = post.get("keyword")
    texture = post.get("texture")
    filter = Filter(
        category=category_is_valid(category),
        color=color_is_valid(color),
        texture=texture_is_valid(texture),
        keyword=keyword,
    )
    return filter


def category_is_valid(category):
    try:
        category = Category.objects.get(name=category)
    except Category.DoesNotExist:
        category = None
    return category


def color_is_valid(color):
    if color not in [
        "modern",
        "scandinavian",
        "minimalist",
        "bohemian",
        "industrial",
        "contemporary",
    ]:
        return None
    return color


def texture_is_valid(texture):
    if texture not in [Artwork.SATIN, Artwork.MATTE, Artwork.ROUGH]:
        return None
    return texture


def filter_by_texture(texture, artworks):
    return artworks.filter(texture=texture)
