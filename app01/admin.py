from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import User, ArticlePost, ArticleColumn, Comment, Coach, Award, Course

admin.site.site_header = '健身房网站后台'
# admin.site.index_title = '健身房网站后台'



class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'number','acount','level')

    list_filter = ('username', 'level',)

    # 每页显示条目数
    list_per_page = 5
    # choices字段设置可编辑
    list_editable = ('level',)
    #连接字段
    # list_display_links = ''

    # '''按级别排倒序'''
    ordering = ('-level',)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author','created','updated')
    list_filter = ('title', 'author',)
    list_per_page = 5


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'article','user')
    list_per_page = 5

class CoachAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_per_page = 5

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','price')
    list_per_page = 5

admin.site.register(User, UserAdmin)
admin.site.register(ArticlePost, ArticleAdmin)
admin.site.register(ArticleColumn)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Coach, CoachAdmin)
admin.site.register(Award)
admin.site.register(Course, CourseAdmin)


