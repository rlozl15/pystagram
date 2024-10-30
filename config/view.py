from django.shortcut import render

def index(request):
    return render(request, "index.html")