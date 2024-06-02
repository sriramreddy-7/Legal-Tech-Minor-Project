from django.urls import path
from  . import views
from django.conf import settings
from django.conf.urls.static import static


app_name="admin_app"


urlpatterns=[
    
    path('admin_lsp_profile/<str:username>/',views.admin_lsp_profile,name="admin_lsp_profile"),
    path("admin_dashboard",views.admin_dashboard,name="admin_dashboard"),
    path('verify_profile/<str:username>/',views.verify_profile,name="verify_profile"),
    path('users_list',views.users_list,name="users_list"),
    path("clients_users_list",views.clients_users_list,name="clients_users_list"),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)