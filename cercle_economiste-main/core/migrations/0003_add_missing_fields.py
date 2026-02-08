# Migration to add missing fields

from django.db import migrations, models
from django.db import connection


def add_fields_if_not_exist(apps, schema_editor):
    """Add fields if they don't already exist"""
    with connection.cursor() as cursor:
        # Helper to check if column exists
        def column_exists(table, column):
            cursor.execute(f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{table}' AND COLUMN_NAME='{column}' AND TABLE_SCHEMA=DATABASE()")
            return cursor.fetchone() is not None
        
        # Add fields
        if not column_exists('core_aboutgalleryimage', 'image'):
            cursor.execute("ALTER TABLE core_aboutgalleryimage ADD COLUMN image LONGBLOB")
        if not column_exists('core_aboutgalleryimage', 'created_at'):
            cursor.execute("ALTER TABLE core_aboutgalleryimage ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
        
        if not column_exists('core_aboutsection', 'image'):
            cursor.execute("ALTER TABLE core_aboutsection ADD COLUMN image LONGBLOB")
        if not column_exists('core_aboutsection', 'created_at'):
            cursor.execute("ALTER TABLE core_aboutsection ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
        if not column_exists('core_aboutsection', 'updated_at'):
            cursor.execute("ALTER TABLE core_aboutsection ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
        
        if not column_exists('core_herosection', 'image'):
            cursor.execute("ALTER TABLE core_herosection ADD COLUMN image LONGBLOB")
        
        if not column_exists('core_newsitem', 'content'):
            cursor.execute("ALTER TABLE core_newsitem ADD COLUMN content LONGTEXT")
        if not column_exists('core_newsitem', 'image'):
            cursor.execute("ALTER TABLE core_newsitem ADD COLUMN image LONGBLOB")
        if not column_exists('core_newsitem', 'updated_at'):
            cursor.execute("ALTER TABLE core_newsitem ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
        
        if not column_exists('core_publication', 'content'):
            cursor.execute("ALTER TABLE core_publication ADD COLUMN content LONGTEXT")
        if not column_exists('core_publication', 'image'):
            cursor.execute("ALTER TABLE core_publication ADD COLUMN image LONGBLOB")
        if not column_exists('core_publication', 'updated_at'):
            cursor.execute("ALTER TABLE core_publication ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
        
        if not column_exists('core_member', 'role'):
            cursor.execute("ALTER TABLE core_member ADD COLUMN role VARCHAR(100)")
        if not column_exists('core_member', 'email'):
            cursor.execute("ALTER TABLE core_member ADD COLUMN email VARCHAR(254)")
        if not column_exists('core_member', 'is_active'):
            cursor.execute("ALTER TABLE core_member ADD COLUMN is_active TINYINT(1) DEFAULT 1")
        if not column_exists('core_member', 'photo'):
            cursor.execute("ALTER TABLE core_member ADD COLUMN photo LONGBLOB")
        if not column_exists('core_member', 'created_at'):
            cursor.execute("ALTER TABLE core_member ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
        if not column_exists('core_member', 'updated_at'):
            cursor.execute("ALTER TABLE core_member ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
        
        if not column_exists('core_testimonial', 'created_at'):
            cursor.execute("ALTER TABLE core_testimonial ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
        if not column_exists('core_testimonial', 'is_active'):
            cursor.execute("ALTER TABLE core_testimonial ADD COLUMN is_active TINYINT(1) DEFAULT 1")
        if not column_exists('core_testimonial', 'order'):
            cursor.execute("ALTER TABLE core_testimonial ADD COLUMN `order` INT DEFAULT 0")
        if not column_exists('core_testimonial', 'photo'):
            cursor.execute("ALTER TABLE core_testimonial ADD COLUMN photo LONGBLOB")


def reverse_func(apps, schema_editor):
    pass  # Don't remove columns on rollback


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_migrate_phone_field'),
    ]

    operations = [
        migrations.RunPython(add_fields_if_not_exist, reverse_func),
    ]
