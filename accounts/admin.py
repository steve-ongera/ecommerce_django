from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account

# here I'm specifing the fields I want to see in the Accounts table in Django admin, so I can see more than only the email
class AccountAdmin(UserAdmin):
    list_display = ("email", "username", "first_name", "last_name", "is_active", "last_login", "date_joined")
    list_display_links = ("email", "first_name", "last_name")
    readonly_fields = ("last_login", "date_joined")
    ordering = ("-date_joined",) # order the table ascending, depending on "date_joined"

    filter_horizontal=()
    list_filter = ()
    fieldsets = ()

# Register your models here.
admin.site.register(Account, AccountAdmin)