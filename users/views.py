from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import get_user_model
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


User = get_user_model()

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            telephone = form.cleaned_data['telephone']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']

            user = User.objects.create_user(first_name=first_name, last_name=last_name,
            telephone = telephone, email=email, username=username, password=password)

            # user activation 
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('users/account_verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()


            # messages.success(request,'We have sent you an activation email, click the link in there to activate this account')
            return redirect('/users/login/?command=verification&email='+email)
        else:
            print(form.errors)
           
            
    else:
        print("something went wrong")
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid login credentials')
            return redirect('login')
    return render(request, 'users/login.html')





@login_required(login_url = 'login')
def logout(request):
    auth.logout(request) 
    messages.success(request, 'You have been logged out!')
    return redirect('login')

@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'users/dashboard.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__iexact=email)

            #reset password email
            current_site = get_current_site(request)
            mail_subject = "Please reset your password"
            message = render_to_string('users/reset_password_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request,'Password reset email has been sent to your email address')
            return redirect('login')

        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotPassword')

    return render(request, 'users/forgotPassword.html')



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active  = True
        user.save()
        messages.success(request,'Congratulations! your account has been activated')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation token, you may register for an account')
        return redirect('register')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = user._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request,'Reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'This link could be expired')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successful')
            return redirect('login')

        else:
            messages.error(request,'Password do not match')
            return redirect('resetPassword')
    else:
        return render(request, 'users/resetPassword.html')