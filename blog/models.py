from django.db import models
from django.contrib.auth.models import User,ContentType
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

from read_statistics.models import Read_number,raad_number_Expand,ReadDetailDate
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.

class BlogType(models.Model):
    # verbose_name=在后台管理的名
    type_name = models.CharField(max_length=15, verbose_name='分类')

    def __str__(self):
        return self.type_name

    def type(self):
        return self.type_name

    # 指定当前方法按照哪个字段进行排序
    type.admin_order_field = 'type_name'
    # 指定方法在后台显示的名称
    type.short_description = '分类'

    def parent(self):
        # 返回父标题的名称
        return self.blog_set.name


class Blog(models.Model,raad_number_Expand):
    title = models.CharField(max_length=30, verbose_name='标题')
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    # 设置反向关系
    read_time = GenericRelation(ReadDetailDate)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('blog:detail', kwargs={'blog_id': self.pk})

    def get_email(self):

        return self.author.email

    def __str__(self):
        return '<Blog:%s>' % self.title


    def type(self):
        return self.blog_type

    # 指定方法在后台显示的名称
    type.short_description = '分类'
    # readnumber.short_description = '阅读数量'
    # 指定字段在后台排序
    type.admin_order_field = 'blog_type'

    class Meta:
        ordering = ['-create_time']

"""
class Read_number(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog,on_delete=models.DO_NOTHING)

"""