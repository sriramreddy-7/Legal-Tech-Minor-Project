from django.shortcuts import render ,redirect
from django.http import HttpResponse ,JsonResponse
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
from accounts.models import Profile,LSP,Message
from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
from accounts.models import Friend,Msg,Fileupload
from django.http import JsonResponse

from accounts.models import Chat

from django.utils import timezone
# from django.contrib.auth.decorators import login_required
# from .models import Message, UserProfile

def test(request):
    return render(request,'test.html')

def law_directory(request):
    service_provider_profiles = Profile.objects.filter(is_service_provider=True)
    context = {
        'service_provider_profiles': service_provider_profiles
    }

    # Render the law directory template with the context
    return render(request, 'law_directory/law_directory.html', context)

def home(request):
    profile=Profile.objects.filter(is_service_provider=True)
    context={
        'profile':profile,
    }
    return render(request,'home.html',context)

def service(request):
    return render(request,'service.html')

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been Activated!!")
        return redirect('home')
    else:
        return render(request,'activation_failed.html')
  
  
def homechat(request):
    return render(request, 'home.html')


def chat_users_list(request):
    user = get_object_or_404(User, username=request.user.username)
    user_profile = get_object_or_404(Profile, user=user)
    if user_profile.is_service_provider:
        user_det = User.objects.filter(profile__is_client=True)
        context={
        # 'user_profile':user_profile,
        # 'lsp_user':lsp_user,
        'user_det':user_det,
        }
        return render(request, 'chatapp/chat_users_list.html',context)
    elif user_profile.is_client:
        user_det=User.objects.filter(profile__is_service_provider=True)
        context={
        # 'user_profile':user_profile,
        'user_det':user_det,
        # 'client_user':client_user,
        }
        return render(request, 'chatapp/chat_users_list.html',context)
    else:
        return HttpResponse("Data Base Error")
 

def chatbot(request):
    chats = Chat.objects.filter(user=request.user.id)
    chats="admin"
    if request.method == 'POST':
        message = request.POST.get('message')
        # response = ask_openai(message)
        # admin_user = User.objects.get(username='admin')
        
        # chat = Chat(user=admin_user, message=message, response=response, created_at=timezone.now())
        # chat.save()
        message="This chat bot is temporarily out of service"
        response="This chat bot is temporarily out of service ! Sorry for inconvenience."
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot/chatbot.html', {'chats': chats})
    # return render(request, 'chatbot/chatbot.html')



def home_chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        # response = ask_openai(message)
        # admin_user = User.objects.get(username='admin')
        # chat = Chat(user=admin_user, message=message, response=response, created_at=timezone.now())
        # chat.save()
        message="This chat bot is temporarily out of service"
        response="This chat bot is temporarily out of service ! Sorry for inconvenience."
        return JsonResponse({'message': message, 'response': response})
    return render(request,'chatbot/home_chatbot.html')



def affidavit(request):
    if request.method =="POST":
        return redirect('affdoc')
        # return render(request,'affdoc.html')
    return render(request,'affidavit.html')


def affdoc(request):
    return render(request,'affdoc.html')

def notary(request):
    if request.method =="POST":
        purpose = request.POST.get('purpose1')
        if purpose == "land":
            return redirect('landnot')
        if purpose == "house":
            return redirect('housenot')
        if purpose == "rental":
            return redirect('rentalnot')
        # return render(request,'affdoc.html')
    return render(request,'notary.html')

def landnot(request):
    return render(request,'landnot.html')

def housenot(request):
    return render(request,'housenot.html')

def rentalnot(request):
    return render(request,'rentalnot.html')


def notdoc(request):
    return render(request,'notdoc.html')

def agreement(request):
    if request.method == "POST":
        purpose = request.POST.get('purpose1')
        if purpose == "partnership":
            return redirect('partnership_doc')
        if purpose == "payment":
            return redirect('payment_doc')
        if purpose == "lease":
            return redirect('lease_doc')
        # return render(request,'affdoc.html')
    return render(request,'agreement.html')


def partnership_doc(request):
    return render(request,'partnership_doc.html')

def payment_doc(request):
    return render(request,'payment_doc.html')

def lease_doc(request):
    return render(request,'lease_doc.html')

def help(request):
    return render(request,'help.html')
    
def about(request):
    return render(request,'about.html')