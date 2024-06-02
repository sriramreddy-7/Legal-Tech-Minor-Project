from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from legaltech import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth import authenticate, login, logout
from accounts.tokens import generate_token
from accounts.models import Profile,LSP,Msg,Friend,Fileupload,Chat,Doubts,Connection,Appointment,AppointmentRequest,Availability
from django.utils import timezone
from django.shortcuts import get_object_or_404
from . import views
from django.contrib import messages
from django.http import JsonResponse
from accounts.models import Profile,LSP,Doubts,Availability, Appointment, AppointmentRequest,Message,CustomMessage
from django.shortcuts import get_object_or_404
from accounts import views
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages as django_messages




def lsp_dashboard(request):
    
    chat_user = User.objects.all()

    # Fetch the current user
    user = get_object_or_404(User, username=request.user.username)

    # Fetch the user profile based on the 'user' field in the Profile model
    user_profile = get_object_or_404(Profile, user=user)

    # Fetch the LSP details based on the 'user' field in the LSP model
    lsp_user = get_object_or_404(LSP, user=user)

    # Fetch today's appointments
    today = timezone.now().date()
    today_appointments = Appointment.objects.filter(date_time__date=today)

    # Fetch total clients
    total_clients = len(set(Appointment.objects.values_list('client', flat=True)))

    # Fetch upcoming appointments (excluding today's appointments)
    upcoming_appointments = Appointment.objects.filter(date_time__gt=today).exclude(date_time__date=today)

    # Fetch past appointments
    past_appointments = Appointment.objects.filter(date_time__lt=today)

    context = {
        'user': user,
        'user_profile': user_profile,
        'lsp_user': lsp_user,
        'chat_user': chat_user,
        'today_appointments': today_appointments,
        'total_clients': total_clients,
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
    }
    return render(request, 'lsp/lsp_dashboard.html', context)


def lsp_profile(request,username):
    user = get_object_or_404(User, username=username)
    print("e1")
    # Fetch the user profile based on the 'user' field in the Profile model
    user_profile = get_object_or_404(Profile, user=user)
    print("e1")
    # Fetch the LSP details based on the 'user' field in the LSP model
    lsp_user = get_object_or_404(LSP, user=user)
    print("e1")
    context = {
        'user': user,
        'user_profile': user_profile,
        'lsp_user': lsp_user,
    }
    return render(request,'lsp/lsp_profile.html',context)


def lsp_chat_list(request):
    chat_user=User.objects.all()
    context={
        'chat_user':chat_user,
    }
    for i in chat_user:
        print(f"{i.username}")
    return render(request,'lsp/lsp_chat_list.html',context)


def lsp_chat_ui(request,username):
    return render(request,'lsp/lsp_chat_ui.html',{'friend':username})



def send(request):
    # if request.user.is_anonymous or request.user.is_active==False:
    #     return redirect('/accounts/login')
    if request.method == 'POST':
        sender=request.POST.get("username")
        receiver=request.POST.get("friend")
        message=request.POST.get("message")
        message=message.strip()
        if (message == "") or (request.user.username != sender):
            return redirect('/lsp/lsp_chat_ui/'+receiver)
       
        newmessage=Msg(sender=sender,receiver=receiver,message=message)
        newmessage.save()

        return HttpResponse("message sent")

    return redirect('/')

def getmessages(request,friend):
    # if request.user.is_anonymous or request.user.is_active==False:
    #     return redirect('/accounts/login')
    # if User.objects.filter(username=friend).exists()==False:
    #     return redirect('/')
    # if request.user.username==friend:
    #     return redirect('/')
    all_messages=Msg.objects.all().filter(sender=request.user).filter(receiver=friend)|Msg.objects.all().filter(sender=friend).filter(receiver=request.user)

    return JsonResponse({"messages":list(all_messages.values())})



