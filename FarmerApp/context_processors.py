from .cart import *

def cart(request):
    return {'cart': Cart(request)}




def cart1(request):
    return {'cart1': Cart1(request)}
