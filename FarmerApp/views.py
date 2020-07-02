from django.shortcuts import render
from .models import *





def list_crops(request):
    val=Crops.objects.all()


    return render(request,'FarmerApp/cropdisplay.html',{'list':val})
