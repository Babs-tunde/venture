# Generated by Django 4.2 on 2024-10-16 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_storebookentry_profit'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostingLedger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_in', models.IntegerField(default=0)),
                ('goods_out', models.IntegerField(default=0)),
                ('balance', models.IntegerField(default=0)),
                ('last_updated', models.DateField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.product')),
            ],
        ),
    ]
