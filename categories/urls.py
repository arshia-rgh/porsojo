from django.urls import path

from .views import FolderList

urlpatterns = [
    path('', FolderList.as_view(), name = 'folder_list')
]