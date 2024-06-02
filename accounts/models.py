from django.db import models
from django.contrib.auth.models import AbstractUser, User
from datetime import datetime

class Profile(models.Model):
    def upload_path(instance, filename):
        new_filename = f"{instance.user}.png"
        return f"LSP/{new_filename}"

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()
    age = models.IntegerField(blank=True)
    profile_picture = models.ImageField(upload_to=upload_path, blank=True)
    bio = models.TextField(blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    address_line = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state_province = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    account_creation_date = models.DateTimeField(auto_now_add=True)
    last_login_date = models.DateTimeField(auto_now=True)
    account_type = models.CharField(max_length=20, default='client')
    is_client = models.BooleanField(default=False)
    is_service_provider = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)


class LSP(models.Model):
    def upload_path(instance, filename):
        new_filename = f"{instance.user}.png"
        return f"LSP/{new_filename}"

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    lsp_type = models.CharField(max_length=100)
    signature = models.ImageField(upload_to=upload_path, blank=True)
    enrollment_number = models.CharField(max_length=50, unique=True)
    bar_council_practicing_certificate = models.FileField(upload_to=upload_path, blank=True)
    enrollment_year = models.IntegerField()
    university_llb_completed = models.CharField(max_length=100)
    llb_passout_year = models.IntegerField()

    def __str__(self):
        return str(self.user.username)


class Message(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Msg(models.Model):
    sender = models.CharField(max_length=120)
    receiver = models.CharField(max_length=120)
    message = models.CharField(max_length=1000000)
    encrypted_message = models.BinaryField(default=b'')
    date = models.DateTimeField(default=datetime.now, blank=True)
    file_status = models.BooleanField(default=False)
    file_name = models.CharField(max_length=1000000, default=None, null=True)


class Friend(models.Model):
    user = models.CharField(max_length=120)
    friend = models.CharField(max_length=120)
    nickname = models.CharField(max_length=120)


class Fileupload(models.Model):
    file = models.FileField(upload_to='uploaded_files/')


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'


class Doubts(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(null=False)
    type_of_doubt = models.CharField(max_length=100, null=False)
    message = models.TextField(null=False)

    def _str_(self):
        return f"{self.first_name} {self.last_name}"


class Connection(models.Model):
    lsp_username = models.CharField(max_length=100)
    client_username = models.CharField(max_length=100)
    message_type = models.CharField(max_length=50)
    case_description = models.TextField()

    def __str__(self):
        return f"{self.lsp_username} - {self.client_username}"


class Appointment(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_appointments')
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provider_appointments')
    date_time = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment {self.id} - {self.client.username} with {self.service_provider.username} on {self.date_time}"


class Availability(models.Model):
    service_provider = models.OneToOneField(User, on_delete=models.CASCADE)
    monday_start = models.TimeField(null=True, blank=True)
    monday_end = models.TimeField(null=True, blank=True)
    tuesday_start = models.TimeField(null=True, blank=True)
    tuesday_end = models.TimeField(null=True, blank=True)
    wednesday_start = models.TimeField(null=True, blank=True)
    wednesday_end = models.TimeField(null=True, blank=True)
    thursday_start = models.TimeField(null=True, blank=True)
    thursday_end = models.TimeField(null=True, blank=True)
    friday_start = models.TimeField(null=True, blank=True)
    friday_end = models.TimeField(null=True, blank=True)
    saturday_start = models.TimeField(null=True, blank=True)
    saturday_end = models.TimeField(null=True, blank=True)
    sunday_start = models.TimeField(null=True, blank=True)
    sunday_end = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"Availability for {self.service_provider.username}"


class AppointmentRequest(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provider_requests')
    date_time = models.DateTimeField()
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    client_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    occupation = models.CharField(max_length=100)
    case_type = models.CharField(max_length=100)
    case_info = models.TextField()

    def __str__(self):
        return f"Appointment request from {self.client.username} to {self.service_provider.username} on {self.date_time}"

   

from django.core.validators import FileExtensionValidator

class CaseDocument(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.FileField(upload_to='case_documents/', validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    shared_with_lsp = models.BooleanField(default=False)
    is_accessible = models.BooleanField(default=False)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Document for {self.client.username} uploaded at {self.uploaded_at}"

    def grant_access_to_lsp(self):
        self.shared_with_lsp = True
        self.save()

    def revoke_access_to_lsp(self):
        self.shared_with_lsp = False
        self.save()


class CustomMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', default=None)
    content = models.TextField()
    file = models.FileField(upload_to='message_attachments/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     ordering = ['timestamp']
        
    def __str__(self):
        if self.receiver:
            return f"From {self.sender.username} to {self.receiver.username}: {self.content}"
        else:
            return f"To {self.sender.username}: {self.content}"