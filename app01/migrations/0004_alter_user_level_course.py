# Generated by Django 4.0.1 on 2022-02-18 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_award_coach_alter_user_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='level',
            field=models.SmallIntegerField(choices=[(2, '普通会员'), (1, '游客'), (3, '高级会员')], default=1, verbose_name='级别'),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='课程标题')),
                ('body', models.TextField(verbose_name='课程详细')),
                ('img_file', models.ImageField(blank=True, null=True, upload_to='course/', verbose_name='课程图像')),
                ('period', models.SmallIntegerField(verbose_name='课时长')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价格')),
                ('day_no', models.SmallIntegerField(choices=[(7, '周日'), (2, '周二'), (4, '周四'), (5, '周五'), (1, '周一'), (3, '周三'), (6, '周六')], verbose_name='课程时间')),
                ('time', models.SmallIntegerField(choices=[(2, '10:00am-11:00am'), (3, '15:00pm-16:00pm'), (1, '9:00am-10:00am'), (4, '16:00pm-17:00pm')], verbose_name='时间段')),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='app01.coach')),
                ('user', models.ManyToManyField(to='app01.User')),
            ],
        ),
    ]
