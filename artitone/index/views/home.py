from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.shortcuts import render

from artworks.models import Artwork
from index.views.search import parse_search_filter

def home(request):
    """Directs the user to their home page."""
    # if request.user.is_authenticated:
    #     return redirect(f"profile/{request.user.pk}")
    print(request.GET)
    filter = parse_search_filter(request.GET)
    artwork_list = filter.search()
    paginator = Paginator(artwork_list, 4)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "index/index.html", {"page_obj": page_obj})