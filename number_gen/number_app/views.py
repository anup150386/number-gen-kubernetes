# api/views.py
import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
import asyncio
from datetime import datetime
from django.db import connection
from django.utils.decorators import classonlymethod
from django.views.generic import View
from asgiref.sync import sync_to_async

from .models import *
from .serializers import *

logger = logging.getLogger(__name__)



class TrackingNumberView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]  # Apply throttling to this view

    def get(self, request):
        # Get the query parameters from the request
        origin_country_id = request.GET.get('origin_country_id')
        destination_country_id = request.GET.get('destination_country_id')
        weight = request.GET.get('weight')
        created_at = request.GET.get('created_at')
        customer_id = request.GET.get('customer_id')
        customer_name = request.GET.get('customer_name')
        customer_slug = request.GET.get('customer_slug')

        # Construct the filter query dynamically based on the provided parameters
        filters = {}
        if origin_country_id:
            filters['origin_country_id'] = origin_country_id
        if destination_country_id:
            filters['destination_country_id'] = destination_country_id
        if weight:
            filters['weight'] = weight
        if created_at:
            filters['created_at'] = created_at
        if customer_id:
            filters['customer_id'] = customer_id
        if customer_name:
            filters['customer_name'] = customer_name
        if customer_slug:
            filters['customer_slug'] = customer_slug

        # Perform asynchronous filtering in the database
        queryset = self.filter_queryset(filters)

        # Serialize the queryset to return as a response
        serializer = TrackingNumberSerializer(queryset, many=True)
        logger.info(f"Tracking number searched: {serializer.data}")
        logger.info(f"Queries Made: {connection.queries}")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def filter_queryset(self, filters):
        """ synchronous database query filtering based on provided filters """
        #await asyncio.sleep(0)  # Simulate an async operation

        # Filter the TrackingNumber records based on the provided filters
        return TrackingRecord.objects.filter(**filters)

    def post(self, request):
        serializer = TrackingNumberSerializer(data=request.data)

        if serializer.is_valid():
            # If the data is valid, generate a tracking number
            tracking_number = self.generate_tracking_number()

            # Save the valid data with the generated tracking number
            serializer.save(tracking_number=tracking_number)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_tracking_number(self):
        """ Generate a tracking number asynchronously. """
        """ Generate a unique tracking number with regex ^[A-Z0-9]{1,16}$ """
        length = 16
        tracking_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

        # Ensure uniqueness (optional, if using a database)
        while TrackingRecord.objects.filter(tracking_number=tracking_number).exists():
            tracking_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

        logger.info(f"Generated tracking number: {tracking_number}")

        return tracking_number

