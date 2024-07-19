from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
import requests
from django.core.files.storage import default_storage
from django.conf import settings
from .forms import SearchForm, LoginForm, SignupForm, EditUserForm
from .books import BookObject, RBook
from .models import Book, User
from datetime import datetime
from .utitlities import hashgen, reformat_date
# Create your views here.

def homeview(request):
    return render(request, 'index.html', {"user": request.COOKIES.get('sessioncookie')})

def searchview(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['searchfield']
            result = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={query}&key=#APIKEY").json()
            books = []
            for item in result["items"]:
                volume_info = item.get("volumeInfo", {})
                title = volume_info.get("title", "No Title Available")
                subtitle = volume_info.get("subtitle", "No Subtitle Available")
                publisher = volume_info.get("publisher", "No Publisher Listed")
                publishDate = volume_info.get("publishedDate", "No Publish Date Available")
                authors = volume_info.get("authors", ["No Authors Listed"])
                thumbnail = volume_info.get("imageLinks", {}).get("thumbnail", "/static/assets/img/default.png")
                description = volume_info.get("description", "No Description Available")
                id = item.get("id")
            
                authors = ", ".join(authors)
                book = BookObject(title=title, publishdate=publishDate, subtitle=subtitle, publisher=publisher, authors=authors, thumbnail=thumbnail, description=description, id=id)
                books.append(book)
            return render(request, 'search.html', {'books': books, "user": request.COOKIES.get('sessioncookie')})
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form, "user": request.COOKIES.get('sessioncookie')})

def aboutview(request):
    return render(request, 'about.html', {"user": request.COOKIES.get('sessioncookie')})

def mylibview(request):
    if request.method == "POST":
        user_id = request.COOKIES.get('sessioncookie')
        if user_id:
            user = User.objects.filter(id=user_id)
            if user:
                Book.objects.filter(id=request.POST.get('id')).delete()
                user.update(readbooks=User.objects.get(id=user_id).readbooks-1)
                return redirect('/mylib/')
            else:
                return redirect('/signup/')
        else:
            return redirect('/login/')
    else:
        user_id = request.COOKIES.get('sessioncookie')
        if user_id:
            user = User.objects.filter(id=user_id)
            if user:
                books = Book.objects.filter(userid=user_id)
                rbooks = []
                for book in books:
                    rbook = RBook(title=book.title, subtitle=book.subtitle, publisher=book.publisher, authors=book.authors, thumbnail=book.thumbnail, description=book.description, id=book.id, publishdate=book.publishdate, rating=book.rating, start_date=book.started_reading, end_date=book.ended_reading)
                    rbooks.append(rbook)
                return render(request, 'mybooks.html', {'books': rbooks, "user": request.COOKIES.get('sessioncookie')})
            else:
                return redirect('/signup/')
        else:
            return redirect('/login/')
        
def loginview(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=email, password=hashgen(password))
            if user:
                user_id = user[0].id
                response = redirect('/mylib/')
                response.set_cookie('sessioncookie', user_id)
                return response
            else:
                return redirect('/signup/')
    else:
        return render(request, 'login.html', {"user": request.COOKIES.get('sessioncookie')})
    
