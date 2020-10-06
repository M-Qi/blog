from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth.models import ContentType
from django.http import JsonResponse
from .models import LikeCount,LikeRecord

# Create your views here.

def ErrorResponse(code,message):
    data = {}
    data['code'] = code
    data['message'] = message

    return JsonResponse(data)

def SuccessResponse(like_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['like_num'] = like_num

    return JsonResponse(data)

def like_num(request):
    #获取数据  验证数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(401,'你未登录')
    object_id = request.GET.get('object_id')
    is_active = request.GET.get('is_active')
    content_type = request.GET.get('content_type')
    try:
        content_type = ContentType.objects.get(model=content_type)
        # model_class = content_type.model_class()
        # model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(400,'错误')
    if is_active == 'true':
        #要点赞
        like_obj,is_create = LikeRecord.objects.get_or_create(content_type=content_type,user=user,object_id=object_id)
        if is_create:
            num_obj,is_create = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            num_obj.like_num+=1
            num_obj.save()
            return SuccessResponse(num_obj.like_num)

        else:
            return ErrorResponse(400,'data error')
    else:
        #要取消点赞

        like_obj = LikeRecord.objects.filter(content_type=content_type, user=user,object_id=object_id).exists()
        if like_obj:
            like_nu = LikeRecord.objects.get(content_type=content_type, user=user, object_id=object_id)
            like_nu.delete()
            num_obj, is_create = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not is_create:
                num_obj.like_num-=1
                num_obj.save()
                return SuccessResponse(num_obj.like_num)
        else:
            #没有点赞过
            return ErrorResponse(401,'你没有点赞不能取消')

