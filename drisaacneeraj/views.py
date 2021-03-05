from django.shortcuts import render, get_object_or_404

def homepage(request):
    return render(request, 'base/index.html', {})

def about(request):
    return render(request, 'base/about.html', {})

def resume(request):
    return render(request, 'base/resume.html', {})

def services(request):
    return render(request, 'base/services.html', {})

def contact(request):
    return render(request, 'base/contact.html', {})

def locations(request):
    return render(request, 'base/locations.html', {})