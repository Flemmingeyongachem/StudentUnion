# Generated by Django 4.1.6 on 2023-03-30 19:24

import StudentUnion.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentUnion', '0005_remove_student_department_remove_student_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duereceipt',
            name='file_name',
            field=models.ImageField(null=True, upload_to=StudentUnion.models.receipt_directory_path),
        ),
    ]
