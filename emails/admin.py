from django.contrib import admin
from .models import List,Subcriber,Email,EmailTracking,Sent
# Register your models here.

admin.site.register(List)
admin.site.register(Subcriber)
admin.site.register(Email)
admin.site.register(EmailTracking)
admin.site.register(Sent)
