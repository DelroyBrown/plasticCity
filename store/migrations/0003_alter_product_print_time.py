# Generated by Django 4.2 on 2023-05-02 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_print_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='print_time',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
    ]
