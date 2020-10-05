# Generated by Django 3.0.7 on 2020-06-26 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crispresso_upload', '0002_auto_20200616_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crispressodata',
            name='description',
        ),
        migrations.RemoveField(
            model_name='crispressodata',
            name='fileNames',
        ),
        migrations.RemoveField(
            model_name='crispressodata',
            name='published',
        ),
        migrations.RemoveField(
            model_name='crispressodata',
            name='title',
        ),
        migrations.AddField(
            model_name='crispressodata',
            name='aligned_sequence',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='crispressodata',
            name='hdr',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='crispressodata',
            name='n_deleted',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
        migrations.AddField(
            model_name='crispressodata',
            name='n_inserted',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
        migrations.AddField(
            model_name='crispressodata',
            name='n_mutated',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
        migrations.AddField(
            model_name='crispressodata',
            name='n_reads',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
        migrations.AddField(
            model_name='crispressodata',
            name='nhej',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='crispressodata',
            name='p_reads',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=2),
        ),
        migrations.AddField(
            model_name='crispressodata',
            name='reference_sequence',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='crispressodata',
            name='unmodified',
            field=models.BooleanField(default=False),
        ),
    ]
