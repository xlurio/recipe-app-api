from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Ingredient, Recipe, Tag, User
from .forms import UserChangeForm, UserCreationForm


# UserAdmin
class UserAdmin(BaseUserAdmin):
    '''The forms to add and change user instances'''
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be user in displaying the User model. These override the
    # definitions on the base UserAdmin that reference specific fields on
    # auth.User.
    list_display = ('email', 'name', 'is_staff',)
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    # add_fieldsets isn't a standard ModelAdmin attribute. UserAdmin overrides
    # get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password_one', 'password_two',),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Admin registers
admin.site.register(User, UserAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
