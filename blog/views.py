from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Blog, BlogType
from django.contrib.auth.models import ContentType
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db.models import Count
from user.forms import LoginForm
from read_statistics.utils import get_seven_days_data,read_statistics,today_hot_data,yesterday_hot_data
from django.utils import timezone
import datetime

# Create your views here.
each_page_number = 7
def get_week_hot_data():
    date = timezone.now().date()
    week_time = date-datetime.timedelta(days=7)
    a = Blog.objects.filter(read_time__date__gt=week_time).values('id','title') \
                                                            .annotate(read_nums=Sum('read_time__read_num')) \
                                                            .order_by('-read_nums')
    return a[:5]

def home(request):
    context = {}

    contenttype = ContentType.objects.get_for_model(Blog)
    time,count = get_seven_days_data(contenttype)
    today_hot = today_hot_data(contenttype)
    yesterday_hot = yesterday_hot_data(contenttype)

    week_hot_cache = cache.get('week_hot_datas')
    if week_hot_cache is None:
        week_hot_datas = get_week_hot_data()
        cache.set('week_hot_datas',week_hot_datas,3600)
        week_hot_cache = cache.get('week_hot_datas')

    context['today_hot'] = today_hot
    context['yesterday_hot'] = yesterday_hot
    context['week_hot'] = week_hot_cache
    context['time'] = time
    context['count'] = count

    return render(request, 'home.html',context)


def get_blog_list_data(request,blogs):
    context = {}
    page_num = request.GET.get('page', 1)
    # 获取总共数据paginator对象
    paginator = Paginator(blogs, each_page_number)
    # 获取当前页的数据
    page_of_blogs = paginator.get_page(page_num)
    # 总共页数
    page_ranges = page_of_blogs.paginator.num_pages
    # 当前页
    current_page = page_of_blogs.number

    page_range = [i for i in range(1, page_ranges + 1) if
                  i > current_page - 3 and i < current_page + 3 or i == 1 or i == page_ranges]

    try:
        if page_range[1] != 2:
            page_range.insert(1, '...')
        if page_range[-2] != page_ranges - 1:
            page_range.insert(-1, '...')
    except IndexError:
        pass
    #获取日期归档博客的数量
    dates = Blog.objects.dates('create_time', 'month', order='DESC')#时间对象
    print(dates)
    dic = {}
    for date in dates:

        date_count = Blog.objects.filter(create_time__year=date.year,create_time__month=date.month).count()
        dic[date] = date_count
        print('date=',date)

    context['page_range'] = page_range
    context['blogs'] = page_of_blogs
    context['bolg_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = dic
    return context

def blog_list(request):
    blogs = Blog.objects.all()
    context = get_blog_list_data(request,blogs)
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, blog_id):
    context = {}

    blog = get_object_or_404(Blog, id=blog_id)
    read_cookie_key = read_statistics(request,blog)

    context['previous_page'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['next_page'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    context['blog'] = blog
    response = render(request,'blog/blog_detail.html',context)
    response.set_cookie(read_cookie_key,'true')


    return response


def blog_type(request, blog_type):

    blog_type = get_object_or_404(BlogType, pk=blog_type)
    blogs = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_data(request,blogs)
    return render(request, 'blog/blog_type.html', context)


def blog_date(request,year,month):

    blogs = Blog.objects.filter(create_time__year=year,create_time__month=month)
    context = get_blog_list_data(request,blogs)
    dates = '%d年%d月' % (year,month)
    context['dates'] = dates

    return render(request, 'blog/blog_date.html', context)
