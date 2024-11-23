from django.db import models
from django.core.files.storage import default_storage
# class Image(models.Model):
#     name = models.TextField()
#     # mole_photo = models.ImageField()
#
#     def __str__(self):
#         return self.name


class UploadedFile(models.Model):
    file = models.FileField()
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.uploaded_on.date())
