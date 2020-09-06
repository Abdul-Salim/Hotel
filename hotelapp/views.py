
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import Customer, Hotels, Rooms
from .forms import CustomerForm, HotelForm, RoomForm
from .forms import StaffForm, LoginCustomerForm, LoginStaffForm
from django.shortcuts import render , get_object_or_404
from django.template import loader
def home(request):
    t = loader.get_template("index.html")
    form1 = RoomForm()
    rooms = Rooms.objects.filter(booked = False)
    hotel = Hotels.objects.all()
    user = request.user.id
    customer = Customer(id=request.user.id)
    hotels = Hotels(owner=customer)
    if request.method == 'POST':
        if 'room' in request.POST:
            form1 = RoomForm(request.POST,request.FILES)
            if form1.is_valid():
                obj = form1.save(commit=False)
                obj.owner = request.user
                obj.hotel = hotels
                obj.save()
                return HttpResponseRedirect('/my_ads', request)
            else:
                x = form1.errors
                return render(request, 'index.html', {'x': x,'form1':form1})
        if 'search' in request.POST:
            location = request.POST['location']
            checkin = request.POST['checkin']
            checkout = request.POST['checkout']
            adults = request.POST['adults']
            children = request.POST['children']
            rooms = Rooms.objects.filter( available_from__lte=checkin , available_to__gte=checkout , adults__gte=adults ,
                                         children__gte=children , location=location )
            context = {'checkin':checkin,'checkout':checkout,'location':location}
            return render(request,'search.html',{'rooms':rooms,'context':context})
    return HttpResponse(t.render({'form1':form1,'rooms':rooms,'hotel':hotel},request))


def customer_signup(request):
    t = loader.get_template("signup.html")
    msg = 'Customers register here'
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/',request)
        else:
            x = form.errors
            return render(request , 'signup.html',{'x': x, 'form': form})
    return HttpResponse(t.render({'form':form,"nsg":msg},request))

def staff_signup(request):
    t = loader.get_template("signup.html")
    form = StaffForm()
    msg = 'Hotels register here'
    if request.method == 'POST':
        form = StaffForm(request.POST,initial={'is_staff': True})
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            staff = authenticate(username=username , password=password)
            if staff is not None:
                auth.login(request,staff)
            return HttpResponseRedirect('/add_hotel',request)
        else:
            x = form.errors
            return render(request, 'signup.html', {'x': x,'form':form})
    return HttpResponse(t.render({'form':form,'msg':msg},request))

def login_customer(request):
    t = loader.get_template("login.html")
    form = LoginCustomerForm()
    if request.method == 'POST':
        form = LoginCustomerForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            customer = authenticate(username=username , password=password)
            if customer is not None:
                print(customer)
                auth.login(request,customer)
                return HttpResponseRedirect('/?next',request)
            else:
                x = form.errors
                return render(request, 'login.html', {'x': x,'form':form})
    return HttpResponse(t.render({'form':form},request))

def login_staff(request):
    t = loader.get_template("login.html")
    form = LoginStaffForm()
    if request.method == 'POST':
        form = LoginStaffForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            customer = authenticate(username=username , password=password, email=email)
            if customer is not None:
                auth.login(request,customer)
                return HttpResponseRedirect('/my_ads',request)
            else:
                x = form.errors
                return render(request, 'login.html', {'x': x,'form':form})
    return HttpResponse(t.render({'form':form},request))
@login_required()
def myads(request):
    t = loader.get_template("myads.html")
    rooms = Rooms.objects.filter(owner = request.user.id)
    hotel = Hotels.objects.filter(owner = request.user.id)
    return HttpResponse(t.render({'rooms':rooms,'hotel':hotel},request))
@login_required()
def add_hotel(request):
    t = loader.get_template("add_hotel.html")
    form = HotelForm()
    if request.method == 'POST':
        form = HotelForm(request.POST,request.FILES)
        customer = Customer.objects.get(id=request.user.id)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = customer
            obj.save()
            return HttpResponseRedirect('/my_ads',request)
        else:
            form = HotelForm()
            x = form.errors
            return render(request , 'add_hotel.html' , {'x': x, 'form': form})
    return HttpResponse(t.render({'form':form},request))
@login_required()
def add_room(request):
    t = loader.get_template("add_room.html")
    form = RoomForm()
    if request.method == 'POST':
        customer = Customer.objects.get(id=request.user.id)
        hotels = Hotels.objects.get(owner=request.user.id)
        form = RoomForm(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = customer
            obj.hotel = hotels
            obj.save()
            return HttpResponseRedirect('/my_ads',request)
        else:
            form = RoomForm()
            x = form.errors
            return render(request,'add_room.html',{'x':x,'form':form})
    return HttpResponse(t.render({'form':form},request))
@login_required()
def delete_ad(request,id):
    ad = get_object_or_404(Rooms,pk=id)
    if request.method == 'POST':
        if ad.owner_id == request.user.id:
            if 'delete' in request.POST:
                ad.delete()
            return HttpResponseRedirect('/my_ads',request)
        else:
            msg = "you are not allowed to delete this post"
            return render(request,'myads.html',{'msg':msg})
@login_required()
def edit_ad(request,id):
    t = loader.get_template("edit_ad.html")
    ad = get_object_or_404( Rooms , pk=id )
    form1 = RoomForm(instance=ad)
    edt = False
    if request.method == 'POST':
        edt = True
        form1 = RoomForm(request.POST,request.FILES,instance=ad )
        if form1.is_valid():
            obj = form1.save(commit=False)
            obj.save()
            return HttpResponseRedirect('/my_ads',request)
        else:
            x = form1.errors
            return render( request , 'edit_ad.html' , {'x': x , 'form': form1} )
    return HttpResponse(t.render({'edt':edt,'form1':form1},request))

@login_required()
def book_room(request,id):
    ad = get_object_or_404( Rooms , pk=id )
    if request.method == 'POST':
        if 'yes' in request.POST:
            ad.booked = True
            ad.save()
            return HttpResponseRedirect( '/', request )
        else:
            return HttpResponseRedirect( '/', request )

def search(request):
    rooms = Rooms.objects.filter(booked = False)
    return render( request , 'search.html' , {'rooms': rooms} )

def about(request):
    t = loader.get_template("about.html")
    rooms = Rooms.objects.all()
    hotels = Hotels.objects.all()
    return HttpResponse(t.render({'rooms':rooms,'hotels':hotels},request))
def hotel_list(request):
    t = loader.get_template("hotel_list.html")
    hotels = Hotels.objects.all()
    return HttpResponse(t.render({'hotels':hotels},request))

