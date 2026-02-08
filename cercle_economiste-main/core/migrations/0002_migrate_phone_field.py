# Migration to handle the rename from phone_contact to phone

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE core_globalsettings RENAME COLUMN phone_contact TO phone;",
            "ALTER TABLE core_globalsettings RENAME COLUMN phone TO phone_contact;",
            state_operations=[],
        ),
    ]
