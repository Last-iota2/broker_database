from django.db import transaction
from django.db.models.functions import Now
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from . import models

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
            print(self.instance)
            if self.instance is not None:
                setting = self.update(self.instance, validated_data)
            else:
                print(self.instance)
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


    