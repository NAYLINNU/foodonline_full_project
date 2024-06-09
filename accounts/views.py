from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm
from .models import User


def registerUser(request):
    # if request.user.is_authenticated:
    #     messages.warning(request,'You are already login')
    #     return redirect('registerUser')
    # elif request.method == 'POST':
        if request.method == 'POST':
    
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

