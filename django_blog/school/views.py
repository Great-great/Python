from django.shortcuts import render

# Create your views here.

def indexSchool(request):
    return render(request,'indexSchool.html')