from django.contrib import admin
from .models import List,Subcriber,Email,EmailTracking,Sent
# Register your models here.

class EmailTrackingAdmin(admin.ModelAdmin):
    list_display = ['email', 'subcriber', 'open_at', 'clicked_at']

admin.site.register(List)
admin.site.register(Subcriber)
admin.site.register(Email)
admin.site.register(EmailTracking,EmailTrackingAdmin)
admin.site.register(Sent)
