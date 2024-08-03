from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .models import Folder, FolderItem
from .serializers import FormSerializer


# Implement Folder-CRUD-APIs methods.

class FolderList(APIView):

    def get(self, request):
        queryset = Folder.objects.select_related('user').all()
        serializer = FormSerializer(queryset, many = True)

        return Response(serializer.data)
    

    def post(self, request):
        folder = FormSerializer(data = request.data)
        print(request.data)
        if folder.is_valid():
            print(folder.validated_data)
            folder.save()

        return Response(folder.data, status = status.HTTP_201_CREATED)


