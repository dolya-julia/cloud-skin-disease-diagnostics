from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import UploadedFile
import PIL
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.conf import settings

# from .models import Image
# from .serializers import ImageSerializer, FileUploadSerializer
from .serializers import FileUploadSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from PIL import Image
import os
import torch
import numpy as np # linear algebra
from . import prediction


# class PostList(APIView):
#     def get(self, request, format=None):
#         posts = Image.objects.all()
#         serializer = ImageSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = ImageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,
#                             status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            upload_file = serializer.save()
            obj = UploadedFile.objects.get(id=upload_file.id)
            file_obj = obj.file
            image = Image.open(file_obj.open())
            image_tensor = prediction.transform(image)
            transformed_image = image_tensor.unsqueeze(0)
            preds = prediction.model(transformed_image)
            test_predictions = []
            test_predictions.append(
                torch.nn.functional.softmax(preds, dim=1)[:, 1].data.cpu().numpy())
            test_predictions = np.concatenate(test_predictions)
            l = "nevus" if test_predictions > 0.5 else "melanoma"
            title = l
	    
            probability = test_predictions
            if title == "melanoma":
    	        probability = 1 - probability

            return Response({"prediction": title, "probability": probability}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return render(request, 'index.html')


