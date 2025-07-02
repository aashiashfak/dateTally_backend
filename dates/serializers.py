from rest_framework import serializers
from .models import Dates


class DateEntrySerializer(serializers.ModelSerializer):
    date = serializers.DateField(required=True)
    count = serializers.IntegerField(required=True)
    class Meta:
        model = Dates
        fields = ["date", "count"]  
