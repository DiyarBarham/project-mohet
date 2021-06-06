from django.shortcuts import render, redirect
from mohet_app.models import Subscription, User, Role, Article
from django.contrib import messages
import bcrypt

def index(request):
    if 'user' in request.session:
        return redirect('/admin/home')
    return render(request, 'login.html')

def login(request):
    if 'user' in request.session:
        return redirect('/home')
 
    user = User.object.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user'] = logged_user.id
            return redirect('/admin/home')
    messages.error(request, 'الإيميل وكلمة السر لا يتطابقان')
    return redirect('/admin')

def logout(request):
    if 'user' in request.session:
        request.session.clear()
    return redirect('/admin')

def home(request):
    if 'user' not in request.session:
        return redirect('/admin/login')
    context = {
        'user': User.object.get(id=request.session['user'])
    }
    return render(request, 'index.html', context)

def new_article(request):
    if 'user' not in request.session:
        return redirect('/admin/login')
    context = {
        'user': User.object.get(id=request.session['user'])
    }
    return render(request, 'new article.html', context)
def new_user(request):
    if 'user' not in request.session:
        return redirect('/admin/login')
    context = {
        'user': User.object.get(id=request.session['user']),
        'jobs': Role.objects.all()
    }
    return render(request, 'new user.html', context)
def new(request):
    if 'user' not in request.session:
        return redirect('/admin/login')
    errors = User.object.basic_validator(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash messagecopy
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/admin/new_user')
    password = request.POST['pass']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.object.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=pw_hash, gender=request.POST['gridRadios'], birthday=request.POST['date'], role_id=Role.objects.get(name=request.POST['job']))
    messages.success(request, "User successfully created")
    return redirect('/admin/new_user')

def accept_article(request):
    if 'user' not in request.session:
        return redirect('/admin/login')
    context = {
        'articles': Article.object.filter(status='Pending'),
        'user': User.object.get(id=request.session['user'])

    }
    return render(request, 'accept.html', context)
def accept(request, id):
    if 'user' not in request.session:
        return redirect('/admin/login')
    a = Article.object.get(id=id)
    a.status = 'Published'
    a.save()
    return redirect('/admin/accept_article')
def refuse(request, id):
    if 'user' not in request.session:
        return redirect('/admin/login')
    a = Article.object.get(id=id)
    a.status = 'Refused'
    return redirect('/admin/accept_article')
def view(request, id):
    if 'user' not in request.session:
        return redirect('/admin/login')
    context = {
        'article': Article.object.get(id=id),
        'user': User.object.get(id=request.session['user'])
    }
    return render(request, 'article.html', context)
def narticle(request):
    if 'user' not in request.session:
        return redirect('/admin/login')
    x = Article.object.create(title=request.POST['title'], description=request.POST['editordata'], status='Pending')
    x.user_id.add(User.object.get(id=request.session['user']))
    return redirect('/admin/new_article')