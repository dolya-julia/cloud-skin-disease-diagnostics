from rest_framework import serializers
# from .models import Image, UploadedFile
from .models import UploadedFile

# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = (
#             "id",
#             "name",
#         )
#         model = Image


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('file', 'uploaded_on',)