def checkview(request):
    if request.method == 'POST':
        friendusername =request.POST.get("friendusername")
        if request.user.username==friendusername:
            return redirect('/')
        if User.objects.filter(username=friendusername).exists():
            return redirect('/lsp/lsp_chat_ui/'+friendusername)
        else:
            return redirect('/')
    
    return redirect('/')





def lsp_appointments(request):
    lsp_appointment_requests = AppointmentRequest.objects.filter(service_provider=request.user)
    user = get_object_or_404(User, username=request.user.username)

    # Fetch the user profile based on the 'user' field in the Profile model
    user_profile = get_object_or_404(Profile, user=user)

    # Fetch the LSP details based on the 'user' field in the LSP model
    lsp_user = get_object_or_404(LSP, user=user)
    context={
        'lsp_appointment_requests':lsp_appointment_requests,
        'user': user,
        'user_profile': user_profile,
        'lsp_user': lsp_user,
    }
    return render(request, 'lsp/lsp_appointments.html', context)

def update_appointment_status(request, request_id):
    if request.method == 'POST':
        try:
            appointment_request = AppointmentRequest.objects.get(id=request_id)
            if appointment_request and appointment_request.service_provider == request.user:
                status = request.POST.get('status')
                if status == 'approve':
                    appointment_request.is_accepted = True
                    appointment_request.save()
                    appointment = Appointment.objects.create(
                        client=appointment_request.client,
                        service_provider=appointment_request.service_provider,
                        date_time=appointment_request.date_time,
                        is_confirmed=True
                    )
                    appointment_request.is_accepted = True
                    appointment_request.save()
                    appointment.is_confirmed = True
                    appointment.save()
                    messages.success(request, 'Appointment request approved successfully.')
                elif status == 'reject':
                    appointment_request.is_rejected = True
                    appointment_request.save()
                    messages.success(request, 'Appointment request rejected successfully.')
                elif status == 'waiting':
                    messages.success(request, 'Appointment request status kept waiting.')
                else:
                    messages.error(request, 'Invalid status option.')
            else:
                messages.error(request, 'Failed to update appointment status.')
        except AppointmentRequest.DoesNotExist:
            messages.error(request, 'Appointment request does not exist.')
        except Exception as e:
            messages.error(request, f'Failed to update appointment status: {str(e)}')
    return redirect('lsp:lsp_appointments')



def chat_room(request):
    # Fetch all profiles
    profiles = Profile.objects.all()

    # Filter service providers
    service_providers = [profile.user for profile in profiles if profile.is_service_provider]

    # Fetch appointment confirmed clients
    confirmed_clients = Appointment.objects.filter(service_provider=request.user, is_confirmed=True)
    print(confirmed_clients, service_providers, request.user, request.user.username,profiles)
    user = get_object_or_404(User, username=request.user.username)

    # Fetch the user profile based on the 'user' field in the Profile model
    user_profile = get_object_or_404(Profile, user=user)

    # Fetch the LSP details based on the 'user' field in the LSP model
    lsp_user = get_object_or_404(LSP, user=user)
    context = {
        'service_providers': service_providers,
        'confirmed_clients': confirmed_clients,
        'user': user,
        'user_profile': user_profile,
        'lsp_user': lsp_user,
    }
    return render(request, 'lsp/chat_room.html', context)


def chat_interface(request, receiver_id):
    if request.method == 'POST':
        # Process the sent message
        content = request.POST.get('content', '')
        receiver = get_object_or_404(User, id=receiver_id)
        sender = request.user

        # Create and save the message
        message = CustomMessage.objects.create(sender=sender, receiver=receiver, content=content)

        # Optionally, you can add additional logic here, like sending notifications
        
        return redirect('lsp:chat_interface', receiver_id=receiver_id)

    # Retrieve messages
    receiver = get_object_or_404(User, id=receiver_id)
    messages = CustomMessage.objects.filter(sender=request.user, receiver=receiver) | CustomMessage.objects.filter(sender=receiver, receiver=request.user)

    return render(request, 'lsp/chat_interface.html', {'receiver': receiver, 'messages': messages})