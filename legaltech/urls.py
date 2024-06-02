"""legaltech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static
from home import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path("lsp/",include('lsp.urls',namespace='lsp')),
    path("client/",include('client.urls',namespace="client")),
    path("admin_app/",include('admin_app.urls',namespace="admin_app")),
    path("accounts/",include('accounts.urls',namespace="accounts")),
    
    path("",views.home,name="home"),
    # path("home",views.home,name="home"), 
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("service",views.service,name="service"),
    path("chatbot",views.home_chatbot,name="chatbot"),
    path("test",views.test,name="test"),
    path('law_directory',views.law_directory,name="law_directory"),
    
    
    path('chat_users_list',views.chat_users_list,name="chat_users_list"),
    # path("room/<str:friendusername>",views.room,name='room'),
    # path("checkview/<str:friendusername>/",views.checkview,name='checkview'),
    # path("send",views.send,name='send'),
    # path("getmessages/<str:friend>",views.getmessages,name='getmessages'),
    # path("friends",views.friends,name='friends'),
    # path("removefriend",views.removefriend,name='removefriend'),
    # path("uploadfiles/<str:friend>",views.uploadfiles,name='uploadfiles'),
    # path('chat_friends',views.chat_friends,name='chat_friends'),
    
    ##
    path("about",views.about,name="about"),
    path("affidavit",views.affidavit,name="affidavit"),
    path('affdoc',views.affdoc,name="affdoc"),
    path("notary",views.notary,name="notary"),
    path('notdoc',views.notdoc,name="notdoc"),
    path('landnot',views.landnot,name="landnot"),
    path('housenot',views.housenot,name='housenot'),
    path('rentalnot',views.rentalnot,name='rentalnot'),
    path("agreement",views.agreement,name="agreement"),
    path('partnership_doc',views.partnership_doc,name="partnership_doc"),
    path('payment_doc',views.payment_doc,name="payment_doc"),
    path('lease_doc',views.lease_doc,name="lease_doc"),
    path("help",views.help,name="help"),
    
]
    
    
   

      

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

# urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)





admin.site.site_header="Legal Tech Web App"
# admin.site.site_title=""
admin.site.index_title="Welcome to the Legal Tech Web App"



 # path("lsp_base",views.lsp_base,name="lsp_base"),
    # path("login",views.login,name="login"),
    # path("admin_base",views.admin_base,name="admin_base"),
    # path("home",include('home.urls',namespace="home")),
    #registration's
   
#    path("user_registration",views.user_registration,name="user_registration"),
    
    # login's
    # path('user_login',views.user_login,name="user_login"),
    # path("logout",views.user_logout,name="logout"),
    # path("user_login",views.user_login,name="user_login"),

    
    #dashboard's