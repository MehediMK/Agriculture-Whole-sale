from django.shortcuts import redirect, render
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from account.models import User_info
from agro.models import ProductItem,BeatItem
from django.contrib.auth.models import User
from .forms import UserSignUpForm,UserInfo,UserFLEname
from .forms import UserSignUpForm,UserInfo
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
from django.contrib import messages

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print('successfully login in')
                return redirect('home')
            else:
                return render(request,'account/login.html')
        else:
            return render(request,'account/login.html')
    else:
        return redirect('home')


def signup_view(request):
    if not request.user.is_authenticated:
        form = UserSignUpForm()
        form1 = UserInfo()
        if request.method == "POST":
            form = UserSignUpForm(request.POST)
            form1 = UserInfo(request.POST , request.FILES or None)        

            if form.is_valid() and form1.is_valid():
                print(form1.cleaned_data['profile_pic'])
                userform = form.save()
                userinfo = form1.save(commit=False)
                userinfo.user = userform
                userinfo.save()
                try:
                    print("got it", request.META['HTTP_REFERER'])
                    from_email = settings.DEFAULT_FROM_EMAIL
                    message = f"Dear {form.cleaned_data['username']}, Thanks for create account.Your email address:{form.cleaned_data['email']}"
                    email = form.cleaned_data['email']
                    send_mail("Your account have been created!", message, from_email, [
                            email],  fail_silently=False,)
                    messages.success(
                        request, f"Account succefully created.")
                except BadHeaderError as error:
                    messages.error(request, f"{error}")
                return redirect('login')    

        return render(request,'account/signup.html',context={'form':form,'form1':form1})
    else:
        return redirect('home')

@login_required(login_url='/account/login/')
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        if cart := request.session.get('cart'):
            cart = {}
        return redirect('login')
    else:
        return redirect('login')


@login_required(login_url='/account/login/')
def user_profile(request):
    user = request.user
    user_profile = User_info.objects.get(user=user)
    products = ProductItem.objects.filter(user=user)
    beat_item = BeatItem.objects.filter(user=user)
    context = {
        'user':user,
        'profile':user_profile,
        'products':products,
        'beat_items':beat_item
    }
    return render(request,'account/dashboard.html',context)


@login_required(login_url='/account/login/')
def editUserInfo(request):
    if request.method == 'POST':
        mydata = User_info.objects.get(user=request.user)
        user = User.objects.get(username=request.user.username)
        form = UserInfo( request.POST, request.FILES or None, instance=mydata)
        form1 = UserFLEname( request.POST, request.FILES or None, instance=user)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
        return redirect('userprofile')
    else:
        mydata = User_info.objects.get(user=request.user)
        user = User.objects.get(username=request.user.username)
        form = UserInfo(instance=mydata)
        form1 = UserFLEname(instance=user)
    context={
        'form':form,
        'form1':form1,
        'userinfo':mydata,
    }
    return render(request,'account/editinfo.html',context)




class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'account/password_reset.html'
    email_template_name = 'account/password_reset_email.html'
    subject_template_name = 'account/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login')