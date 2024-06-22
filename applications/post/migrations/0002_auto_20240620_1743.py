from django.db import migrations

def populate_tags(apps, schema_editor):
    Tag = apps.get_model('post', 'Tag')  # Замените 'your_app_name' на имя вашего приложения
    tags = [
        {'title': 'Technology'},
        {'title': 'Science'},
        {'title': 'Programming'},
        {'title': 'Art'},
    ]
    for tag_data in tags:
        Tag.objects.create(**tag_data)


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_tags),
    ]
