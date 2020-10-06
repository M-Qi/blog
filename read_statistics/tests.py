from django.test import TestCase

# Create your tests here.
import datetime
import time
# a = datetime.datetime.now()
# print(type(a))
# a= a.strftime('%y-%m-%d %H:%M:%S')
# print(a)
# print(type(a))
# date = datetime.datetime.strptime(a,'%y-%m-%d %H:%M:%S')
# print(date)
# print(type(date))
#1到100求和的结果
# sum1 = 0
# for i in range(0,101):
#     sum1+=i
#     print('%d+%d=%d'%(i,sum1,sum1+i))
# print(sum1)

# for i in range(1,101):
#     if i%10==2 and i %3==0:
#         print(i)

# num = int(input('请输入一个整数：'))
# count=0
# if isinstance(num,int):
#     str_num = str(num)
#     for i in str_num:
#        count+=1
#
# print('你输入的数为{}位数'.format(count))


#求质数:除了1和它本身以外,不能再被其他整数整除

# for i in range(100,200):
#     for j in range(2,i):
#         if i%j==0:
#             # print(i)
#             break
#     else:
#         print(i)

for i in range(1,11):
    if i%2==0:
        break
    else:
        print(i)

