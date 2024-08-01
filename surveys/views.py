from rest_framework import viewsets

from .models import Form
from .serializers import FormSerializer


class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
