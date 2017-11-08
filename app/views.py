from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.shortcuts import render

# main view
def main(request):
    return redirect(index)

def index(request):
    return render(request, 'app/index.html')