def signupview(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User(username=username, email=email, password=hashgen(password), readbooks=0)
            user.save()
            response = redirect('/mylib/')
            response.set_cookie('sessioncookie', user.id)
            return response
    else:
        return render(request, 'signup.html', {"user": request.COOKIES.get('sessioncookie')})
    
def addbookview(request):
    cookie = request.COOKIES.get('sessioncookie')
    if cookie:
        user = User.objects.filter(id=cookie)
        if user:
            title = request.POST.get('title')
            authors = request.POST.get('authors')
            subtitle = request.POST.get('subtitle')
            publisher = request.POST.get('publisher')
            publishDate = request.POST.get('publishedDate')
            thumbnail = request.POST.get('thumbnail')
            description = request.POST.get('description')
            id = request.POST.get('id')
            book = BookObject(title=title, publishdate=publishDate, subtitle=subtitle, publisher=publisher, authors=authors, thumbnail=thumbnail, description=description, id=id)
            return render(request, 'addbook.html', {'book': book, 'user': request.COOKIES.get('sessioncookie')})
        else:
            return render(request, 'addbook.html', {'user': request.COOKIES.get('sessioncookie')})  # Render the form with errors
    else:
        return redirect('/login/')
    
    
def savebookview(request):
    
    title = request.POST.get('title')
    authors = request.POST.get('authors')
    subtitle = request.POST.get('subtitle')
    publisher = request.POST.get('publisher')
    publishDate = request.POST.get('publishedDate')
    thumbnail = request.POST.get('thumbnail')
    description = request.POST.get('description')
    id = request.POST.get('id')
    rating = request.POST.get('rating')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    book = Book(title=title, userid=request.COOKIES.get('sessioncookie'), publishdate=publishDate, subtitle=subtitle, publisher=publisher, authors=authors, thumbnail=thumbnail, description=description, rating=rating, started_reading=start_date, ended_reading=end_date)
    book.save()
    User.objects.filter(id=request.COOKIES.get('sessioncookie')).update(readbooks=User.objects.get(id=request.COOKIES.get('sessioncookie')).readbooks+1)
    return redirect('/mylib/')

def startreadingview(request):
    title = request.POST.get('title')
    authors = request.POST.get('authors')
    subtitle = request.POST.get('subtitle')
    publisher = request.POST.get('publisher')
    publishDate = request.POST.get('publishedDate')
    thumbnail = request.POST.get('thumbnail')
    description = request.POST.get('description')
    start_date = datetime.now().strftime("%Y-%m-%d")
    book = Book(title=title, userid=request.COOKIES.get('sessioncookie'), publishdate=publishDate, subtitle=subtitle, publisher=publisher, authors=authors, thumbnail=thumbnail, description=description, rating=None, started_reading=start_date, ended_reading=None)
    book.save()
    return redirect('/mylib/')

def finishreadingview(request):
    id = request.POST.get('id')
    return render(request, 'finish.html', {'id': id, 'user': request.COOKIES.get('sessioncookie')})

def finish(request):
    id = request.POST.get('id')
    rating = request.POST.get('rating')
    Book.objects.filter(id=id).update(rating=rating, ended_reading=datetime.now().strftime("%Y-%m-%d"))
    User.objects.filter(id=request.COOKIES.get('sessioncookie')).update(readbooks=User.objects.get(id=request.COOKIES.get('sessioncookie')).readbooks+1)
    return redirect('/mylib/')

def editview(request):
    title = request.POST.get('title')
    authors = request.POST.get('authors')
    subtitle = request.POST.get('subtitle')
    publisher = request.POST.get('publisher')
    publishDate = request.POST.get('publishedDate')
    thumbnail = request.POST.get('thumbnail')
    description = request.POST.get('description')
    id = request.POST.get('id')
    rating = request.POST.get('rating')
    start_date = reformat_date(request.POST.get('start_date'))
    try:
        end_date = reformat_date(request.POST.get('end_date'))
    except:
        end_date = None
    book = RBook(title=title, publishdate=publishDate, subtitle=subtitle, publisher=publisher, authors=authors, thumbnail=thumbnail, description=description, id=id, rating=rating, start_date=start_date, end_date=end_date)
    return render(request, 'edit.html', {'book': book, 'user': request.COOKIES.get('sessioncookie')})

def edit(request):
    rating = request.POST.get('rating')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    Book.objects.filter(id=request.POST.get('id')).update(rating=rating, started_reading=start_date, ended_reading=end_date)
    return redirect('/mylib/')
<<<<<<< HEAD
=======

def userview(request):
    user = User.objects.get(id=request.COOKIES.get('sessioncookie'))
    return render(request, 'user.html', {'user': user, 'username': user.username.title()})

def usereditview(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                if username != '':
                    User.objects.filter(id=request.COOKIES.get('sessioncookie')).update(username=username)
            except:
                pass
            
            try:
                email = form.cleaned_data['email']
                if email != '':
                    User.objects.filter(id=request.COOKIES.get('sessioncookie')).update(email=email)
            except:
                pass
            
            try:
                password = form.cleaned_data['password']
                if password != '':
                    User.objects.filter(id=request.COOKIES.get('sessioncookie')).update(password=password)
            except:
                pass
            return redirect('/user/')
    else:
        user = User.objects.get(id=request.COOKIES.get('sessioncookie'))
        return render(request, 'useredit.html', {'user': user, 'username': user.username.title()})
    
def logoutview(request):
    response = redirect('/')
    response.delete_cookie('sessioncookie')
    return response

def deleteuserview(request):
    user = User.objects.get(id=request.COOKIES.get('sessioncookie'))
    user.delete()
    return redirect('/')
>>>>>>> 2bb7399 (added user profile page, change whole size of page)
