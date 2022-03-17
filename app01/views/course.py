from django.http import JsonResponse
from django.shortcuts import render

from app01 import models
from app01.models import Course
from app01.utils.pagination import Pagination
from django.db.models import Q

def course_list(request):
    queryset = Course.objects.all()
    page_obj = Pagination(request,queryset,page_size=4)
    context = {
        'courses': page_obj.page_queryset,
        'page_string':page_obj.html(),
    }
    return render(request, 'course_list.html', context)


def course_detail(request, nid):
    course = Course.objects.filter(id=nid).first()
    user_obj = models.User.objects.filter(id=request.session['info']['id']).first()
    content = {
        'course': course,
        'user_obj':user_obj,
    }
    return render(request, 'course_detail.html', content)


def buy_course(request):
    uid = request.GET.get('uid')
    course_obj = models.Course.objects.filter(id=uid).first()
    user_obj = models.User.objects.filter(id=request.session['info']['id']).first()
    exists = user_obj.course_set.filter(id=uid).exists()
    course_day = course_obj.day_no
    course_no = course_obj.time
    time_clash = user_obj.course_set.filter(Q(day_no = course_day)&Q(time = course_no)).exists()
    if exists:
        return JsonResponse({'status': False, 'errors': '购买失败，你已经购买过此课程'})
    elif time_clash:
        return JsonResponse({'status': False, 'errors': '购买失败，你已经购买过相同时间段的课程'})
    elif user_obj.acount < course_obj.price:
        return JsonResponse({'status': False, 'errors': '余额不足！'})
    else:
        user_obj.acount -= course_obj.price
        user_obj.course_set.add(course_obj)
        user_obj.save()
        return JsonResponse({'status': True, 'acount':user_obj.acount.to_eng_string()})
