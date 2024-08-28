from django.shortcuts import render


def home(request):
    return render(request, 'b2d/home.html')

