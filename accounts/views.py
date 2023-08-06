from django.http import HttpResponse
from django.shortcuts import redirect, render

from vendor.forms import VendorForm
from .forms import MyUserForm
from .models import MyUser, UserProfile
from django.contrib import messages, auth 
# Create your views here.

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.!')
        return redirect('dashboard')
    elif request.method =='POST':
        # print(request.POST)
        form = MyUserForm(request.POST)
        if form.is_valid():
            # Create the user using the form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = MyUser.CUSTOMER
            # user.save()

            # Create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = MyUser.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = MyUser.CUSTOMER
            user.save()
            messages.success(request, "Your account has been registered successfully!")    
            return redirect('login')
        else:
            print(form.errors)    
    else:    
        form =  MyUserForm()

    context = {
        'form': form, 
    }
    return render(request, 'accounts/registerUser.html', context)

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.!')
        return redirect('dashboard')
    elif request.method =='POST':
        form = MyUserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = MyUser.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = MyUser.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "Your account has been registered successfully! Please wait for the approval.")   
            return redirect('login')
        else:
            print('Invalid form')  
            print(form.errors)  
            print(v_form.errors)  
    else:
        form = MyUserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/registerVendor.html', context)  


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.!')
        return redirect('dashboard')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(request, email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials ')
            return redirect('login')   
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')