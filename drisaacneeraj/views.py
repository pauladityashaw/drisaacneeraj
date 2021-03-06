from django.shortcuts import render

def homepage(request):
    return render(request, 'base/index.html', {})

def about(request):
    return render(request, 'base/about.html', {})

def contact(request):
    return render(request, 'base/contact.html', {})

def locations(request):
    return render(request, 'base/locations.html', {})