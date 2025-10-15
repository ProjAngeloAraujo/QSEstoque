from django.shortcuts import render

def home(request):
    return render(request, 'APPEstoque/home.html')