from django.db import models
from django.contrib.auth.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')#评论对象
    text = models.TextField()#评论内容
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)#谁评论的
    create_time = models.DateTimeField(auto_now_add=True)#评论时间
    # 记录该条评论的祖宗评论
    root = models.ForeignKey('self',on_delete=models.CASCADE,related_name='root_comment',null=True)
    # 记录该条评论的父级评论
    parent = models.ForeignKey('self',on_delete=models.CASCADE,related_name='parent_comment',null=True)
    # 回复的是谁
    user_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='replies',null=True)#replies:回复
    class Meta:
        ordering = ['create_time']
    def __str__(self):
        return self.text
