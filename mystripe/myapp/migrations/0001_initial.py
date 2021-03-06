# Generated by Django 4.0.4 on 2022-04-26 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
                ('file', models.FileField(upload_to='product_files/')),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('customer_email', models.EmailField(max_length=254, verbose_name='Customer Email')),
                ('amount', models.IntegerField(verbose_name='Amount')),
                ('stripe_payment', models.CharField(max_length=150)),
                ('has_paid', models.BooleanField(default=False, verbose_name='Payment Status')),
                ('create_on', models.DateTimeField(auto_now_add=True)),
                ('update_on', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.product')),
            ],
        ),
    ]
