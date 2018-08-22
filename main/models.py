from django.db import models

# Create your models here.


class LinkURL(models.Model):
    url = models.TextField('链接', max_length=8192)
    short_code = models.TextField('短代码', unique=True)
    update_time = models.DateTimeField('创建更改时间', auto_now_add=True)
    end_time = models.DateTimeField('失效时间')

    def __str__(self):
        return url

    class META:
        models.Model.ordering = ['update_time']
