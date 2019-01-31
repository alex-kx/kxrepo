# Generated by Django 2.0 on 2018-03-26 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moduletest', '0004_项目信息'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('项目名称', models.CharField(default='', max_length=200)),
                ('steam_load', models.CharField(default='', max_length=200000)),
                ('electricity_load', models.CharField(default='', max_length=200000)),
                ('市政电价', models.CharField(default='', max_length=200000)),
                ('上网电价', models.CharField(default='', max_length=200000)),
                ('内部售电价', models.CharField(default='', max_length=200000)),
                ('发电机台数', models.IntegerField(default=1)),
                ('燃气价格', models.DecimalField(decimal_places=4, default=0, max_digits=20)),
                ('蒸汽价格', models.DecimalField(decimal_places=4, default=0, max_digits=20)),
                ('燃气热值', models.DecimalField(decimal_places=4, default=0, max_digits=20)),
                ('水蒸气焓差', models.DecimalField(decimal_places=4, default=0, max_digits=20)),
                ('燃气轮机满负荷运行小时数限制', models.IntegerField(default=0)),
                ('燃气内燃机满负荷运行小时数限制', models.IntegerField(default=0)),
                ('燃气锅炉效率', models.DecimalField(decimal_places=4, default=0, max_digits=20)),
                ('余热锅炉效率', models.DecimalField(decimal_places=4, default=0, max_digits=20)),
            ],
        ),
        migrations.DeleteModel(
            name='项目信息',
        ),
    ]
