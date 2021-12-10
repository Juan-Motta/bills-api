from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from apps.clients.models import Client


class ClientCreationForm(forms.ModelForm):
    """A form for creating new clients. Includes all the required fields, plus a repeated password."""

    password_1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password_2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = Client
        fields = (
            'first_name',
            'last_name',
            'email',
            'document'
        )

    def clean_password2(self):
        # Check that the two password entries match
        password_1 = self.cleaned_data.get("password_1")
        password_2 = self.cleaned_data.get("password_2")
        if password_1 and password_2 and password_1 != password_2:
            raise ValidationError("Passwords don't match")
        return password_2

    def save(self, commit=True):
        # Save the provided password in hashed format
        client = super().save(commit=False)
        client.set_password(self.cleaned_data["password_1"])
        if commit:
            client.save()
        return client


class ClientChangeForm(forms.ModelForm):
    """A form for updating clients. Includes all the fields on the client, but replaces the password field with admin's disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Client
        fields = (
            'email',
            'first_name',
            'last_name',
            'document',
            'is_staff',
        )


class ClientAdmin(BaseUserAdmin):

    # The forms to add and change client instances
    form = ClientChangeForm
    add_form = ClientCreationForm

    # The fields to be used in displaying the Client model. These override the definitions on the base UserAdmin that reference specific fields on auth.User.
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'document',
        'is_staff',
        'is_active'
    )

    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
         'fields': ('first_name', 'last_name', 'document',)
         }),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'document', 'password1', 'password2'),
        }),
    )

    search_fields = ('email',)

    ordering = ('email',)

    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(Client, ClientAdmin)

# unregister the Group model from admin.
admin.site.unregister(Group)
