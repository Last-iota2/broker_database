from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.timezone import datetime
from .models import *
import zoneinfo


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


@admin.register(Active)
class ActiveAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'last_check', 'is_active', 'has_permision_to_work']
    list_display_links = ["user"]
    list_editable = ['has_permision_to_work']
    readonly_fields = ['user']


    @admin.display(boolean=True)
    def is_active(self, active):
        return (datetime.now(tz=zoneinfo.ZoneInfo("UTC"))- active.last_check).total_seconds() < 100

    def save_model(self, request, obj, form, change):
        obj.save(update_fields=["automatic", 'has_permision_to_work'])