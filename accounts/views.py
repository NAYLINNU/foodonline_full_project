from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required,user_passes_test
# from accounts.utils import detectUser
from accounts.utils import detectUser
from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.core.exceptions import PermissionDenied


 #Restrict the vendor from accessing the customer page for 403 forbiden error using with user_passes_test
def check_role_vendor(user):
    if user.role == 1:
        
        return True
    else:
        raise PermissionDenied

#Restrict the customer from accessing the vendor page for 403 forbiden error using with user_passes_test
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already login')
        return redirect('myAccount')
    elif request.method == 'POST':
        
        form = UserForm(request.POST)
        
        if form.is_valid():
            # created the user using form for hashing password
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER 
            # user.save()
            
            # created the user using create_user method in model
            
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.CUSTOMER
            user.save() 
            
            # #Send verification Email
            # mail_subject = 'Please activate your account'
            # email_template = 'accounts/emails/acc_verify_email.html'
            # send_verification_email(request, user, mail_subject,email_template )
            
            messages.success(request, 'Your account have been register successfully')
            return redirect('registerUser')
        
        #checking error field in form
        else:       
            print('Invalit Form')
            print(form.errors)
            
    else:
        form = UserForm()
    context = {
        'form':form,
    }
    return render(request,'accounts/registerUser.html',context)



def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already login')
        return redirect('myAccount')
    elif request.method =='POST':
        #Store the data and Create User
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            # vendor_name = v_form.cleaned_data['vendor_name']
            # vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile= user_profile
            vendor.save()
    
            # # #Send verification Email
            # mail_subject = 'Please activate your account'
            # email_template = 'accounts/emails/acc_verify_email.html'
            # send_verification_email(request, user, mail_subject,email_template )
            
            messages.success(request, 'Your account have been register successfully Please wait for approval.')
            return redirect('registerVendor')
        else:
            print('Invalit Form')
            print(form.errors)
                    
                
    else:
        form = UserForm()
        v_form = VendorForm()
    context = {
        'form':form,
        'v_form':v_form,
    }
    return render(request,'accounts/registerVendor.html',context)



def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already login')
        return redirect('myAccount')
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,'Login Successfully')
            return redirect('myAccount')
        else:
            messages.error(request,'Login Faild . Please Check your email and password ')
            return redirect('login')
        
    return render(request,'accounts/login.html')




def logout(request):
    auth.logout(request)
    messages.info(request,'Logout Successfully')
    return redirect('login')


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@user_passes_test(check_role_customer)
@login_required(login_url='login')
def custDashboard(request):
    return render(request,'accounts/custDashboard.html')


@user_passes_test(check_role_vendor)
@login_required(login_url='login')
def vendorDashboard(request):
    return render(request,'accounts/vendorDashboard.html')