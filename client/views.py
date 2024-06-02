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
from accounts.models import Profile,LSP,Doubts,Availability, Appointment, AppointmentRequest,Message,CustomMessage
from django.shortcuts import get_object_or_404
from accounts import views
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages as django_messages


    
def client_dashboard(request):
    upcoming_appointments = Appointment.objects.filter(client=request.user, date_time__gte=timezone.now()).order_by('date_time')[:5]
    recent_messages = Message.objects.filter(user_profile=request.user).order_by('-timestamp')[:5]
    appointment_requests = AppointmentRequest.objects.filter(client=request.user).order_by('-created_at')[:5]
    user_profile = request.user.profile
    profile=Profile.objects.filter(user=request.user)

    context = {
        'upcoming_appointments': upcoming_appointments,
        'recent_messages': recent_messages,
        'appointment_requests': appointment_requests,
        'user_profile': user_profile,
        'profile': profile,
    }
    
    return render(request, 'client/client_dashboard.html', context)

def client_lsp_view(request):
    # user_det=User.objects.all()
    # profile_user=Profile.objects.all()
    # lsp_users= LSP.objects.all()
    lsp_users = LSP.objects.filter(lsp_type='Lawyer')
    profiles = Profile.objects.filter(user__in=lsp_users.values('user'))
    user_det = User.objects.filter(pk__in=lsp_users.values('user'))

    # profiles_with_lsps = []

    # for i in range(len(lsp_users)):
    #     profiles_with_lsps.append({
    #         'user_det': user_det[i],
    #         'lsp_user': lsp_users[i],
    #         'profile': profiles[i],
    #     })

    context = {
        'lsp_users':lsp_users,
    }
    
    return render(request,'client/client_lsp_view.html',context)


def client_lsp_profile(request,username):
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
    return render(request,'client/client_lsp_profile.html',context)



def client_contact(request):
    if request.method == 'POST':
        # Extract data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        type_of_doubt = request.POST.get('type_of_doubt')
        message = request.POST.get('message')
        print(first_name)
        print(last_name)
        print(email)
        print(type_of_doubt)
        print(message)
        # Validate data if necessary

        # Save data to the database
        d=Doubts.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            type_of_doubt=type_of_doubt,
            message=message
        )
        d.save()
        return render(request,'client/client_contact.html')
    
    return render(request,'client/client_contact.html')




def client_law_directory(request):
    service_provider_profiles = Profile.objects.filter(is_service_provider=True)
    context = {
        'service_provider_profiles': service_provider_profiles
    }
    return render(request,'client/client_law_directory.html',context)

# def upload_details(request, service_provider_id):
#     service_provider = User.objects.get(id=service_provider_id)
#     if request.method == 'POST':
#         client_name = request.POST.get('name')
#         phone_number = request.POST.get('mobile_number')
#         email = request.POST.get('email')
#         gender = request.POST.get('gender')
#         address = request.POST.get('address')
#         occupation = request.POST.get('occupation')
#         case_type = request.POST.get('case_type')
#         case_info = request.POST.get('case_info')
#         appointment_request = AppointmentRequest.objects.create(
#             client=request.user,
#             service_provider=service_provider,
#             client_name=client_name,
#             phone_number=phone_number,
#             email=email,
#             gender=gender,
#             address=address,
#             occupation=occupation,
#             case_type=case_type,
#             case_info=case_info
#         )
#         appointment_request.save()
#         return redirect('send_request_confirmation')
#     return render(request, 'upload_details.html', {'service_provider': service_provider})


def client_lsp_consult(request,id):
    lsp = get_object_or_404(LSP, enrollment_number=id)
    context = {
        "lsp": lsp,
    }
    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        occupation = request.POST.get('occupation')
        case_type = request.POST.get('case_type')
        case_info = request.POST.get('case_info')
        date_time=request.POST.get('date_time')

        # Save the appointment request
        appointment_request = AppointmentRequest.objects.create(
            client=request.user,
            service_provider=lsp.user,
            client_name=client_name,
            phone_number=phone_number,
            email=email,
            gender=gender,
            address=address,
            occupation=occupation,
            case_type=case_type,
            case_info=case_info,
            date_time=date_time
        )
        appointment_request.save()
        return redirect('client:client_appointments')
    return render(request, 'client/client_lsp_consult.html',context)


