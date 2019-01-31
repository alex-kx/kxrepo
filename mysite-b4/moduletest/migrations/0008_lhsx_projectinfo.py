# Generated by Django 2.0 on 2018-04-11 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moduletest', '0007_auto_20180330_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='LHSX_ProjectInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('项目名称', models.CharField(default='', max_length=200)),
                ('steam_load', models.CharField(default='', max_length=200000)),
                ('electricity_load', models.CharField(default='', max_length=200000)),
                ('市政电价', models.CharField(default='', max_length=200000)),
                ('上网电价', models.CharField(default='', max_length=200000)),
                ('内部售电价', models.CharField(default='', max_length=200000)),
                ('燃气价格', models.FloatField(default=0)),
                ('水价格', models.FloatField(default=0)),
                ('蒸汽价格', models.FloatField(default=0)),
                ('燃气热值', models.FloatField(default=0)),
                ('管损率', models.FloatField(default=0)),
                ('水蒸气焓差', models.FloatField(default=0)),
                ('土建工程建筑', models.FloatField(default=0)),
                ('管网投资总费用', models.FloatField(default=0)),
                ('辅助工程_设备_设定值', models.FloatField(default=0)),
                ('辅助工程_安装_设定值', models.FloatField(default=0)),
                ('电力接入费', models.FloatField(default=0)),
                ('燃气工程费', models.FloatField(default=0)),
                ('土地费', models.FloatField(default=0)),
                ('收购费用', models.FloatField(default=0)),
                ('人数', models.IntegerField(default=0)),
                ('工资', models.FloatField(default=0)),
                ('变压器容量费', models.FloatField(default=0)),
                ('系统备用容量费', models.FloatField(default=0)),
                ('土地租金', models.FloatField(default=0)),
                ('设备租金', models.FloatField(default=0)),
                ('额外天然气销售年总收入', models.FloatField(default=0)),
                ('额外天然气销售年总成本', models.FloatField(default=0)),
                ('燃气轮机满负荷运行小时数限制', models.FloatField(default=6000)),
                ('燃气轮机自耗电比例', models.FloatField(default=0.04)),
                ('燃气轮机最低运行负荷比例', models.FloatField(default=0.85)),
                ('燃气轮机发电效率修正', models.FloatField(default=1)),
                ('燃气轮机烟气流量修正', models.FloatField(default=1)),
                ('燃气轮机排烟温度修正', models.FloatField(default=1)),
                ('燃气轮机发电功率修正', models.FloatField(default=1)),
                ('燃气内燃机满负荷运行小时数限制', models.FloatField(default=6000)),
                ('燃气内燃机自耗电比例', models.FloatField(default=0.04)),
                ('燃气内燃机最低运行负荷比例', models.FloatField(default=0.75)),
                ('燃气锅炉单位产汽耗电量', models.FloatField(default=5)),
                ('锅炉耗水率', models.FloatField(default=1.1)),
                ('燃气锅炉效率', models.FloatField(default=0.95)),
                ('余热锅炉效率', models.FloatField(default=0.95)),
                ('余热锅炉单位产汽耗电量', models.FloatField(default=2)),
                ('冷却后烟气温度', models.FloatField(default=120)),
                ('余热锅炉单位造价', models.FloatField(default=20)),
                ('燃气锅炉单位造价', models.FloatField(default=13)),
                ('天然气是否先用后付', models.FloatField(default=1)),
                ('电费是否先用后付', models.FloatField(default=0)),
                ('水费是否先用后付', models.FloatField(default=0)),
                ('工资是否先用后付', models.FloatField(default=1)),
                ('维修费是否先用后付', models.FloatField(default=1)),
            ],
        ),
    ]
