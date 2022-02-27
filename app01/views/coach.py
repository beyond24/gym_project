from django.shortcuts import render, HttpResponse, get_object_or_404, redirect

from app01.models import Coach
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootstrapModelForm




def coach_list(request):

    coaches = Coach.objects.all()

    content = {
        'coaches': coaches
    }

    return render(request,'coach_list.html', content)