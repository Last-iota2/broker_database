from django_filters.rest_framework import FilterSet
from . import models


class BrowserFilter(FilterSet):
    class Meta:
        model = models.Browser
        fields = {
            'date': ['exact']
        }

class ArrayDataFilter(FilterSet):
    class Meta:
        model = models.ArrayData
        fields = {
            'browse': ['exact']
        }


class AlarmListFilter(FilterSet):
    class Meta:
        model = models.AlarmList
        fields = {
            'browse': ['exact']
        }


class XDataFilter(FilterSet):
    class Meta:
        model = models.XData
        fields = {
            'browse': ['exact']
        }


class EventIndexPlotFilter(FilterSet):
    class Meta:
        model = models.EventIndexPlot
        fields = {
            'browse': ['exact']
        }


class EventLocationPrintFilter(FilterSet):
    class Meta:
        model = models.EventLocationPrint
        fields = {
            'browse': ['exact']
        }


class TableListFilter(FilterSet):
    class Meta:
        model = models.TableList
        fields = {
            'browse': ['exact']
        }


class AlarmTableFilter(FilterSet):
    class Meta:
        model = models.AlarmTable
        fields = {
            'browse': ['exact']
        }


class SystemAlarmFilter(FilterSet):
    class Meta:
        model = models.SystemAlarm
        fields = {
            'browse': ['exact']
        }


class EndFiberFilter(FilterSet):
    class Meta:
        model = models.EndFiber
        fields = {
            'receiver': ['exact']
        }