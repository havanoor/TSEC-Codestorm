from django.shortcuts import render
from .models import *





def list_crops(request):
    val=Crops.objects.all()
    

    return render(request,'cropdisplay.html',{'list':val})


def login(request):
    return render(request,'FarmerApp/login.html')