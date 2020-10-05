# Generated by Django 3.0.7 on 2020-06-26 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crispresso_upload', '0003_auto_20200626_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crispressodata',
            name='n_deleted',
            field=models.DecimalField(decimal_places=20, default=0.0, max_digits=40),
        ),
        migrations.AlterField(
            model_name='crispressodata',
            name='n_inserted',
            field=models.DecimalField(decimal_places=20, default=0.0, max_digits=40),
        ),
        migrations.AlterField(
            model_name='crispressodata',
            name='n_mutated',
            field=models.DecimalField(decimal_places=20, default=0.0, max_digits=40),
        ),
        migrations.AlterField(
            model_name='crispressodata',
            name='n_reads',
            field=models.DecimalField(decimal_places=20, default=0.0, max_digits=40),
        ),
        migrations.AlterField(
            model_name='crispressodata',
            name='p_reads',
            field=models.DecimalField(decimal_places=20, default=0.0, max_digits=40),
        ),
    ]
