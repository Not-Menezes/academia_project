# Generated by Django 3.1.2 on 2020-11-21 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='is_professor',
        ),
        migrations.RemoveField(
            model_name='account',
            name='is_superuser',
        ),
        migrations.AlterField(
            model_name='account',
            name='function',
            field=models.CharField(choices=[('S', 'Student'), ('P', 'Professor')], default='S', max_length=1, verbose_name='Function'),
        ),
    ]
