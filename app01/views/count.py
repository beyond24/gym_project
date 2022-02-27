
from django.contrib.auth.models import User
from django.shortcuts import render
from ..models import User


def dashboard(request):
    user_count = User.objects.count()


    context = {
        'user_count': user_count,
    }
    return render(request, 'dashboard.html', context)