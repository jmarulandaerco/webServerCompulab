# Generated by Django 3.1.12 on 2025-02-04 22:14

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InverterData',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('send_server', models.BooleanField(default=True)),
                ('DATE', models.DateTimeField()),
                ('TP_I', models.IntegerField()),
                ('OPERATION_STATE', models.IntegerField()),
                ('GENERATION', models.FloatField()),
                ('POWER_FACTOR', models.FloatField()),
                ('REACTIVE_POWER', models.FloatField()),
                ('POWER_SNAPSHOT', models.FloatField()),
                ('VOLTAGE_1_DC', models.FloatField()),
                ('VOLTAGE_2_DC', models.FloatField()),
                ('VOLTAGE_3_DC', models.FloatField()),
                ('VOLTAGE_4_DC', models.FloatField()),
                ('CURRENT_1_DC', models.FloatField()),
                ('CURRENT_2_DC', models.FloatField()),
                ('CURRENT_3_DC', models.FloatField()),
                ('CURRENT_4_DC', models.FloatField()),
                ('VOLTAGE_1_AC', models.FloatField()),
                ('VOLTAGE_2_AC', models.FloatField()),
                ('VOLTAGE_3_AC', models.FloatField()),
                ('CURRENT_1_AC', models.FloatField()),
                ('CURRENT_2_AC', models.FloatField()),
                ('CURRENT_3_AC', models.FloatField()),
                ('TEMPERATURE_INVERTER', models.FloatField()),
                ('GRID_FREQUENCY', models.FloatField()),
                ('id_slave', models.IntegerField()),
                ('device_type', models.CharField(max_length=255)),
                ('sent', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'inverters',
                'managed': True,
            },
        ),
    ]
