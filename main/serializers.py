from django.core.validators import MinValueValidator
from django.db import transaction
from rest_framework import serializers
from . import models
from . import tasks


class FloatListField(serializers.ListField):
    child = serializers.FloatField()


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

    def save(self, **kwargs):
        with transaction.atomic():
            validated_data = {**self.validated_data, **kwargs}
            alarm_list = models.AlarmList(**validated_data)
            validated_data['browse'] = validated_data['browse'].id
            tasks.alarm_list.delay(validated_data)
            # array_data = models.ArrayData.objects.create(**validated_data)

            return alarm_list
        

class AlarmListCreateSerializer(serializers.ModelSerializer):
    alarm_list = FloatListField()
    class Meta:
        model = models.AlarmList
        fields = "__all__"

    def save(self, **kwargs):
        with transaction.atomic():
            validated_data = {**self.validated_data, **kwargs}
            alarm_list = models.AlarmList(**validated_data)
            validated_data['browse'] = validated_data['browse'].id
            tasks.alarm_lists.delay(validated_data)
            # array_data = models.ArrayData.objects.create(**validated_data)

            return alarm_list
        

class ArrayDataViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArrayData
        fields = "__all__"

# class ArrayDataFileSerializer(serializers.ModelSerializer):


    # def save(self, **kwargs):
    #     with transaction.atomic():
    #         validated_data = {**self.validated_data, **kwargs}
    #         array_data = models.ArrayData(**validated_data)
    #         validated_data['browse'] = validated_data['browse'].id
    #         tasks.array_data.delay(validated_data)
    #         # array_data = models.ArrayData.objects.create(**validated_data)

    #         return array_data

# class ArrayDataSerializer(serializers.ModelSerializer):
#     array_data = FloatListField()
#     class Meta:
#         model = models.ArrayData
#         fields = "__all__"

#     def save(self, **kwargs):
#         with transaction.atomic():
#             validated_data = {**self.validated_data, **kwargs}
#             array_data = models.ArrayData(**validated_data)
#             validated_data['browse'] = validated_data['browse'].id
#             tasks.array_datas.delay(validated_data)
#             # array_data = models.ArrayData.objects.create(**validated_data)

#             return array_data


class EventIndexPlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventIndexPlot
        fields = "__all__"
    def save(self, **kwargs):
        with transaction.atomic():
            validated_data = {**self.validated_data, **kwargs}
            event_index_plot = models.EventIndexPlot(**validated_data)
            validated_data['browse'] = validated_data['browse'].id
            tasks.event_index_plot.delay(validated_data)
            # array_data = models.ArrayData.objects.create(**validated_data)

            return event_index_plot
        
class EventIndexPlotCreateSerializer(serializers.ModelSerializer):
    event_index_plot = FloatListField()
    class Meta:
        model = models.EventIndexPlot
        fields = "__all__"

    def save(self, **kwargs):
        with transaction.atomic():
            validated_data = {**self.validated_data, **kwargs}
            event_index_plot = models.EventIndexPlot(**validated_data)
            validated_data['browse'] = validated_data['browse'].id
            tasks.event_index_plots.delay(validated_data)
            # array_data = models.ArrayData.objects.create(**validated_data)

            return event_index_plot


class EventLocationPrintSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventLocationPrint
        fields = "__all__"

    def save(self, **kwargs):
        with transaction.atomic():
            validated_data = {**self.validated_data, **kwargs}
            event_location_print = models.EventLocationPrint(**validated_data)
            validated_data['browse'] = validated_data['browse'].id
            tasks.event_location_print.delay(validated_data)
            # array_data = models.ArrayData.objects.create(**validated_data)

            return event_location_print
        

class EventLocationPrintCreateSerializer(serializers.ModelSerializer):
    event_location_print = FloatListField()
    class Meta:
        model = models.EventLocationPrint
        fields = "__all__"

    def save(self, **kwargs):
        with transaction.atomic():
            validated_data = {**self.validated_data, **kwargs}
            event_location_print = models.EventLocationPrint(**validated_data)
            validated_data['browse'] = validated_data['browse'].id
            tasks.event_location_prints.delay(validated_data)
            # array_data = models.ArrayData.objects.create(**validated_data)

            return event_location_print

class BasicTableListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TableList
        exclude = ['browse']


class TableListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TableList
        fields = "__all__"

class TableListCreateSerializer(serializers.ModelSerializer):
    data = serializers.ListField(
        child=BasicTableListSerializer()
    )
    class Meta:
        model = models.TableList
        fields = ['browse',"data"]

    def save(self, **kwargs):
        with transaction.atomic():
            validated_data = {**self.validated_data, **kwargs}
            table_list = models.TableList(browse=validated_data['browse'])
            validated_data['browse'] = validated_data['browse'].id
            tasks.table_lists.delay(validated_data)
            # array_data = models.ArrayData.objects.create(**validated_data)

            return table_list



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


    # def save(self, **kwargs):
    #     with transaction.atomic():
    #         validated_data = {**self.validated_data, **kwargs}
    #         alarm_table = models.AlarmTable(date=self.context["date"], **validated_data)
    #         validated_data['browse'] = models.Browser.objects.filter(date=self.context["date"]).values()[0]['id']
    #         tasks.alarm_table.delay(self.context["date"], validated_data)
    #         return alarm_table
        

class BasicAlarmTableSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)
    class Meta:
        model = models.AlarmTable
        exclude = ['browse']

class AlarmTableCreateSerializer(serializers.ModelSerializer):
    alarm_table_data = serializers.ListField(
        child=BasicAlarmTableSerializer()
    )

    class Meta:
        model = models.AlarmTable
        fields = ['browse', 'alarm_table_data']


    def save(self, **kwargs):
        with transaction.atomic():
            validated_data = {**self.validated_data, **kwargs}
            validated_data['browse'] = models.Browser.objects.filter(date=self.context["date"]).values()[0]['id']
            alarm_table = models.AlarmTable(date=self.context["date"], browse=models.Browser.objects.get(id=validated_data['browse']))
            tasks.alarm_table.delay(self.context["date"], validated_data)
            return alarm_table