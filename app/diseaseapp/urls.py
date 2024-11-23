from django.urls import path
# from .views import PostList, FileUploadAPIView, index
from .views import FileUploadAPIView, index

urlpatterns = [
    # path("", PostList.as_view(), name="post_list"),
    path('upload-file/', FileUploadAPIView.as_view(), name='upload-file'),
    path('index/', index, name='index'),
]