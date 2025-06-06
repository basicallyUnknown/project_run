from django.contrib.auth.models import User
from rest_framework import serializers

from app_run.models import Run


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "date_joined", "username", "last_name", "first_name", "type"]

    def get_type(self, obj):
        return "athlete" if obj.is_staff == False else "coach"

class UserShortsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "last_name", "first_name"]


class RunSerializer(serializers.ModelSerializer):
    athlete_data = UserShortsSerializer(source="athlete", read_only=True)

    class Meta:
        model = Run
        fields = '__all__'
