from django.shortcuts import render

def index(request):
    """The home page for Bugger"""
    return render(request, 'bugs/index.html')