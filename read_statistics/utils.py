from django.contrib.auth.models import ContentType
from read_statistics.models import Read_number,ReadDetailDate
from django.db.models import Sum

from django.utils import timezone
import datetime

def read_statistics(request,obj):
    cf = ContentType.objects.get_for_model(obj)

    key = '%s_%d_read'%(cf.model,obj.pk)
    if not request.COOKIES.get(key):

        read_number,create = Read_number.objects.get_or_create(content_type=cf, object_id=obj.pk)
        #计数+1
        read_number.read_num+=1
        read_number.save()

        date = timezone.now().date()
        read_data,create = ReadDetailDate.objects.get_or_create(date=date,content_type=cf,object_id=obj.pk)

        read_data.read_num+=1
        read_data.save()
    return key

def get_seven_days_data(content_type):
    today = timezone.now()
    print(today)
    time = []
    li = []
    for i in range(7,0,-1):
        date = today-datetime.timedelta(days=i)
        time.append(date.strftime('%m/%d'))
        readdatildate = ReadDetailDate.objects.filter(content_type=content_type,date=date)
        result = readdatildate.aggregate(readdate=Sum('read_num'))
        li.append(result['readdate'] or 0)
    print(li)
    print(time)
    return time,li

#今天热门博客
def today_hot_data(content_type):
    date = timezone.now().date()
    read_today_data = ReadDetailDate.objects.filter(content_type=content_type,date=date).order_by('-read_num')
    return read_today_data[:5]

#昨天热门博客
def yesterday_hot_data(content_type):
    date = timezone.now().date()
    yesterday = date-datetime.timedelta(days=1)
    read_yest_data = ReadDetailDate.objects.filter(content_type=content_type,date=yesterday).order_by('-read_num')
    return read_yest_data[:5]

#7天热门博客  #暂时不用目前用views里获取
def week_hot_data(content_type):
    date = timezone.now().date()
    week_days = date - datetime.timedelta(days=7)
    week_data = ReadDetailDate.objects.filter(date__gte=week_days,content_type=content_type) \
                                                            .annotate(read_nums=Sum('read_num')) \
                                                            .order_by('-read_nums')

    return week_data[:5]








