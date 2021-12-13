# Generated by Django 3.0.8 on 2021-12-12 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateReceived', models.DateTimeField(auto_now=True)),
                ('content', models.CharField(max_length=120)),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='clinicuser',
            name='address',
            field=models.CharField(default='Olongapo', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clinicuser',
            name='contact',
            field=models.CharField(default='09338698794', max_length=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clinicuser',
            name='middle_name',
            field=models.CharField(default='Dantay', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clinicuser',
            name='offense_count',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clinicuser',
            name='sex',
            field=models.CharField(default='Male', max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clinicuser',
            name='user_category',
            field=models.CharField(default='Patient', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='category',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='content',
            field=models.CharField(max_length=3000),
        ),
        migrations.RemoveField(
            model_name='staff',
            name='assigned_clinic',
        ),
        migrations.AddField(
            model_name='staff',
            name='assigned_clinic',
            field=models.ManyToManyField(related_name='assigned_clinic', to='clinic.Clinic'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AddField(
            model_name='notification',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificationRecipient', to=settings.AUTH_USER_MODEL),
        ),
    ]