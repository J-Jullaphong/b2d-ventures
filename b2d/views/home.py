from django.shortcuts import render


def home(request):
    return render(request, template_name="b2d/home.html")
