from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Subscription
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'Home/index.html')

def articles(request):
    context = {
        
        "articles" : Article.object.filter(status='Published')
    }
    return render(request, 'Navbar/article_page.html', context)

def about(request):
    return render(request, 'Navbar/about_us.html')

def contact(request):
    return render(request, 'Navbar/contact_us.html')

def rigesterwith(request):
    Subscription.objects.create(email=request.POST['email'], name=request.POST['name'], status='active')
    data = {}
    data['msg'] = 'Thank You for your Subscription!'
    return JsonResponse(data)
def rigesterwithus(request):
    Subscription.objects.create(email=request.POST['email'], name=request.POST['name'], status='active')
    return redirect(f"/{request.POST['page']}")

def contact_us(request):
    name=request.POST['nemee']
    title=request.POST['emailee']
    desc=request.POST['note']
    number=request.POST['number']
    Contact.objects.create(title=title,name=name,description=desc,number=number)
    return redirect('/contact')

def image (request,id):
    context = {
        "article": Article.object.get(id = id)
    }
    return render(request, 'Navbar/single_article.html', context)
    
