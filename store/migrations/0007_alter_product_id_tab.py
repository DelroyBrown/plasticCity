# Generated by Django 4.2 on 2023-05-02 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_remove_product_id_tag_product_id_tab'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id_tab',
            field=models.CharField(blank=True, default='tab-', max_length=20, null=True),
        ),
    ]
