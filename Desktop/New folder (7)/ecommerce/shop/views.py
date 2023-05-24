from django.shortcuts import render
from .models import Product
# Create your views here.


def index(request):
   product = Product.objects.all()
   
   data ={
      'product':product
   }
   return render(request, 'index.html',data)