from django.contrib.auth.management import create_permissions
from django.db import migrations

GROUP = "Moderators"


def create_group(apps, schema_editor):
    # Permissions are normally created in post_migrate, i.e. after this runs
    # on a fresh database, so make sure they exist first.
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    group, _ = Group.objects.get_or_create(name=GROUP)
    group.permissions.add(
        Permission.objects.get(codename="delete_review", content_type__app_label="reviews")
    )


def delete_group(apps, schema_editor):
    apps.get_model("auth", "Group").objects.filter(name=GROUP).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0002_review_user"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]
    operations = [migrations.RunPython(create_group, delete_group)]
