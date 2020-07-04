from .logic import *
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from .cart import *
from django.http import HttpResponse, JsonResponse,Http404
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
from .refdata import *
import re
from .decorators import *
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

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
                Buyer=form3.save()

                # buyer=Buyer.objects.create(form2.data)
                Buyer.set_password(Buyer.password)
                Buyer.is_farmer = False
                Buyer.is_buyer=True
                Buyer.save()
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
	return redirect('signup')

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


def buyerHome(request):
    return render(request,'FarmerApp/BuyerLand.html')




def CropCreate(request, id):
    filter1 = CropFilter.objects.get(pk=id)
    userr = request.user
    filter = CropFilter.objects
    print(filter1.name)
    print(type(userr))
    if request.method == 'POST':
        form = CropForm(request.POST,request.FILES)
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
    return render(request,'FarmerApp/Farmerf.html',{'filters':filter1,'form':form,'filter':filter})







def Crop_View(request):
    print("hello")
    crops = Crops.objects.filter(farmer=request.user)
    print(crops)
    return render(request, 'FarmerApp/CropView.html', {'crops':crops})


class UpdateCrop(LoginRequiredMixin, generic.UpdateView):
    model = Crops
    template_name = 'FarmerApp/CropUpdate.html'
    fields = ['quantity','price']
    success_url = reverse_lazy('crop_view')

    def get_object(self):
        crop = super(UpdateCrop, self).get_object()
        return crop


class DeleteCrop(LoginRequiredMixin, generic.DeleteView):
    model = Crops
    template_name = 'FarmerApp/CropDelete.html'
    success_url = reverse_lazy('crop_view')

    def get_object(self):
        crop = super(DeleteCrop, self).get_object()
        return crop

def cropd(request):
    filter = CropFilter.objects
    return render(request,'FarmerApp/Farmerf.html',{'filter':filter})

'''Buyer E-commerce start'''
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
            print(order.email)
            for item in cart:
                print(item['product'],item['price'],item['quantity'],item['product'].farmer)

                crop = get_object_or_404(Crops, id=item['product'].id)

                if crop.quantity >=item['quantity']:
                    crop.quantity = crop.quantity- item['quantity']
                crop.save()                  

                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            sendmail(request.user.username,order.email,order.id,cart.get_total_price())
            cart.clear()
            return render(request, 'FarmerApp/OrderCreated.html',{'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'FarmerApp/OrderCreate.html', {'cart': cart, 'form': form})

@api_view(('GET',))
def sugs(request,state):
    crops = state_crop_dict.get(state,{'none':'none'})
    cropcount = state_crop_dict_count.get(state,{'none':'none'})
    result = {
        'crops': crops,
        'counts':cropcount
    }
    return JsonResponse(result)

class CropView(generics.ListCreateAPIView):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    queryset = CropSeeds.objects.all()
    serializer_class = CropSeedSerializer

'''Buyer E-commerce End'''





'''Farmer E-commerce Start'''

def farm_product_list(request):
    userr = request.user
    seeds = CropSeeds.objects.all()
    ferts = fertilizer.objects.all()
    pests = pesticide.objects.all()
    #products = fertilizer.objects + CropSeeds.objects +pesticide.objects
    return render(request, 'FarmerApp/FarmerShop2.html', {'user':userr,'cropseeds':seeds, 'ferts':ferts, 'pests':pests})


def farm_product_detail(request, sc_id):
    userr = request.user
    if re.match("^cs[0-9]*[0-9]$",sc_id):
        model = 'cs'
    elif re.match("^f[0-9]*[0-9]$",sc_id):
        model = 'f'
    elif re.match("^p[0-9]*[0-9]$",sc_id):
        model = 'p'
    else:
        model = ''
    ref_dict = {
        'cs':CropSeeds,
        'f':fertilizer,
        'p':pesticide
    }
    try:
        item = get_object_or_404(ref_dict[model],pk=sc_id)
        print(item.p_id)
    except:
        return HttpResponse("Error")
    #product = get_object_or_404(item, id=sc_id,  available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'FarmerApp/FarmE/FarmerDetail.html', {'product': item,'user':userr,'cart_product_form': cart_product_form,'model':model})



@require_POST
def farm_cart_add(request, sc_id):
    cart = Cart1(request)
    if re.match("^cs[0-9]*[0-9]$",sc_id):
        model = 'cs'
    elif re.match("^f[0-9]*[0-9]$",sc_id):
        model = 'f'
    elif re.match("^p[0-9]*[0-9]$",sc_id):
        model = 'p'
    else:
        model = ''

    ref_dict = {
        'cs':CropSeeds,
        'f':fertilizer,
        'p':pesticide
    }
    item = get_object_or_404(ref_dict[model],pk=sc_id)
    #product = get_object_or_404(item, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=item, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('farmer_cart_detail')

def farm_cart_remove(request, pid):
    cart = Cart1(request)
    if re.match("^cs[0-9]*[0-9]$",sc_id):
        model = 'cs'
    elif re.match("^f[0-9]*[0-9]$",sc_id):
        model = 'f'
    elif re.match("^p[0-9]*[0-9]$",sc_id):
        model = 'p'
    else:
        model = ''

    ref_dict = {
        'cs':CropSeeds,
        'f':fertilizer,
        'p':pesticide
    }
    item = get_object_or_404(ref_dict[model],pk=sc_id)
    #product = get_object_or_404(tot, id=pid)
    cart.remove(item)
    return redirect('farmer_cart_detail')

def farm_cart_clear(request):
    cart = Cart1(request)
    cart.clear()
    return redirect('farmer_cart_detail')

def farm_cart_detail(request):
    cart = Cart1(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'override': True})
    return render(request, 'FarmerApp/FarmE/FarmerCartDetail.html', {'cart': cart})

def farm_order_create(request):
    cart = Cart1(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            #for item in cart:
                #OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            sendmail(request.user.username,order.email,order.id,cart.get_total_price())
            cart.clear()
            return render(request, 'FarmerApp/FarmE/FarmerOrderCreated.html',{'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'FarmerApp/FarmE/FarmerOrderCreate.html', {'cart': cart, 'form': form})

'''Farmer E-commerce End'''
def hin_view(request):
    userr = request.user
    return render(request,'FarmerApp/FarmerLand Hindi.html',{'user':userr})



'''Farmer E-commerce End'''







def individual_product(request,model ,sc_id):

    ref_dict = {
        'c': Crops,
        'cs':CropSeeds,
        'f':fertilizer,
        'p':pesticide
    }
    try:
        item = get_object_or_404(ref_dict[model],pk=sc_id)
    except:
        return HttpResponse("Error")
    return render(request,'FarmerApp/IndividualList.html',{'item':item})
