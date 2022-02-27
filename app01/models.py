from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

class User(models.Model):
    """ 用户 """
    username = models.CharField(unique=True,verbose_name='用户名', max_length=32)
    number = models.CharField(unique=True, verbose_name='手机号', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    # name = models.CharField(verbose_name='姓名', max_length=10)
    # email = models.EmailField(verbose_name='邮箱')
    acount = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)

    level_choices = {
        (1, "游客"),
        (2, "普通会员"),
        (3, "高级会员"),
    }
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

        # constraints = [
        #     models.UniqueConstraint(fields=['username'], name='unique_username'),
        #     models.UniqueConstraint(fields=['number'], name='unique_number')
        # ]

    def __str__(self):
        return self.username

class Coach(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=32)

    bio = models.CharField(verbose_name='经历', max_length=100, null=True, blank=True)
    avatar = models.ImageField(verbose_name='头像',upload_to='avatar/', null=True, blank=True )

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '教练'
        verbose_name_plural = '教练'

class Award(models.Model):

    coach = models.ForeignKey(
        Coach,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='award'
    )
    title = models.CharField(verbose_name='奖项标题',max_length=50)
    img_file = models.ImageField(verbose_name='照片',upload_to='awards/', null=True, blank=True )
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = '奖项'
        verbose_name_plural = '奖项'

class ArticleColumn(models.Model):
    """
    栏目的 Model
    """
    # 栏目标题
    title = models.CharField(verbose_name='分类名称',max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(verbose_name='创建时间',default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = '文章分类'

class ArticlePost(models.Model):
    author = models.ForeignKey(Coach, on_delete=models.CASCADE, verbose_name='作者')
    title = models.CharField('文章标题', max_length=100)
    body = models.TextField('文章内容')
    created = models.DateTimeField('文章创建时间',default=timezone.now)
    updated = models.DateTimeField('最近一次更新',auto_now=True)
    total_views = models.PositiveIntegerField('浏览量',default=0)
    tags = TaggableManager(blank=True)
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ('-created',)

    def __str__(self):
        return self.title
        # 获取文章地址

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.id])

class Comment(models.Model):
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body[:20]



class Course(models.Model):
    title = models.CharField(verbose_name='课程标题',max_length=30)
    body = models.TextField(verbose_name='课程详细')
    img_file = models.ImageField(verbose_name='课程图像',upload_to='course/', null=True, blank=True )
    period = models.SmallIntegerField('课时长')
    price = models.DecimalField(verbose_name='价格', max_digits=10, decimal_places=2)
    day_choice = {
        (1,'周一'),
        (2,'周二'),
        (3,'周三'),
        (4,'周四'),
        (5,'周五'),
        (6,'周六'),
        (7,'周日'),
    }
    day_no = models.SmallIntegerField(verbose_name='课程时间',choices=day_choice)
    time_choice = {
        (1,'9:00am-10:00am'),
        (2,'10:00am-11:00am'),
        (3,'11:00am-12:00am'),
        (4,'14:00am-15:00am'),
        (5,'15:00pm-16:00pm'),
        (6,'16:00pm-17:00pm'),
        (7,'17:00pm-18:00pm'),
        (8,'19:00pm-20:00pm'),
    }
    time = models.SmallIntegerField(verbose_name='时间段',choices=time_choice)
    coach = models.ForeignKey(
        Coach,
        on_delete=models.CASCADE,
        related_name='course'
    )
    user = models.ManyToManyField(
        User,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = '课程管理'
        verbose_name_plural = '课程管理'