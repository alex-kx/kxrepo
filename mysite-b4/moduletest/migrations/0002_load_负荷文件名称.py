# Generated by Django 2.0 on 2018-03-21 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moduletest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='load',
            name='负荷文件名称',
            field=models.CharField(default='xxx项目负荷数据', max_length=200),
            preserve_default=False,
        ),
    ]
