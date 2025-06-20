from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.views import APIView

from app_run.models import Run
from app_run.serializers import RunSerializer, UserSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class RunsPagination(PageNumberPagination):
    page_size_query_param = 'size'


class UsersPagination(PageNumberPagination):
    page_size_query_param = 'size'


@api_view(['GET'])
def company_details(request):
    details = {"company_name": settings.COMPANY_NAME,
               "slogan": settings.SLOGAN,
               "contacts": settings.CONTACTS}
    return Response(details)


class RunsViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related("athlete").all()
    serializer_class = RunSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'athlete']
    ordering_fields = ['created_at']
    pagination_class = RunsPagination


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['date_joined']
    pagination_class = UsersPagination

    def get_queryset(self):
        qs = self.queryset
        type = self.request.query_params.get("type", None)
        if type == "coach":
            qs = qs.filter(is_staff=True)
        elif type == "athlete":
            qs = qs.filter(is_staff=False)
        return qs


class RunStartAPI(APIView):
    def post(self, request, id):
        run = get_object_or_404(Run, id=id)
        if run.status == 'init':
            run.status = 'in_progress'
            run.save()
            data = {"messege": "Get запрос обработан!"}
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise ValidationError({'messege': 'Get запрос НЕ обработан!'})


class RunStopAPI(APIView):
    def post(self, request, id):
        run = get_object_or_404(Run, id=id)
        if run.status == 'in_progress':
            run.status = 'finished'
            run.save()
            data = {"messege": "Get запрос обработан!"}
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise ValidationError({'messege': 'Get запрос НЕ обработан!'})
