from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page


@login_required()
def tutorial_list(request):
    return render(request, "tutorial/tutorialList.html")