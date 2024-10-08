# Generated by Django 5.0.3 on 2024-04-17 06:38

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('serial_number', models.CharField(max_length=255, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AllSettings',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('changed', models.BooleanField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Active',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('automatic', models.BooleanField(blank=True)),
                ('last_check', models.DateTimeField(auto_now=True)),
                ('has_permision_to_work', models.BooleanField(blank=True, default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Thresholds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wavelength', models.PositiveBigIntegerField()),
                ('thresholds_format_name', models.CharField(choices=[('n', 'normal'), ('f', 'fine'), ('c', 'cors')], default='n', max_length=1)),
                ('thresholds_type', models.CharField(choices=[('mi', 'minor'), ('ma', 'major')], default='mi', max_length=2)),
                ('splice_loss', models.CharField(max_length=255)),
                ('connector', models.CharField(max_length=255)),
                ('span_loss', models.CharField(max_length=255)),
                ('reflectance', models.CharField(max_length=255)),
                ('setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thresholds', to='core.allsettings')),
            ],
        ),
        migrations.CreateModel(
            name='TestConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_ports', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('port_number', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('wavelength', models.PositiveBigIntegerField()),
                ('pulsewidth', models.PositiveBigIntegerField()),
                ('range', models.PositiveBigIntegerField()),
                ('test_interval_hours', models.PositiveSmallIntegerField()),
                ('test_interval_minutes', models.PositiveSmallIntegerField()),
                ('duration', models.PositiveIntegerField()),
                ('setting', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='test_configuration', to='core.allsettings')),
            ],
        ),
        migrations.CreateModel(
            name='ManualTestSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wavelength', models.PositiveBigIntegerField()),
                ('pulsewidth', models.PositiveBigIntegerField()),
                ('range', models.PositiveBigIntegerField()),
                ('port_name', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('duration', models.PositiveIntegerField()),
                ('setting', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='manual_test_settings', to='core.allsettings')),
            ],
        ),
        migrations.CreateModel(
            name='LinkDefinition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ior', models.FloatField()),
                ('reflectance', models.CharField(max_length=255)),
                ('splice_loss', models.FloatField()),
                ('end_of_fiber', models.PositiveBigIntegerField()),
                ('setting', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='link_definition', to='core.allsettings')),
            ],
        ),
        migrations.CreateModel(
            name='Fiber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
                ('end_location', models.CharField(max_length=255)),
                ('cable_type', models.CharField(max_length=255)),
                ('comment', models.CharField(default='no comment', max_length=255)),
                ('operator', models.CharField(max_length=255)),
                ('cable_sn', models.CharField(max_length=255)),
                ('autosave', models.BooleanField()),
                ('setting', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fiber', to='core.allsettings')),
            ],
        ),
        migrations.AddConstraint(
            model_name='thresholds',
            constraint=models.UniqueConstraint(fields=('setting', 'wavelength', 'thresholds_format_name'), name='unique together constraint'),
        ),
    ]
