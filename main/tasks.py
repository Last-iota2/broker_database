from celery import shared_task
from . import models


@shared_task
def alarm_table(date, data):
    # alarm_tables = models.AlarmTable(date,**data)
    # alarm_tables.save()
    data['browse'] = models.Browser.objects.get(id=data['browse'])
    for alarm_table in data['alarm_table_data']:
        alarm_table = models.AlarmTable.objects.create(date=date, browse=data['browse'], **alarm_table)
    # models.AlarmTable(model_id)


# @shared_task
# def array_data(data):
#     data['browse'] = models.Browser.objects.get(id=data['browse'])
#     models.ArrayData.objects.create(**data)


# @shared_task
# def array_datas(data):
#     data['browse'] = models.Browser.objects.get(id=data['browse'])
#     for array_data in data['array_data']:
#         models.ArrayData.objects.create(browse=data['browse'],array_data=array_data)


@shared_task
def event_index_plot(data):
    data['browse'] = models.Browser.objects.get(id=data['browse'])
    models.EventIndexPlot.objects.create(**data)


@shared_task
def event_index_plots(data):
    data['browse'] = models.Browser.objects.get(id=data['browse'])
    for event_index_plot in data['event_index_plot']:
        models.EventIndexPlot.objects.create(browse=data['browse'],event_index_plot=event_index_plot)


@shared_task
def event_location_print(data):
    data['browse'] = models.Browser.objects.get(id=data['browse'])
    models.EventLocationPrint.objects.create(**data)


@shared_task
def event_location_prints(data):
    data['browse'] = models.Browser.objects.get(id=data['browse'])
    for event_location_print in data['event_location_print']:
        models.EventLocationPrint.objects.create(browse=data['browse'],event_location_print=event_location_print)


@shared_task
def alarm_list(data):
    data['browse'] = models.Browser.objects.get(id=data['browse'])
    models.AlarmList.objects.create(**data)


@shared_task
def alarm_lists(data):
    data['browse'] = models.Browser.objects.get(id=data['browse'])
    for alarm_list in data['alarm_list']:
        models.AlarmList.objects.create(browse=data['browse'],alarm_list=alarm_list)


@shared_task
def table_lists(data):
    data['browse'] = models.Browser.objects.get(id=data['browse'])
    for dicr in data['data']:
        models.TableList.objects.create(browse=data['browse'],**dicr)


