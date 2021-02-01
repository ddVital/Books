from django.shortcuts import render

# index function
def index(request):
    return render(request, 'index.html')