from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from .cart import Cart
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin



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
    userr = request.user
    return render(request,'FarmerApp/FarmerLand.html',{'user':userr})


def buyerHome(request):
    return render(request,'FarmerApp/BuyerLand.html')



def CropCreate(request, id):
    filter1 = CropFilter.objects.get(pk=id)
    userr = request.user
    print(filter1.name)
    print(type(userr))
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            crops = Crops()
            crops.farmer = Farmer.objects.get(username=userr.username)
            crops.category=filter1
            crops.slug = form.cleaned_data['name']
            crops.name = form.cleaned_data['name']
            crops.c_type = form.cleaned_data['c_type']
            crops.price = form.cleaned_data['price']
            crops.quantity = form.cleaned_data['quantity']
            crops.photo = form.cleaned_data['photo']
            crops.save()
            return redirect('farmer_home')
    else:
        form=CropForm()
    return render(request,'FarmerApp/FarmerCrop.html',{'filters':filter1,'form':form})



def cropd(request):
    filter = CropFilter.objects
    return render(request,'FarmerApp/Farmerf.html',{'filter':filter})


def product_list(request, filter_slug=None):
    filter1=None
    filter2 = CropFilter.objects.all()
    crops = Crops.objects.filter(available=True)
    if filter1_slug:
        filter1 = get_object_or_404(Category, slug=category_slug)
        crops = crops.filter(category=filter1)
    return render(request,'shop/product/list.html',{'category': category, 'categories': filter2,'products': crops})
