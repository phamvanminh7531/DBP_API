from django.db import models

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

# Create your models here.
class TWO_IMG2IMG(models.Model):
    img_3d_input = models.ImageField(upload_to=upload_to, blank=True, null=True)
    img_style_input = models.ImageField(upload_to=upload_to, blank=True, null=True)

    def __str__(self):
        return super().__str__()