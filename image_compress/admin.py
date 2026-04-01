from django.contrib import admin
from .models import CompressImage
from django.utils.html import format_html
# Register your models here.

class CompressImageAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.compressed_image:
            return format_html(
                '<img src="{}" width="40" height="40" />',
                obj.compressed_image.url
            )
        return "No Image"

    thumbnail.short_description = "Preview"

    list_display = ('user', 'thumbnail', 'compressed_at')


admin.site.register(CompressImage, CompressImageAdmin)