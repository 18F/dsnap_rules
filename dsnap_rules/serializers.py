from rest_framework import serializers
from .models import ApplicationPeriod, Disaster

class CountyField(serializers.RelatedField):
    def to_representation(self, value):
        return f"{value.name}"


class ApplicationPeriodSerializer(serializers.ModelSerializer):
    counties = CountyField(many=True, read_only=True)
    class Meta:
        model = ApplicationPeriod
        fields = ('begin_date', 'end_date', 'counties')

class DisasterSerializer(serializers.ModelSerializer):
    application_periods = ApplicationPeriodSerializer(many=True)
    class Meta:
        model = Disaster
        fields = '__all__'
