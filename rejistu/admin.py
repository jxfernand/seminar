# rejistu/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.core.mail import send_mail
from django.contrib import messages
from .models import Registrant, Institution, AccessPass


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'quota', 'access_pass_counter')
    # readonly_fields = ('access_pass_counter',)


@admin.register(AccessPass)
class AccessPassAdmin(admin.ModelAdmin):
    list_display = ('code', 'institution', 'is_used')
    list_filter = ('institution', 'is_used')
    readonly_fields = ('code',)


@admin.register(Registrant)
class RegistrantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'institution', 'access_pass', 'created_at')
    list_filter = ('institution', 'gender', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'access_pass')
    readonly_fields = ('access_pass', 'created_at', 'display_qr_code')

    # Customize the form in the admin panel
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'picture', 'gender', 'email', 'mobile_phone')
        }),
        ('Professional Information', {
            'fields': ('institution', 'position')
        }),
        ('Registration Details', {
            'fields': ('display_qr_code', 'access_pass', 'signature', 'created_at')
        }),
    )

    
    def save_model(self, request, obj, form, change):
        # Check if the institution has reached its quota
        if obj.institution.access_pass_counter >= obj.institution.quota:
            self.message_user(request, f"The institution {obj.institution.name} has reached its quota of {obj.institution.quota} access passes.", level='ERROR')
            return

            # Save the registrant (this will trigger the save method in the model)
        super().save_model(request, obj, form, change)

    def display_picture(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.picture.url)

    display_picture.short_description = 'Picture'


    def display_qr_code(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="100" height="100" />', obj.qr_code.url)
        return "No QR Code"

    display_qr_code.short_description = 'QR Code'

# ----


class RegistrantAdmin(admin.ModelAdmin):
    actions = ['send_reminder_email']

    def send_reminder_email(self, request, queryset):
        for registrant in queryset:
            send_mail(
                'Reminder: Your Registration Details',
                f'Hello {registrant.first_name}, your access pass is: {registrant.access_pass}',
                'admin@example.com',
                [registrant.email],
                fail_silently=False,
            )
        self.message_user(request, f'Reminder emails sent to {queryset.count()} registrants.', messages.SUCCESS)

    send_reminder_email.short_description = 'Send reminder email with access pass'
