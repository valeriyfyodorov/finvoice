from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.
def index(request):
    context = {'title': "Test Title"}
    return render(request, "frontside/index.html", context)



def logout_view(request):
    logout(request)
    return redirect('frontside:index')