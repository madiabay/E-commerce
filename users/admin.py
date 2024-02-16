from django.contrib import admin
from . import models


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'email',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'email')}),
    )

    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(models.CustomUser, CustomUserAdmin)
