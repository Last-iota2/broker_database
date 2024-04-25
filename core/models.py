from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class User(AbstractUser):
    serial_number = models.CharField(max_length=255, unique=True)


class AllSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)
    # manual_test_setting = models.OneToOneField(ManualTestSettings, on_delete=models.CASCADE)
    # link_definition = models.OneToOneField(LinkDefinition, on_delete=models.CASCADE)
    # fiber = models.OneToOneField(Fiber, on_delete=models.CASCADE)
    # test_configuration = models.OneToOneField(TestConfiguration, on_delete=models.CASCADE)
    # thresholds = models.ForeignKey(Thresholds, on_delete=models.PROTECT)
    changed = models.BooleanField()
    last_updated = models.DateTimeField(auto_now=True)


class TestConfiguration(models.Model):
    # user = models.OneToOneField(User, on_delete=models.PROTECT)
    setting = models.OneToOneField(AllSettings, on_delete=models.CASCADE, related_name="test_configuration") 
    number_of_ports = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    port_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    wavelength = models.PositiveBigIntegerField()
    pulsewidth = models.PositiveBigIntegerField()
    range = models.PositiveBigIntegerField()
    test_interval_hours = models.PositiveSmallIntegerField()
    test_interval_minutes = models.PositiveSmallIntegerField()
    duration = models.PositiveIntegerField()
    # last_updated = models.DateTimeField(auto_now=True)
    # changed = models.BooleanField()


class LinkDefinition(models.Model):
    # user = models.OneToOneField(User, on_delete=models.PROTECT)
    setting = models.OneToOneField(AllSettings, on_delete=models.CASCADE, related_name="link_definition") 
    ior = models.FloatField()
    reflectance = models.CharField(max_length=255)
    splice_loss = models.FloatField()
    end_of_fiber = models.PositiveBigIntegerField()
    # last_updated = models.DateTimeField(auto_now=True)
    # changed = models.BooleanField()


class Fiber(models.Model):
    # user = models.OneToOneField(User, on_delete=models.PROTECT)
    setting = models.OneToOneField(AllSettings, on_delete=models.CASCADE, related_name="fiber") 
    location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    cable_type = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, default="no comment")
    operator = models.CharField(max_length=255)
    cable_sn = models.CharField(max_length=255)
    autosave = models.BooleanField()
    # last_updated = models.DateTimeField(auto_now=True)
    # changed = models.BooleanField()


class ManualTestSettings(models.Model):
    # user = models.OneToOneField(User, on_delete=models.PROTECT)
    setting = models.OneToOneField(AllSettings, on_delete=models.CASCADE, related_name="manual_test_settings") 
    wavelength = models.PositiveBigIntegerField()
    pulsewidth = models.PositiveBigIntegerField()
    range = models.PositiveBigIntegerField()
    port_name = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    duration = models.PositiveIntegerField()
    # last_updated = models.DateTimeField(auto_now=True)
    # changed = models.BooleanField()


class Thresholds(models.Model):
    THRESHOLDS_FORMAT_NORMAL = 'n'
    THRESHOLDS_FORMAT_FINE = 'f'
    THRESHOLDS_FORMAT_CORS = 'c'
    THRESHOLDS_FORMAT_CHOICES = [
        (THRESHOLDS_FORMAT_NORMAL, 'normal'),
        (THRESHOLDS_FORMAT_FINE, 'fine'),
        (THRESHOLDS_FORMAT_CORS, 'cors' )
    ]
    THRESHOLD_TYPE_MINOR = 'mi'
    THRESHOLD_TYPE_MAJOR = 'ma'
    THRESHOLD_TYPE_CHOICES = [
        (THRESHOLD_TYPE_MINOR, 'minor'),
        (THRESHOLD_TYPE_MAJOR, 'major')
    ]
    # user = models.ForeignKey(User, on_delete=models.PROTECT) 
    setting = models.ForeignKey(AllSettings, on_delete=models.CASCADE, related_name="thresholds") 
    wavelength = models.PositiveBigIntegerField()
    thresholds_format_name = models.CharField(
        max_length=1,
        choices=THRESHOLDS_FORMAT_CHOICES,
        default='n'
    )
    thresholds_type = models.CharField(
        max_length=2,
        choices=THRESHOLD_TYPE_CHOICES,
        default='mi'   
    )
    splice_loss = models.CharField(max_length=255)
    connector = models.CharField(max_length=255)
    span_loss = models.CharField(max_length=255)
    reflectance = models.CharField(max_length=255)
    # last_updated = models.DateTimeField(auto_now=True)
    # changed = models.BooleanField()


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['setting', 'wavelength', 'thresholds_format_name'], name='unique together constraint')
        ]


class Active(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    automatic = models.BooleanField(blank=True)
    last_check = models.DateTimeField(auto_now=True)
    has_permision_to_work = models.BooleanField(default=False, blank=True)