from django.contrib import admin
from .models import *


@admin.register(Browser)
class BrowserAdmin(admin.ModelAdmin):
    list_display = ['date', 'receiver']
    list_select_related = ['receiver']
    search_fields = ['date', 'receiver__user__username']
    list_filter = ['date']