def client_appointments(request):
    appointment_requests = AppointmentRequest.objects.filter(client=request.user)
    context = {
        'appointment_requests': appointment_requests
    }
    
    return render(request, 'client/client_appointments.html', context)



def custom_message(request):
    user_messages = CustomMessage.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-timestamp')
    context = {
        'user_messages': user_messages
    }
    return render(request, 'client/chat_room.html', context)


def chat_room(request):
    # Assuming you have a way to determine the currently logged-in user
    current_user = request.user

    # Retrieve appointment requests accepted by the current client
    accepted_requests = AppointmentRequest.objects.filter(client=current_user, is_accepted=True)

    # Get the IDs of service providers who have accepted appointments
    accepted_service_provider_ids = accepted_requests.values_list('service_provider_id', flat=True)
    
    # Retrieve service providers based on the accepted service provider IDs
    service_providers = User.objects.filter(id__in=accepted_service_provider_ids)

    context = {
        'service_providers': service_providers
    }

    return render(request, 'client/chat_room.html', context)


# def chat_interface(request, receiver_id):
#     # Retrieve all messages involving the current user and the specified receiver
#     messages = CustomMessage.objects.filter(sender=request.user, receiver_id=receiver_id) | \
#                CustomMessage.objects.filter(sender_id=receiver_id, receiver=request.user)
    
#     # Retrieve the receiver object
#     receiver = User.objects.get(id=receiver_id)
    
#     context = {
#         'receiver': receiver,
#         'messages': messages
#     }
#     return render(request, 'client/chat_interface.html', context)


    

# def chat_interface(request, receiver_id):
#     if request.method == 'POST':
#         content = request.POST.get('content')
#         receiver = User.objects.get(id=receiver_id)
#         CustomMessage.objects.create(sender=request.user, receiver=receiver, content=content)
#         django_messages.success(request, 'Message sent successfully!')
#         print("Message sent successfully!-chat_interface")
#         context={
#             'receiver_id':receiver_id,
#             'receiver':receiver,
#         }
#         return redirect('client:chat_interface', context)  # Update this line
#     else:
#         # Retrieve all messages involving the current user
#         messages = CustomMessage.objects.filter(sender=request.user) | CustomMessage.objects.filter(receiver=request.user)
#         return render(request, 'client/chat_interface.html', {'messages': messages})
    
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        receiver_id = request.POST.get('receiver_id')
        receiver = User.objects.get(id=receiver_id)
        CustomMessage.objects.create(sender=request.user, receiver=receiver, content=content)
        django_messages.success(request, 'Message sent successfully!')
        print("Message sent successfully!-send_message")
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

# def chat_interface(request, receiver_id):
#     if request.method == 'POST':
#         content = request.POST.get('content')
#         receiver = User.objects.get(id=receiver_id)
#         CustomMessage.objects.create(sender=request.user, receiver=receiver, content=content)
#         django_messages.success(request, 'Message sent successfully!')
#         print("Message sent successfully!-chat_interface")
#         return JsonResponse({'success': True})
#     else:
#         # Retrieve all messages involving the current user
#         messages = CustomMessage.objects.filter(sender=request.user) | CustomMessage.objects.filter(receiver=request.user)
#         return render(request, 'client/chat_interface.html', {'messages': messages, 'receiver_id': receiver_id})
    
    
    
def fetch_messages(request):
    # Retrieve all messages involving the current user
    messages = CustomMessage.objects.filter(sender=request.user) | CustomMessage.objects.filter(receiver=request.user)
    data = {
        'messages': messages
    }
    return render(request, 'client/chat_interface.html', data)



def chat_interface(request, receiver_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        receiver = User.objects.get(id=receiver_id)
        CustomMessage.objects.create(sender=request.user, receiver=receiver, content=content)
        django_messages.success(request, 'Message sent successfully!')
        print("Message sent successfully!-chat_interface")
        return JsonResponse({'success': True})
    else:
        # Retrieve messages between the current user and the selected recipient
        sender_messages = CustomMessage.objects.filter(sender=request.user, receiver_id=receiver_id)
        receiver_messages = CustomMessage.objects.filter(sender_id=receiver_id, receiver=request.user)
        messages = sender_messages.union(receiver_messages).order_by('timestamp')
        
        return render(request, 'client/chat_interface.html', {'messages': messages, 'receiver_id': receiver_id})
