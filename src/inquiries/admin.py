from django.contrib import admin
from .models import Enquiry

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'email', 'subject', 'message')
