# Generated by Django 4.1.6 on 2023-03-30 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StudentUnion', '0004_duereceipt_level_alter_duereceipt_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='department',
        ),
        migrations.RemoveField(
            model_name='student',
            name='level',
        ),
    ]