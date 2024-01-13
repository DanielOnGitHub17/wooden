from django.shortcuts import render

# Create your views here.

def register_page(request, which="signup"):
    return render(request, 'signs.html', {"which": which})

def signin(request):
    data = request.POS