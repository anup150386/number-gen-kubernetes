# api/models.py
from django.db import models
import uuid

class TrackingRecord(models.Model):
    # The tracking number itself (must match regex ^[A-Z0-9]{1,16}$)
    tracking_number = models.CharField(max_length=16, unique=True)

    # Origin and destination country codes (ISO 3166-1 alpha-2 format)
    origin_country_id = models.CharField(max_length=2)  # e.g., "MY"
    destination_country_id = models.CharField(max_length=2)  # e.g., "ID"

    # Order weight in kilograms (up to 3 decimal places)
    weight = models.DecimalField(max_digits=6, decimal_places=3)  # e.g., 1.234

    # Order creation timestamp (RFC 3339 format)
    created_at = models.DateTimeField()  # e.g., "2018-11-20T19:29:32+08:00"

    # Customer information
    customer_id = models.UUIDField(default=uuid.uuid4,
                                   editable=False)  # UUID, e.g., "de619854-b59b-425e-9db4-943979e1bd49"
    customer_name = models.CharField(max_length=255)  # Customer's name, e.g., "RedBox Logistics"
    customer_slug = models.SlugField(max_length=255)  # Slug version of customer name, e.g., "redbox-logistics"

    # Timestamp when the tracking number was created
    tracking_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tracking_number


