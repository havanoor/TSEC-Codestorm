from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from .cart import Cart
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.http import require_POST



from .forms import *
from django.contrib.auth import login, authenticate, logout


'''Registration,login,logout start'''



def register(request):
    if request.method == 'POST':
        form2 = FarmerForm(request.POST)
        form=AccountAuthenticationForm(request.POST)
        print("1",form.is_valid())
        print("2",form2.is_valid())

        if form2.is_valid():
            print("-------->",form2.data)
            if ("is_farmer" in form2.data.keys()):
                print("------------->","yes")
                Farmer=form2.save()
                Farmer.set_password(Farmer.password)
                Farmer.is_farmer = True
                Farmer.is_buyer=False
                Farmer.save()

                return redirect('signup')
            else:
                print("no")
                print("Its a buyer")
                form3=BuyerForm(data=form2.data)
                print(form3)
                buyer=form3.save()

                # buyer=Buyer.objects.create(form2.data)
                buyer.set_password(Buyer.password)
                buyer.is_farmer = False
                buyer.is_buyer=True
                buyer.save()
                return redirect('signup')
            # Farmer=form.save()
            # Farmer.set_password(Farmer.password)
            # Farmer.is_farmer = True
            # Farmer.is_buyer=False
            # Farmer.save()
            # return redirect('login')

        elif form.is_valid():
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
        form=AccountAuthenticationForm()
        form2 = FarmerForm()

    return render(request, 'FarmerApp/login.html', {'form2': form2,'form':form})


def logout_view(request):
	logout(request)
	return redirect('home')


'''Registration,login,logout end'''



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
    else:
        return HttpResponse(pref)


    return render(request,'FarmerApp/cropdisplay.html',{'list':val})


def farmerHome(request):
    return render(request,'FarmerApp/FarmerLand.html')


def buyerHome(request):
    return render(request,'FarmerApp/BuyerLand.html')
