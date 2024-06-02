from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from legaltech import settings
from accounts.tokens import generate_token
from accounts.models import Profile, LSP

# Client login view
def client_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("client:client_dashboard")
        else:
            messages.error(request, "Bad Credentials!!")
    return render(request, 'client/client_login.html')

# LSP login view
def lsp_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            myuser = get_object_or_404(User, username=username)
            user_profile = get_object_or_404(Profile, user=myuser)
            if user_profile.is_service_provider:
                login(request, user)
                return redirect("lsp:lsp_dashboard")
            else:
                return HttpResponse(f"<h1 style='color:red'>Hello {myuser.first_name}, your account is not yet activated! Please login after account confirmation.</h1>")
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('accounts:lsp_login')
    return render(request, 'lsp/lsp_login.html')

# User registration view
def user_registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try another username.")
            return redirect('user_registration')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('user_registration')

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric!")
            return redirect('home')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        messages.success(request, "Your account has been created successfully! Please check your email to confirm your email address in order to activate your account.")

        # Send welcome email
        subject = "Welcome to Law Desk!"
        message = f"Hello {myuser.first_name}!\nWelcome to Law Desk! Thank you for visiting our website.\nWe have also sent you a confirmation email, please confirm your email address.\n\nThanking You, Team Law Desk!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Send email confirmation
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Law Desk - Login!"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(email_subject, message2, settings.EMAIL_HOST_USER, [myuser.email])
        email.fail_silently = True
        email.send()

        return redirect('user_login')

    return render(request, 'client/client_registration.html')

# User login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("lsp:lsp_dashboard")
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('client:user_login')
    return render(request, 'client/user_login.html')

# User logout view
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

# Client registration view
def client_registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mnumber = request.POST.get('mnumber')
        dob = request.POST.get('dob')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zipcode = request.POST.get('zipcode')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try another username.")
            return redirect('accounts:client_registration')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('accounts:client_registration')

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric!")

        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        profile_user = Profile.objects.create(
            user=myuser,
            phone_number=mnumber,
            date_of_birth=dob,
            age=7,  # This seems hardcoded, make sure this is intended
            country=country,
            state_province=state,
            address_line=city,
            zip_code=zipcode
        )
        profile_user.save()

        messages.success(request, "Your account has been created successfully! Please check your email to confirm your email address in order to activate your account.")

        # Send welcome email
        subject = "Welcome to Law Desk!"
        message = f"Hello {myuser.first_name}!\nWelcome to Legal Tech Web App ! Thank you for visiting our website.\nWe have also sent you a confirmation email, please confirm your email address.\n\nThanking You, Team Law Desk!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Send email confirmation
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Legal Tech Web App!"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(email_subject, message2, settings.EMAIL_HOST_USER, [myuser.email])
        email.fail_silently = True
        email.send()

        return redirect('accounts:client_login')

    return render(request, 'client/client_registration.html')

# LSP registration view
def lsp_registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mnumber = request.POST.get('mnumber')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zipcode = request.POST.get('zipcode')
        lsp_type = request.POST.get('lsp_type')
        profile_picture = request.FILES.get('profile_picture')
        signature = request.FILES.get('signature')
        enrollment_number = request.POST.get('enrollment_number')
        enrollment_year = request.POST.get('enrollment_year')
        bcpc = request.FILES.get('bcpc')
        university_name = request.POST.get('university_name')
        llb_passout_year = request.POST.get('llb_passout_year')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try another username.")
            return redirect('accounts:lsp_registration')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('accounts:lsp_registration')

        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        profile_user = Profile.objects.create(
            user=myuser,
            phone_number=mnumber,
            date_of_birth=dob,
            gender=gender,
            age=age,
            profile_picture=profile_picture,
            country=country,
            state_province=state,
            address_line=city,
            city=city,
            zip_code=zipcode
        )
        profile_user.save()

        lsp_user = LSP.objects.create(
            user=myuser,
            lsp_type=lsp_type,
            signature=signature,
            enrollment_number=enrollment_number,
            bar_council_practicing_certificate=bcpc,
            enrollment_year=enrollment_year,
            university_llb_completed=university_name,
            llb_passout_year=llb_passout_year,
        )
        lsp_user.save()

        messages.success(request, "Your profile has been created successfully! You will receive a confirmation link after your profile verification. Once verified, activate your account, login, and start offering services on the Legal Tech web app.")

        # Send welcome email
        subject = "Welcome to Law Desk Web App"
        message = f"Hello {myuser.first_name}!\nWelcome to Law Desk! Your profile has been created successfully! You will receive a confirmation link after your profile verification. Once verified, activate your account, login, and start offering services on the Legal Tech web app.\nThank you for visiting our website.\n\nTeam Law Desk Web App!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('accounts:lsp_login')

    return render(request, 'lsp/lsp_registration.html')
