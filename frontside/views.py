from django.shortcuts import render

# Create your views here.
def index(request):
    context = {'title': "Test Title"}
    return render(request, "frontside/index.html", context)
