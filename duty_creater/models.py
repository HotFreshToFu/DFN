from django.db import models
from django.conf import settings

# Create your models here.
class Event(models.Model):
    # on_delete=DO_NOTHING: nurse user가 삭제되어도 db를 수정하거나 삭제하지 않는 것으로 추정
    nurse = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    date = models.DateField()
    duty = models.IntegerField()


    def __str__(self):
        return f'{self.date}N{self.nurse.pk}D{self.duty}'