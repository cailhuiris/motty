from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render

# main view
def index(request):
    return render(request, 'app/index.html')