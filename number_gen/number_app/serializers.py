# api/serializers.py
from rest_framework import serializers
from .models import TrackingRecord


class TrackingNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingRecord
        fields = [
            'origin_country_id',
            'destination_country_id',
            'weight',
            'created_at',
            'customer_id',
            'customer_name',
            'customer_slug',
            'tracking_number'
        ]

    def validate(self, data):
        # Perform any custom validation if needed
        return data
