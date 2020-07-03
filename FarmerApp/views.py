
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from .cart import Cart
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.http import require_POST
import json
from .serializers import CropSeedSerializer
from rest_framework import generics
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
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
                    return redirect('product_list')
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


def farmersell(request):
    seeds = CropSeeds.objects.all()
    ferts = fertilizer.objects.all()
    pests = pesticide.objects.all()
    return render(request,'FarmerApp/FarmerShop.html',{'cropseeds':seeds, 'ferts':ferts, 'pests':pests})

def dashboard(request):
    return render(request, 'FarmerApp/FarmerLand.html')

def suggestion(request):
        
    return render(request,'FarmerApp/suggestion.html')

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
    userr = request.user
    filter = CropFilter.objects
<<<<<<< HEAD
    return render(request,'FarmerApp/Farmerf.html',{'filter':filter,'user':userr})



def product_list(request, category_slug=None):
    userr = request.user
    category = None
    categories = CropFilter.objects.all()
    products = Crops.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(CropFilter, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'FarmerApp/BuyerLand.html', {'category': category, 'categories': categories, 'products': products,'user':userr})

def product_detail(request, id, slug):
    userr = request.user
    product = get_object_or_404(Crops, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'FarmerApp/BuyerDetail.html', {'product': product,'user':userr,'cart_product_form': cart_product_form})





@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Crops, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])

    return redirect('cart_detail')




