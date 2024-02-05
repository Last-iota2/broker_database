from django.core.validators import MinValueValidator
from django.db import transaction
from rest_framework import serializers
from . import models


class BrowserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Browser
        fields = "__all__"
        exlude = ['serial_number']


class CreateBrowserSerializer(serializers.ModelSerializer):
    receiver = serializers.StringRelatedField()
    class Meta:
        model = models.Browser
        fields = '__all__'


    def save(self, **kwargs):
        with transaction.atomic():
            validated_data = {**self.validated_data, **kwargs}
            receiver = models.Receiver.objects.get(id=self.context['id'])
            browser = models.Browser.objects.create(receiver=receiver, **validated_data)

            return browser
    

class AlarmListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AlarmList
        fields = "__all__"


class ArrayDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArrayData
        fields = "__all__"


class EventIndexPlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventIndexPlot
        fields = "__all__"


class EventLocationPrintSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventLocationPrint
        fields = "__all__"


class TableListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TableList
        fields = "__all__"


class XDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.XData
        fields = "__all__"


class EndFiberSerializer(serializers.ModelSerializer):
    receiver = serializers.StringRelatedField()
    class Meta:
        model = models.EndFiber
        fields = "__all__"

    def save(self, **kwargs):
        with transaction.atomic():
            validated_data = {**self.validated_data, **kwargs}
            receiver = models.Receiver.objects.get(id=self.context['id'])
            end_fiber = models.EndFiber.objects.create(receiver=receiver, **validated_data)

            return end_fiber


class SystemAlarmSerializer(serializers.ModelSerializer):
    creation = serializers.DateTimeField(read_only=True)
    last_update = serializers.DateTimeField(read_only=True)
    class Meta:
        model = models.SystemAlarm
        fields = "__all__"

    def save(self, **kwargs):
        with transaction.atomic():
            validated_data = {**self.validated_data, **kwargs}
            system_alarm = models.SystemAlarm.objects.create(creation=self.context["date"], last_update=self.context["date"], **validated_data)
            return system_alarm
        

class AlarmTableSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)
    class Meta:
        model = models.AlarmTable
        fields = "__all__"



    def save(self, **kwargs):
        with transaction.atomic():
            validated_data = {**self.validated_data, **kwargs}
            alarm_table = models.AlarmTable.objects.create(date=self.context["date"], **validated_data)
            return alarm_table