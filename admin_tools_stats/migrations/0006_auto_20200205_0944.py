# Generated by Django 2.2.10 on 2020-02-05 08:44

from django.db import migrations, models
import django.db.models.deletion


def transform_criteria_mtm(apps, schema_editor):
    DashboardStats = apps.get_model('admin_tools_stats', 'DashboardStats')
    CriteriaToStatsM2M = apps.get_model('admin_tools_stats', 'CriteriaToStatsM2M')
    for stats in DashboardStats.objects.all():
        for criteria in stats.criteria.all():
            CriteriaToStatsM2M.objects.create(stats=stats, criteria=criteria, use_as=criteria.use_as)


def transform_criteria_mtm_reverse(apps, schema_editor):
    DashboardStats = apps.get_model('admin_tools_stats', 'DashboardStats')
    CriteriaToStatsM2M = apps.get_model('admin_tools_stats', 'CriteriaToStatsM2M')
    for stats in DashboardStats.objects.all():
        for criteria in stats.criteria_new.all():
            if not stats.criteria.through.objects.filter(dashboardstats=stats, dashboardstatscriteria=criteria).exists():
                stats.criteria.through.objects.create(dashboardstats=stats, dashboardstatscriteria=criteria)
                criteria.use_as = CriteriaToStatsM2M.objects.get(stats=stats, criteria=criteria).use_as
                criteria.save()


class Migration(migrations.Migration):

    dependencies = [
        ('admin_tools_stats', '0005_auto_20200203_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='CriteriaToStatsM2M',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(blank=True, null=True, unique=True)),
                ('prefix', models.CharField(default='', help_text='prefix, that will be added befor all lookup paths of criteria', max_length=255, verbose_name='criteria field prefix')),
                ('use_as', models.CharField(choices=[('chart_filter', 'Chart filter'), ('multiple_series', 'Multiple series')], default='chart_filter', max_length=90, verbose_name='Use dynamic criteria as')),
                ('criteria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='th', to='admin_tools_stats.DashboardStatsCriteria')),
                ('stats', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='th1', to='admin_tools_stats.DashboardStats')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.AddField(
            model_name='dashboardstats',
            name='criteria_new',
            field=models.ManyToManyField(blank=True, related_name='asdf', through='admin_tools_stats.CriteriaToStatsM2M', to='admin_tools_stats.DashboardStatsCriteria'),
        ),
        migrations.RunPython(transform_criteria_mtm, reverse_code=transform_criteria_mtm_reverse),
    ]
