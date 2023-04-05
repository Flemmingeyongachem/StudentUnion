# Generated by Django 4.1.6 on 2023-04-01 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StudentUnion', '0007_alter_duereceipt_department_alter_duereceipt_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='my_department',
            field=models.ForeignKey(choices=[('College of Technology', 'College of Technology'), ('FET', 'FET'), ('ASTI', 'ASTI')], null=True, on_delete=django.db.models.deletion.CASCADE, to='StudentUnion.department'),
        ),
        migrations.AddField(
            model_name='student',
            name='my_level',
            field=models.ForeignKey(choices=[(200, 200), (300, 300), (400, 400)], null=True, on_delete=django.db.models.deletion.CASCADE, to='StudentUnion.level'),
        ),
        migrations.AlterField(
            model_name='duereceipt',
            name='department',
            field=models.CharField(choices=[('College of Technology', 'College of Technology'), ('FET', 'FET'), ('ASTI', 'ASTI')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='duereceipt',
            name='level',
            field=models.IntegerField(choices=[(200, 200), (300, 300), (400, 400)], null=True),
        ),
    ]