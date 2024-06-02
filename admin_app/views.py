from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from legaltech import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth import authenticate, login, logout
from accounts.tokens import generate_token
from accounts.models import Profile,LSP
from django.shortcuts import get_object_or_404


def admin_dashboard(request):
    total_clients = Profile.objects.filter(is_client=True).count()
    total_service_providers = LSP.objects.count() 
    clients_data = Profile.objects.filter(is_client=True).values_list('account_creation_date', flat=True)
    service_providers_data = LSP.objects.values_list('enrollment_year', flat=True)
    clients_data = list(map(lambda d: d.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), clients_data))
    service_providers_data = list(map(str, service_providers_data))
    recent_lsp_profiles = LSP.objects.order_by('-user__date_joined')[:5]
    
    context = {
        'total_clients': total_clients,
        'total_service_providers': total_service_providers,
        'clients_data': clients_data,
        'service_providers_data': service_providers_data,
         'recent_lsp_profiles': recent_lsp_profiles,
    }
    return render(request, 'admin/admin_dashboard.html', context)


"""def users_list(request):
    # user_det=User.objects.all()
    # profile_user=Profile.objects.all()
    # lsp_users= LSP.objects.all()
    lsp_users = LSP.objects.all()
    profiles = Profile.objects.filter(user__in=lsp_users.values('user'))
    user_det = User.objects.filter(pk__in=lsp_users.values('user'))

    profiles_with_lsps = []

    for i in range(len(lsp_users)):
        profiles_with_lsps.append({
            'user_det': user_det[i],
            'lsp_user': lsp_users[i],
            'profile': profiles[i],
        })

    context = {
        'profiles_with_lsps': profiles_with_lsps,
    }
    
    return render(request,'admin/users_list.html',context)"""
    
    

def users_list(request):
    lsp_users = LSP.objects.all()
    users_data = []
    for lsp_user in lsp_users:
        profile = Profile.objects.get(user=lsp_user.user)
        users_data.append({
            'user_det': lsp_user.user,
            'lsp_user': lsp_user,
            'profile': profile,
        })
    context = {
        'users_data': users_data,
    }
    return render(request, 'admin/users_list.html', context)
   

def verify_profile(request,username):
    if request.method=="POST":
        myuser = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(Profile, user=myuser)
        if  user_profile.is_service_provider==True:
            return HttpResponse("LSP is Active")
        else:
            user_profile.is_service_provider=True
            print(user_profile.save())
            # subject = "Welcome law Desk Login!"
            # message = "Hello " + myuser.first_name + "!! \n" + "Welcome to law Desk!! \nThank you for visiting our website.\nWe have also sent you a confirmation email, please confirm your email address. \n\nThanking You Team Law Desk!"        
            # from_email = settings.EMAIL_HOST_USER
            # to_list = [myuser.email]
            # send_mail(subject, message, from_email, to_list, fail_silently=True)

            # Email Address Confirmation Email
            current_site = get_current_site(request)
            email_subject = "Account Verification Confirmation @ Law Desk - Login!"
            message2 = render_to_string('email_confirmation.html',{
                'name': myuser.first_name,
                'domain': current_site.domain,
                # 'domain':'https://legal-tech-webapp-git-sriram-sriramreddy-7.vercel.app',
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser),
            })
            email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
            )
            email.fail_silently = True
            email.send()

            return HttpResponse('<h1 style="color:green;">Profile Verified Sucessfully</h1>')
        
    else:
        return HttpResponse("Null Response")
    
    
    
def admin_lsp_profile(request,username):
    # user = get_object_or_404(User, username=username)
    user = get_object_or_404(User, username=username)
    print("e1")
    # Fetch the user profile based on the 'user' field in the Profile model
    user_profile = get_object_or_404(Profile, user=user)
    print("e2")
    # Fetch the LSP details based on the 'user' field in the LSP model
    lsp_user = get_object_or_404(LSP, user=user)
    print("e3")
    context = {
        'user': user,
        'user_profile': user_profile,
        'lsp_user': lsp_user,
    }
    print("e4")
    
    return render(request, 'admin/admin_lsp_profile.html', context)
   
   
 
def clients_users_list(request):
    profile=Profile.objects.filter(is_service_provider=False)
    context={
        'profile':profile,
    }
    return render(request,'admin/clients_users_list.html',context)
    