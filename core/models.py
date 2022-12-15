from django.db import models

from django.db.models import DateTimeField


class Base(models.Model):
    creation_date = DateTimeField(auto_now_add=True)
    edit_date = DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Request(Base):
    generation_time = DateTimeField(auto_now=True)
    image = models.FileField(upload_to='images/')
    user_id = models.IntegerField(null=True)
    user_name = models.CharField(max_length=50)
    image_pixel_size = models.IntegerField(null=True)
    algorithm_name = models.CharField(max_length=100, null=True)
    iterations = models.IntegerField(null=True)

    def __str__(self):
        return str(self.user_name)



