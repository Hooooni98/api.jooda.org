# Generated by Django 4.1.7 on 2023-05-08 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('churchs', '0004_alter_churchhistory_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='churchnotice',
            name='content',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='공지사항 내용'),
        ),
    ]
