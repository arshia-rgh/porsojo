from django.urls import path

from .views import FolderList, FolderDetail

urlpatterns = [
    path('', FolderList.as_view(), name = 'folder_list'),
    path('<int:pk>', FolderDetail.as_view(), name = 'folder_detail'),
]