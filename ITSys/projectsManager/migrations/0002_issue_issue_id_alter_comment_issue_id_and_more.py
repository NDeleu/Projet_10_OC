# Generated by Django 4.2.2 on 2023-06-20 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectsManager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='issue_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='issue_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='projectsManager.issue'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='projectsManager.project'),
        ),
    ]
