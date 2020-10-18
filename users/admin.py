from django.contrib import admin
from .models import User, Profile
from django.contrib.auth.admin import UserAdmin
from .forms import UserRegisterForm


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'name', 'is_staff')
    search_fields = ('name', 'email')
    ordering = ('-id',)

    add_form = UserRegisterForm
    add_form_template = 'admin/add_form.html'

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('name',)}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)