from django.db import migrations
from api.user.models import CostumUser


class Migration(migrations.Migration):
    def seed_data(apps,schema_editor):
        user = CostumUser(
            name = 'amirali',
            email = 'akhbariamirali42@gmail.com',
            is_staff = True,
            is_superuser = True
        )
        user.set_password('aka271827')
        user.save()

    dependencies = []

    operations = [migrations.RunPython(seed_data)]