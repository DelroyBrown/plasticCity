# Generated by Django 4.2 on 2023-05-02 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_print_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='id_tab',
            field=models.CharField(blank=True, default='tab-', max_length=10, null=True),
        ),
    ]