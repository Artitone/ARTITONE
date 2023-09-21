from django.db.models import Q

from artworks.models import Artwork
from artworks.models import Category
from artworks.utils.color_meter import filter_by_color_pallate


class Filter:
    def __init__(self, category=None, color=None, keyword=None):
        self.category = category
        self.color = color
        self.keyword = keyword

    def gen_dict(self):
        return {
            "category": self.category,
            "color": self.color,
            "keyword": self.keyword,
        }

    def search(self):
        artworks = Artwork.objects.all()
        if self.category is not None:
            artworks = filter_by_category(self.category, artworks)
        if self.color is not None:
            artworks = filter_by_color_pallate(self.color, artworks)
        if self.keyword is not None:
            artworks = artworks.filter(
                Q(title__icontains=self.keyword)
                | Q(content__icontains=self.keyword)
                | Q(tags__name__icontains=self.keyword)
            )
        return artworks


def filter_by_category(category_name, artworks):
    try:
        category = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        category = None
    if category:
        artworks = artworks.filter(category=category)
    return artworks


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
    filter = Filter(
        category=category_is_valid(category),
        color=color_is_valid(color),
        keyword=keyword,
    )
    return filter


def category_is_valid(category):
    return category


def color_is_valid(color):
    return color
