from django.shortcuts import render,reverse,redirect
from .models import Comment,ContentType
from .forms import CommentForm
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
# 导入多线程
import threading

from django.template.loader import render_to_string


def send_email_threading(subject,message,email):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_FROM,
        recipient_list=[email],
        fail_silently=False,
        html_message=message
    )
# Create your views here.
def update_commit(request):
    '''
    #数据检查
    user = request.user
    text = request.POST.get('text', '').strip()
    if text == '':
        return render(request,'error.html',{'message':'不能输入空白'})
    if not user.is_authenticated:
        return render(request,'error.html',{'message':'请先登录'})
    try:
        type = request.POST.get('content_type','')
        objcet_id = int(request.POST.get('object_id',''))
        model = ContentType.objects.get(model=type).model_class()
        model_obj = model.objects.get(pk=objcet_id)
    except:
        return render(request,'error.html',{'message':'你评论的模型不存在'})
    comment = Comment()
    comment.user = user

    comment.text=text
    comment.content_object = model_obj
    comment.save()
    referer = request.META.get('HTTP_REFERER',reverse('home'))
    return redirect(referer)
    '''

    referer = request.META.get('HTTP_REFERER',reverse('home'))
    data = {}
    commentform = CommentForm(request.POST,user=request.user)
    if commentform.is_valid():
        comment = Comment()
        comment.content_object=commentform.cleaned_data.get('content_object')
        comment.user = commentform.cleaned_data.get('user')
        comment.text = commentform.cleaned_data.get('text')
        parent = commentform.cleaned_data.get('parent')

        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.user_to = parent.user
        comment.save()
        if comment.parent is None:
            # 评论了该博客
            email = comment.content_object.get_email()
            subject = '有人评论了你的博客'

        else:
            # 回复了博客
            subject = '有人回复了你的评论'
            email = comment.user_to.email
        if email != '':
            a = 'http://127.0.0.1:8000%s'%comment.content_object.get_url()
            # message = comment.text + '\n' + a
            context = {}
            context['text'] = comment.text
            context['url'] = ''
            message = render_to_string('comment/send_html.html',context)
            send = threading.Thread(target=send_email_threading,args=(subject,message,email,))
            send.start()
        #返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_username()
        data['comment_time'] = comment.create_time.timestamp()
        data['content'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if not parent is None:
            data['reply_to'] = comment.user_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        data['status'] = 'ERROR'

        data['message'] = list(commentform.errors.values())[0][0]
    return JsonResponse(data)


