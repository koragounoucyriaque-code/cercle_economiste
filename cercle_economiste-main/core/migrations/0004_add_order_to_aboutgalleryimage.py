# Add order field to AboutGalleryImage

from django.db import migrations, models


def add_order_field(apps, schema_editor):
    """Add order field if it doesn't exist"""
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='core_aboutgalleryimage' AND COLUMN_NAME='order' AND TABLE_SCHEMA=DATABASE()")
        if cursor.fetchone() is None:
            cursor.execute("ALTER TABLE core_aboutgalleryimage ADD COLUMN `order` INT DEFAULT 0")


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_add_missing_fields'),
    ]

    operations = [
        migrations.RunPython(add_order_field, reverse_func),
    ]
