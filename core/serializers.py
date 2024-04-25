from django.db import transaction
from django.db.models.functions import Now
from django.utils.timezone import datetime
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from . import models
import zoneinfo

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'serial_number','password']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username']


class ThresholdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Thresholds
        exclude = ['setting', 'id']


class TestConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestConfiguration
        exclude = ['setting', 'id']


class FiberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fiber
        exclude = ['setting', 'id']


class LinkDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LinkDefinition
        exclude = ['setting', 'id']


class ManualTestSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ManualTestSettings
        exclude = ['setting', 'id']


class AllSettingsSerializers(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()
    manual_test_settings = ManualTestSettingsSerializer()
    link_definition = LinkDefinitionSerializer()
    fiber = FiberSerializer()
    test_configuration = TestConfigurationSerializer()
    thresholds = ThresholdsSerializer(many=True)

    class Meta:
        model = models.AllSettings
        # fields = "__all__"
        exclude = ['changed', 'last_updated', 'user']

    
    def save(self, **kwargs):
        with transaction.atomic():
            validated_data = {**self.validated_data, **kwargs}
            user_id = models.User.objects.all().get(id=self.context["id"])
            try:
                self.instance = models.AllSettings.objects.get(user=user_id)
            except:
                self.instance = None
            if self.instance is not None:
                setting = self.update(self.instance, validated_data)
            else:
                setting = models.AllSettings.objects.create(user=user_id, changed=False)
                models.ManualTestSettings.objects.create(setting=setting, **validated_data['manual_test_settings'])
                models.Fiber.objects.create(setting=setting, **self.validated_data['fiber'])
                models.LinkDefinition.objects.create(setting=setting, **self.validated_data['link_definition'])
                models.TestConfiguration.objects.create(setting=setting, **self.validated_data['test_configuration'])
                [models.Thresholds.objects.create(**{"setting": setting, **item}) for item in self.validated_data["thresholds"]]
            return setting

    def update(self, instance, validated_data):
        with transaction.atomic():
            setting = models.AllSettings.objects.filter(user=self.context['id']).update(last_updated=Now())
            models.Fiber.objects.filter(setting=self.context['id']).update(**validated_data['fiber'])
            models.ManualTestSettings.objects.filter(setting=self.context['id']).update(**validated_data['manual_test_settings'])
            models.LinkDefinition.objects.filter(setting=self.context['id']).update(**validated_data['link_definition'])
            models.TestConfiguration.objects.filter(setting=self.context['id']).update(**validated_data['test_configuration'])
            [models.Thresholds.objects.filter(setting=self.context['id'],thresholds_format_name=item["thresholds_format_name"]).update(**item) for item in self.validated_data["thresholds"]]

            return instance


class ActiveSerializer(serializers.ModelSerializer):
    has_permision_to_work = serializers.BooleanField(read_only=True)
    class Meta:
        model = models.Active
        fields = ["automatic", 'has_permision_to_work']

    def save(self, **kwargs):
        # print(self.validated_data.items())
        with transaction.atomic():
            validated_data = {**self.validated_data, **kwargs}
            user_id = models.User.objects.all().get(id=self.context['id'])
            try:
                self.instance = models.Active.objects.get(user=user_id)
            except:
                self.instance = None
            if self.instance is not None:
                active = self.update(self.instance, validated_data)
            else:
                active = models.Active.objects.create(user=user_id, **validated_data)
            return active

    def update(self, instance, validated_data):
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save(update_fields=["automatic", 'last_check'])
            return instance


class ActiveAdminSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    is_active = serializers.SerializerMethodField()

    def get_is_active(self, active=models.Active):  
        if (datetime.now(tz=zoneinfo.ZoneInfo("UTC"))- active.last_check).total_seconds() > 100:
            return False
        return True


    class Meta:
        model = models.Active
        fields = ['id' ,'user' ,"automatic", 'is_active', 'has_permision_to_work']

    def save(self, **kwargs):
        with transaction.atomic():
            validated_data = {**self.validated_data, **kwargs}
            user_id = models.User.objects.all().get(id=self.context['id'])
            try:
                self.instance = models.Active.objects.get(user=user_id)
            except:
                self.instance = None
            if self.instance is not None:
                active = self.update(self.instance, validated_data)
            else:
                active = models.Active.objects.create(user=user_id, **validated_data)
            return active


class UpdateActiveAdminSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    is_active = serializers.SerializerMethodField()

    def get_is_active(self, active=models.Active):  
        return (datetime.now(tz=zoneinfo.ZoneInfo("UTC"))- active.last_check).total_seconds() < 100

    class Meta:
        model = models.Active
        fields = ['id' ,'user' ,"automatic" ,'is_active' ,'has_permision_to_work']

    def save(self, **kwargs):
        with transaction.atomic():
            validated_data = {**self.validated_data, **kwargs}
            self.instance = models.Active.objects.all().get(id=self.context["user_id"])
            active = self.update(self.instance, validated_data)
            return active

    def update(self, instance, validated_data):
        with transaction.atomic():
            date = instance.last_check
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            print(validated_data.items())
            instance.save(update_fields=["automatic", 'has_permision_to_work'])
            return instance