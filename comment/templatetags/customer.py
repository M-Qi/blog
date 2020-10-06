from django import template
from django.contrib.auth.models import ContentType
from ..models import Comment
from ..forms import CommentForm
register = template.Library()

@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type,object_id=obj.id).count()

@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    data = {}
    data['object_id'] = obj.id
    data['content_type'] = content_type.model
    data['reply_comment_id'] = 0
    form = CommentForm(initial=data)
    return form

@register.simple_tag
def get_comment_data(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type,object_id=obj.id,parent=None)
    return comments.order_by('-create_time')
