from django.db import models
from django.conf import settings


class Receiver(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.user)


class Browser(models.Model):
    receiver = models.ForeignKey(Receiver, on_delete=models.PROTECT)
    date = models.DateTimeField()
    link_wavelength = models.FloatField()    
    pulsewidth = models.FloatField()    
    fiber_length = models.FloatField()    
    duration = models.FloatField()    
    link_number = models.FloatField()    
    test_number = models.FloatField()    
    test_manual = models.FloatField()  

    def __str__(self):
        return str(self.date)


class AlarmList(models.Model):
    browse = models.ForeignKey(Browser,on_delete=models.PROTECT,null=False, blank=False)
    alarm_list = models.FloatField()


class ArrayData(models.Model):
    browse = models.ForeignKey(Browser,on_delete=models.PROTECT,null=False, blank=False)
    # array_data = models.FloatField()
    array_data = models.FileField(upload_to="array_data")

# class ArrayDataFiles(models.Model):
#     array_data = models.OneToOneField


class EventIndexPlot(models.Model):
    browse = models.ForeignKey(Browser,on_delete=models.PROTECT,null=False, blank=False)
    event_index_plot = models.FloatField()


class EventLocationPrint(models.Model):
    browse = models.ForeignKey(Browser,on_delete=models.PROTECT,null=False, blank=False)
    event_location_print = models.FloatField()


class TableList(models.Model):
    browse = models.ForeignKey(Browser,on_delete=models.PROTECT,null=False, blank=False)
    number = models.IntegerField()
    types = models.CharField(max_length=100)
    string_loc = models.FloatField()
    loss = models.FloatField()
    orl = models.FloatField()
    att = models.FloatField()
    section_loss = models.FloatField(default=0)
    length_shift = models.FloatField()


class XData(models.Model):
    browse = models.ForeignKey(Browser,on_delete=models.PROTECT,null=False, blank=False)
    x_data = models.FloatField()


class AlarmTable(models.Model):
    browse = models.ForeignKey(Browser,on_delete=models.PROTECT,null=False, blank=False)
    port_id = models.CharField(max_length=255)
    date = models.DateTimeField()
    link_number = models.CharField(max_length=255)
    count = models.IntegerField()


class EndFiber(models.Model):
    receiver = models.ForeignKey(Receiver, on_delete=models.PROTECT)
    port_id = models.CharField(max_length=255)
    end_fiber = models.FloatField()


class SystemAlarm(models.Model):
    browse = models.ForeignKey(Browser,on_delete=models.PROTECT,null=False, blank=False)
    port_id = models.CharField(max_length=255)
    creation = models.DateTimeField()
    last_update = models.DateTimeField()
    severity = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    alarm_type = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
