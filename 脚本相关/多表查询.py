import datetime
import os
import random

from faker import Faker

if __name__ == '__main__':
    # 加载Django项目的配置信息
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gym_project.settings")
    # 导入Django，并启动Django项目
    import django

    django.setup()

    from app01.models import *

    user_obj = User.objects.filter(id=1).first()
    course_list = []
    for i in range(7):
        d_list = []
        for j in range(8):
            course = user_obj.course_set.filter(day_no=i,time=j).first()
            if not course:
                d_list.append('')
            else:
                d_list.append(course.title)
        course_list.append(d_list)



    print(course_list)