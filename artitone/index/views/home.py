from django.shortcuts import redirect
from django.shortcuts import render


def home(request):
    """Directs the user to their home page."""
    # if request.user.is_authenticated:
    #     return redirect(f"profile/{request.user.pk}")
    return render(request, "index/index.html")