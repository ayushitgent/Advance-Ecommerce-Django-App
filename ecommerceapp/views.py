from django.shortcuts import render
from ecommerceapp.models import Contact,Product,Orders,OrderUpdate
from django.contrib import messages
from math import ceil
# Create your views here.
def index(request):
    allProds=[]
    catprods = Product.objects.values('subcategory','id')
    cats = { item['subcategory'] for item in catprods}
    for cat in cats:
        prod =  Product.objects.filter(subcategory=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nSlides),nSlides])
    params={'allProds':allProds}
    print(allProds)
    return render(request,"index.html",params)  


def checkout(request):    
    return render(request,"checkout.html")   


def profile(request):    
    return render(request,"profile.html")   


def contact(request):
    if request.method =="POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        desc=request.POST.get('desc')
        pnumber=request.POST.get('number')
        myquery=Contact(firstName=fname,lastName=lname,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        messages.info(request,"We will get back to you soon.. ")
    return render(request,"contact.html")