def cart_remove(request, pid):
    cart = Cart(request)
    product = get_object_or_404(Crops, id=pid)
    cart.remove(product)
    return redirect('cart_detail')

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'override': True})
    return render(request, 'FarmerApp/CartDetail.html', {'cart': cart})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            return render(request, 'FarmerApp/OrderCreated.html',{'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'FarmerApp/OrderCreate.html', {'cart': cart, 'form': form})

=======
    return render(request,'FarmerApp/Farmerf.html',{'filter':filter})
  
>>>>>>> e0097b4b9c618fd29f500de87f4fbe77b062d91b
@api_view(('GET',))
def sugs(request,state):
    d= {'Gujarat': ['Sugarcane',
  'Cotton(lint)',
  'Onion',
  'Groundnut',
  'Potato',
  'Wheat',
  'Oilseeds total',
  'Banana',
  'Maize',
  'Bajra'],
 'Goa': ['Coconut ',
  'Rice',
  'Sugarcane',
  'Other Vegetables',
  'Other Fresh Fruits',
  'Cashewnut',
  'Banana',
  'Other  Rabi pulses',
  'Groundnut',
  'Mango'],
 'Nagaland': ['Sugarcane',
  'Rice',
  'Niger seed',
  'Potato',
  'Jute',
  'Maize',
  'Rapeseed &Mustard',
  'Tapioca',
  'Soyabean',
  'Oilseeds total'],
 'Tripura': ['Rice',
  'Potato',
  'Sugarcane',
  'Jute & mesta',
  'Mesta',
  'Jute',
  'Oilseeds total',
  'Maize',
  'Other Kharif pulses',
  'other oilseeds'],
 'Jammu and Kashmir ': ['Wheat',
  'Maize',
  'Rice',
  'Rapeseed &Mustard',
  'Bajra',
  'Potato',
  'Other Vegetables',
  'Jowar',
  'Barley',
  'Urad'],
 'Karnataka': ['Sugarcane',
  'Coconut ',
  'Dry ginger',
  'Maize',
  'Paddy',
  'Arecanut',
  'Arhar/Tur',
  'Cotton(lint)',
  'Banana',
  'Rice'],
 'Jharkhand': ['Rice',
  'Potato',
  'Wheat',
  'Maize',
  'Ragi',
  'Sugarcane',
  'Arhar/Tur',
  'Onion',
  'Masoor',
  'Gram'],
 'Himachal Pradesh': ['Wheat',
  'Maize',
  'Rice',
  'Potato',
  'Sugarcane',
  'Dry ginger',
  'Peas & beans (Pulses)',
  'Ginger',
  'Barley',
  'Small millets'],
 'Rajasthan': ['Wheat',
  'Bajra',
  'Rapeseed &Mustard',
  'Maize',
  'Guar seed',
  'Sugarcane',
  'Cotton(lint)',
  'Soyabean',
  'Gram',
  'Barley'],
 'Uttarakhand': ['Sugarcane',
  'Total foodgrain',
  'Wheat',
  'Rice',
  'Onion',
  'Potato',
  'Ragi',
  'Other Cereals & Millets',
  'Small millets',
  'Maize'],
 'Dadra and Nagar Haveli': ['Sugarcane',
  'Coconut ',
  'Rice',
  'Other  Rabi pulses',
  'Ragi',
  'Other Kharif pulses',
  'Arhar/Tur',
  'Urad',
  'Wheat',
  'Banana'],
 'Odisha': ['Rice',
  'Paddy',
  'Sugarcane',
  'Maize',
  'Sweet potato',
  'Onion',
  'Groundnut',
  'Jute',
  'Moong(Green Gram)',
  'Ragi'],
 'Manipur': ['Rice',
  'Banana',
  'Pineapple',
  'Potato',
  'Sugarcane',
  'Maize',
  'Other Fresh Fruits',
  'Dry ginger',
  'Cabbage',
  'Dry chillies'],
 'Chandigarh': ['Wheat',
  'Potato',
  'Maize',
  'Rice',
  'Onion',
  'Rapeseed &Mustard',
  'Arhar/Tur',
  'Masoor',
  'Urad',
  'Sunflower'],
 'Mizoram': ['Rice',
  'Sugarcane',
  'Maize',
  'Tapioca',
  'Other Kharif pulses',
  'other oilseeds',
  'Other  Rabi pulses',
  'Potato',
  'Sesamum',
  'Rapeseed &Mustard'],
 'Assam': ['Coconut ',
  'Sugarcane',
  'Rice',
  'Paddy',
  'Jute',
  'Potato',
  'Banana',
  'Pineapple',
  'Orange',
  'Ginger'],
 'Tamil Nadu': ['Coconut ',
  'Sugarcane',
  'Tapioca',
  'Banana',
  'Rice',
  'Total foodgrain',
  'Guar seed',
  'Maize',
  'Mango',
  'Groundnut'],
 'Kerala': ['Coconut ',
  'Tapioca',
  'Sugarcane',
  'Banana',
  'Rice',
  'Rubber',
  'Mango',
  'Pineapple',
  'Coffee',
  'Black pepper'],
 'Haryana': ['Sugarcane',
  'Wheat',
  'Cotton(lint)',
  'Rice',
  'Bajra',
  'Rapeseed &Mustard',
  'Potato',
  'Gram',
  'Guar seed',
  'Other Vegetables'],
 'Meghalaya': ['Potato',
  'Rice',
  'Jute',
  'Pineapple',
  'Total foodgrain',
  'Banana',
  'Dry ginger',
  'Citrus Fruit',
  'Mesta',
  'Cashewnut'],
 'West Bengal': ['Coconut ',
  'Oilseeds total',
  'Pulses total',
  'Potato',
  'Jute',
  'Rice',
  'Sugarcane',
  'Wheat',
  'Maize',
  'Rapeseed &Mustard'],
 'Arunachal Pradesh': ['Rice',
  'Oilseeds total',
  'Dry ginger',
  'Maize',
  'Sugarcane',
  'Potato',
  'Rapeseed &Mustard',
  'Small millets',
  'Wheat',
  'Dry chillies'],
 'Madhya Pradesh': ['Sugarcane',
  'Banana',
  'Wheat',
  'Soyabean',
  'Maize',
  'Rice',
  'Cotton(lint)',
  'Paddy',
  'Rapeseed &Mustard',
  'Potato'],
 'Punjab': ['Wheat',
  'Sugarcane',
  'Rice',
  'Cotton(lint)',
  'Maize',
  'Barley',
  'Groundnut',
  'Guar seed',
  'Rapeseed &Mustard',
  'Peas & beans (Pulses)'],
 'Andaman and Nicobar Islands': ['Coconut ',
  'Rice',
  'Banana',
  'Sugarcane',
  'Arecanut',
  'Tapioca',
  'Dry ginger',
  'Dry chillies',
  'Sweet potato',
  'Turmeric'],
 'Maharashtra': ['Sugarcane',
  'Banana',
  'Cotton(lint)',
  'Onion',
  'Maize',
  'Grapes',
  'Soyabean',
  'Jowar',
  'Bajra',
  'Rice'],
 'Puducherry': ['Coconut ',
  'Sugarcane',
  'Rice',
  'Paddy',
  'Tapioca',
  'Banana',
  'Mango',
  'Groundnut',
  'Urad',
  'Brinjal'],
 'Andhra Pradesh': ['Coconut ',
  'Sugarcane',
  'Rice',
  'Groundnut',
  'Cotton(lint)',
  'Maize',
  'other oilseeds',
  'Mango',
  'Mesta',
  'Banana'],
 'Uttar Pradesh': ['Sugarcane',
  'Potato',
  'Wheat',
  'Total foodgrain',
  'Rice',
  'Bajra',
  'Maize',
  'Urad',
  'Peas & beans (Pulses)',
  'Gram'],
 'Sikkim': ['Maize',
  'Total foodgrain',
  'Other Vegetables',
  'Potato',
  'Rice',
  'Small millets',
  'Other Kharif pulses',
  'Other Fresh Fruits',
  'Wheat',
  'Pulses total'],
 'Bihar': ['Sugarcane',
  'Rice',
  'Jute',
  'Wheat',
  'Maize',
  'Banana',
  'Potato',
  'Mesta',
  'Other  Rabi pulses',
  'Masoor'],
 'Telangana ': ['Coconut ',
  'Sugarcane',
  'Rice',
  'Cotton(lint)',
  'Maize',
  'Orange',
  'Soyabean',
  'Groundnut',
  'Turmeric',
  'Onion'],
 'Chhattisgarh': ['Sugarcane',
  'Rice',
  'Khesari',
  'Gram',
  'Maize',
  'Soyabean',
  'Potato',
  'Wheat',
  'Small millets',
  'Groundnut']}
    crops = d.get(state,{'none':'none'})
    return JsonResponse(crops,safe = False)

<<<<<<< HEAD

=======
>>>>>>> e0097b4b9c618fd29f500de87f4fbe77b062d91b
class CropView(generics.ListCreateAPIView):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    queryset = CropSeeds.objects.all()
    serializer_class = CropSeedSerializer


def individual_product(request, sc_id):
    item = get_object_or_404(CropSeeds,pk=sc_id)
    return render(request,'FarmerApp/IndividualList.html',{'item':item})
