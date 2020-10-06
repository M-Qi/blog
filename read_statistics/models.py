from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.auth.models import ContentType
from django.db.models.fields import exceptions

from django.utils import timezone
class Read_number(models.Model):
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class raad_number_Expand():
    def readnumber(self):
        content_type = ContentType.objects.get_for_model(self)
        try:
            read = Read_number.objects.get(content_type=content_type,object_id=self.pk)
            return read.read_num
        except exceptions.ObjectDoesNotExist:
            return 0



class ReadDetailDate(models.Model):
    date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')



