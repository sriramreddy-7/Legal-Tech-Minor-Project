from django.urls import path
from  . import views
from django.conf import settings
from django.conf.urls.static import static

app_name="client"


urlpatterns=[
     path("client_dashboard",views.client_dashboard,name="client_dashboard"),
     path("client_lsp_view",views.client_lsp_view,name="client_lsp_view"),
     path('client_lsp_profile/<str:username>/',views.client_lsp_profile,name="client_lsp_profile"),
     path('client_contact',views.client_contact,name="client_contact"),
     path('client_lsp_consult',views.client_lsp_consult,name="client_lsp_consult"),
     path('client_law_directory',views.client_law_directory,name="client_law_directory"),
     path("/<str:id>/client_lsp_consult",views.client_lsp_consult,name="client_lsp_consult"),
     path("client_appointments",views.client_appointments,name="client_appointments"),
     path('custom_message/', views.custom_message, name='custom_message'),
     # path('chat/<int:receiver_id>/', views.chat_view, name='chat'), 
     path("chat_room",views.chat_room,name="chat_room"),
     path('chat/<int:receiver_id>/', views.chat_interface, name='chat_interface'),
     path('send_message/', views.send_message, name='send_message'),
     path('fetch_messages/', views.fetch_messages, name='fetch_messages'),

    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)