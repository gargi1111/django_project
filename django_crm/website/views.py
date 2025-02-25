from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


# Create your views here.
# display some form in the homepage that allow users to login
def home(request:HttpRequest):    
    records = Record.objects.all()
     
    #check to see if logging in
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate: is this a valid user
        user = authenticate(request, username = username, password = password)
        if user:
            login(request, user)
            messages.success(request, "You have successfully logged in...")
            return redirect('home')   
        else:
            messages.success(request, "There was a problem logging you in...")  
            return redirect('home')
    else:  # they have already logged in, show them the records
        return render(request, 'home.html', {'records': records})

# login users
def login_user(request:HttpRequest):
    pass

# logout users
def logout_user(request:HttpRequest):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')

def register_user(request:HttpRequest):
    if request.method == 'POST':   #if they are filling out the form
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and log in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # authenticate
            user = authenticate(request, username = username, password = password)
            login(request, user)
            messages.success(request, "You have successfully registered")
            return redirect('home')
    else:  #going to the website, they want to fill out the form
        form = SignUpForm() #get the form 
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        # look up the record
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')
        
def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')     



def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
		return render(request, 'add_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')   

def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')

