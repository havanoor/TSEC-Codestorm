from django.shortcuts import render, redirect
from .models import *

from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

from .forms import *
from django.contrib.auth import login, authenticate, logout




def list_crops(request):
    val=Crops.objects.all()

    return render(request,'FarmerApp/cropdisplay.html',{'list':val})

def suggestion(request):
    return HttpResponse("suggestion")
def farmersell(request):
    seeds = CropSeeds.objects.all()
    ferts = fertilizer.objects.all()
    pests = pesticide.objects.all()
    return render(request,'FarmerApp/FarmerShop.html',{'cropseeds':seeds, 'ferts':ferts, 'pests':pests})

@api_view(('GET',))
def order(request, pref):
    if pref=="cost":
        seeds = CropSeeds.objects.order_by("price")
        ferts = fertilizer.objects.order_by("price")
        pests = pesticide.objects.order_by("price")
        seeds = list(seeds)
        ferts = list(ferts)
        pests = list(pests)
        ordered = {}
        d={}
        for i in range(0,len(seeds)):
            a=vars(seeds[i])
            a.pop('_state')
            d[i]=a
        
        ordered[0]=d
        d = {}
        for i in range(0,len(ferts)):
            a=vars(ferts[i])
            a.pop('_state')
            d[i]=a
        
        ordered[1] = d
        d={}
        for i in range(0,len(pests)):
            a=vars(pests[i])
            a.pop('_state')
            d[i]=a
        ordered[2] = d
        
        return JsonResponse(ordered)
        return HttpResponse("YO")
    if pref =="quality":
        seeds = CropSeeds.objects.order_by("-quality")
        ferts = fertilizer.objects.order_by("-quality")
        pests = pesticide.objects.order_by("-quality")
        seeds = list(seeds)
        ferts = list(ferts)
        pests = list(pests)
        ordered = {}
        d={}
        for i in range(0,len(seeds)):
            a=vars(seeds[i])
            a.pop('_state')
            d[i]=a
        
        ordered[0]=d
        d = {}
        for i in range(0,len(ferts)):
            a=vars(ferts[i])
            a.pop('_state')
            d[i]=a
        
        ordered[1] = d
        d={}
        for i in range(0,len(pests)):
            a=vars(pests[i])
            a.pop('_state')
            d[i]=a
        ordered[2] = d
        
        return JsonResponse(ordered)
        return HttpResponse("YO")
    else:
        return HttpResponse(pref)

  
    return render(request,'FarmerApp/cropdisplay.html',{'list':val})




'''Registration,login,logout start'''
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            if user.is_farmer:
                return redirect('farmer_add')
            else:
                return redirect('buyer_add')
    else:
        form = RegistrationForm()
    return render(request, 'FarmerApp/signup.html', {'form': form})


def register_farmer(request):
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        if form.is_valid():
            Farmer=form.save()
            Farmer.set_password(Farmer.password)
            Farmer.is_farmer = True
            Farmer.is_buyer=False
            Farmer.save()
            return redirect('login')
    else:
        form = FarmerForm()
    return render(request, 'FarmerApp/FarmerData.html', {'form': form})


def register_buyer(request):
    if request.method == 'POST':
        form = BuyerForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            Buyer=form.save()
            Buyer.set_password(Buyer.password)
            Buyer.is_farmer = False
            Buyer.is_buyer=True
            Buyer.save()
            return redirect('login')
    else:
        form = BuyerForm()
    return render(request, 'FarmerApp/BuyerData.html', {'form': form})


def login_view(request):
	context = {}
	user = request.user
	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user:
				login(request, user)
				if user.is_farmer:
					return redirect('farmer_home')
				else:
					return redirect('buyer_home')
	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form
	return render(request, 'FarmerApp/login.html', context)



def logout_view(request):
	logout(request)
	return redirect('home')




'''Registration,login,logout start'''




def farmerHome(request):
    return render(request,'FarmerApp/FarmerLand.html')


def buyerHome(request):
    return render(request,'FarmerApp/BuyerLand.html')

   


def login(request):
    return render(request,'FarmerApp/login.html')


