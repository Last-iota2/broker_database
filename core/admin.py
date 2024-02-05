from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'username', 'serial_number', 'is_active']
    list_display_links = ['username']
    list_editable = ['serial_number', 'is_active']
    search_fields = ['serial_number__icontains', 'username']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'serial_number', 'password1', 'password2'),
        }),
    )


class TestConfigurationInline(admin.StackedInline):
    model = TestConfiguration


class ThresholdsInline(admin.StackedInline):
    radio_fields = {"thresholds_format_name": admin.HORIZONTAL, 'thresholds_type': admin.HORIZONTAL}
    model = Thresholds
    max_num = 3
    min_num = 3


class LinkDefinitionInline(admin.StackedInline):
    model = LinkDefinition


class FiberInline(admin.StackedInline):
    model = Fiber


class ManualTestSettingsInline(admin.StackedInline):
    model = ManualTestSettings


@admin.register(AllSettings)
class SettingsAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['user', 'changed', 'last_updated']
    list_select_related = ['user', 'test_configuration',
                            'manual_test_settings', 'fiber', 'link_definition']
    list_filter = ['changed', 'last_updated']
    readonly_fields = ['changed']
    inlines = [TestConfigurationInline, ManualTestSettingsInline, 
                FiberInline, LinkDefinitionInline, ThresholdsInline]
    search_fields = ['user']

    def save_model(self, request, obj, form, change):
        obj.changed = True
        super().save_model(request, obj, form, change)
