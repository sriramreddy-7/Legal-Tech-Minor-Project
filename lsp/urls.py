from django.urls import path
from  lsp import views
from django.conf import settings
from django.conf.urls.static import static

app_name="lsp"


urlpatterns=[
    
    path("lsp_dashboard",views.lsp_dashboard,name="lsp_dashboard"),
    path("lsp_profile/<str:username>/",views.lsp_profile,name="lsp_profile"),
    path('lsp_chat_list',views.lsp_chat_list,name="lsp_chat_list"),
    path('lsp_chat_ui/<str:username>',views.lsp_chat_ui,name="lsp_chat_ui"),
    path("send",views.send,name='send'),
    path("checkview",views.checkview,name='checkview'),
    path("getmessages/<str:friend>",views.getmessages,name='getmessages'),
    path('lsp_appointments',views.lsp_appointments,name="lsp_appointments"),
    path('<str:request_id>/update_appointment_status',views.update_appointment_status,name="update_appointment_status"),
    path("chat_room",views.chat_room,name="chat_room"),
    path('chat/<int:receiver_id>/', views.chat_interface, name='chat_interface'),
    # path("lsp_login",views.lsp_login,name="lsp_login"),
    # path('lsp_registration',views.lsp_registration,name="lsp_registration"),
    # path('users_list',views.users_list,name="users_list"),
    # path("lsp_dashboard",views.lsp_dashboard,name="lsp_dashboard"),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)