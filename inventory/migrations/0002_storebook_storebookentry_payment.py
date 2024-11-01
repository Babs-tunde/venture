# Generated by Django 4.2 on 2024-10-09 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_goods_value', models.DecimalField(decimal_places=2, max_digits=15)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=15)),
                ('outstanding_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('other_expenses', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('profit', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('date_received', models.DateField()),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.manufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='StoreBookEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('company_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('retail_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('quantity', models.IntegerField()),
                ('storebook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='inventory.storebook')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=15)),
                ('date_paid', models.DateField()),
                ('storebook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='inventory.storebook')),
            ],
        ),
    ]