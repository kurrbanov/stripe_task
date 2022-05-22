# Generated by Django 4.0.4 on 2022-05-22 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(unique=True)),
                ('percent_off', models.IntegerField()),
                ('duration', models.CharField(choices=[('forever', 'forever'), ('once', 'once'), ('repeating', 'repeating')], max_length=9)),
                ('duration_in_months', models.IntegerField(blank=True, default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(unique=True)),
                ('jurisdiction', models.CharField(default='RU', max_length=2)),
                ('discount', models.ManyToManyField(blank=True, to='stripe_app.discount')),
            ],
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_id', models.CharField(max_length=255)),
                ('display_name', models.CharField(max_length=3)),
                ('jurisdiction', models.CharField(choices=[('US', 'US'), ('DE', 'DE'), ('RU', 'RU')], max_length=2)),
                ('percentage', models.IntegerField()),
                ('inclusive', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, unique=True)),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stripe_app.discount')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stripe_app.item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stripe_app.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='tax',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stripe_app.tax'),
        ),
    ]
