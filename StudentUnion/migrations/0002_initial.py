# Generated by Django 4.1.6 on 2023-04-11 20:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('StudentUnion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='student',
            name='years_active',
            field=models.ManyToManyField(blank=True, to='StudentUnion.sessionyearmodel'),
        ),
        migrations.AddField(
            model_name='sessionyearmodel',
            name='session_president',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='StudentUnion.student'),
        ),
        migrations.AddField(
            model_name='duereceipt',
            name='academic_session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='StudentUnion.sessionyearmodel'),
        ),
        migrations.AddField(
            model_name='duereceipt',
            name='receipt_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_receipts', to='StudentUnion.student'),
        ),
    ]
