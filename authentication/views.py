from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

from .forms import SignUpForm, QueryForm

from udyam_backend.models import Content

def HomeView(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form  = QueryForm()
    return render(request, 'index.html', {'form': form, 'schedule': Content.objects.all()})

def LogoutView(request):
    logout(request)
    return redirect('/')

def LoginView(request):
    if request.method == 'POST':
        form1 = AuthenticationForm()
        form2 = SignUpForm()
        print(request.POST.get('submit'))
        if request.POST.get('submit') == 'Login':
            form1 = AuthenticationForm(request=request, data = request.POST)
            if form1.is_valid():
                print("YES")
                email = form1.cleaned_data.get('username')
                password = form1.cleaned_data.get('password')
                print(email, password)
                user = authenticate(email=email, password=password)
                print(user)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')
            else:
                print('else')
                return render(request, 'login.html', {'form1':form1, 'form2': form2, 'error': 'error'})
        elif request.POST.get('submit') == 'Sign up':
            print('signin')
            form2 = SignUpForm(request.POST)
            print(form2)
            if form2.is_valid():
                print('valid')
                user = form2.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your Udyam account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                })
                to_email = form2.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return render(request, 'email_verification.html')
    else:
        form1 = AuthenticationForm()
        form2 = SignUpForm()
    return render(request, 'login.html', {'form1':form1, 'form2': form2})

# def SignupView(request):
#     if request.method == 'POST':
    #     form = SignUpForm(request.POST)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         user.is_active = False
    #         user.save()
    #         current_site = get_current_site(request)
    #         mail_subject = 'Activate your Udyam account.'
    #         message = render_to_string('acc_active_email.html', {
    #             'user': user,
    #             'domain': current_site.domain,
    #             'uid':urlsafe_base64_encode(force_bytes(user.pk)),
    #             'token':account_activation_token.make_token(user),
    #         })
    #         to_email = form.cleaned_data.get('email')
    #         email = EmailMessage(mail_subject, message, to=[to_email])
    #         email.send()
    #         return HttpResponse('Please confirm your email address to complete the registration')
    # else:
    #     form = SignUpForm()
#     return render(request, 'signup.html', {'form': form})
        
def ActivateAccountView(request, uidb64, token):
    try:
        Users = get_user_model()
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        print(user)
        user.save()
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')