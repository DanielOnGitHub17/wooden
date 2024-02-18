from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def lounge(request):
    # request.user is everything.
    return render(request, "lounge.html", {})