from django.contrib import admin

from accounts.models import Profile,LSP,Msg,Friend,Fileupload,Chat,Doubts,Connection,Appointment,AppointmentRequest,Availability,CaseDocument,Message,CustomMessage
# Register your models here.

admin.site.register(Profile)
admin.site.register(LSP)

admin.site.register(Msg)
# admin.site.register(Friend)
# admin.site.register(Fileupload)
# admin.site.register(Chat)
# admin.site.register(Doubts)
# admin.site.register(Connection)
admin.site.register(Appointment)
admin.site.register(AppointmentRequest)
admin.site.register(Availability)
# admin.site.register(CaseDocument)
admin.site.register(Message)
admin.site.register(CustomMessage)
