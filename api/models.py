from django.db import models
import uuid


class Destination(models.Model):
    place = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.place


class Booking(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
    ]

    booking_id = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
        blank=True,
        null=True,
    )

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE
    )

    travel_date = models.DateField()

    return_date = models.DateField(
        null=True,
        blank=True
    )

    payment_method = models.CharField(max_length=50)

    total_amount = models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = "TRV" + uuid.uuid4().hex[:7].upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.booking_id if self.booking_id else f"Booking-{self.id}"


class FlightBooking(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    destination = models.CharField(max_length=100)
    travel_date = models.DateField()

    status = models.CharField(
        max_length=20,
        default="Booked"
    )

    def __str__(self):
        return self.full_name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
            
    def __str__(self):
        return self.email


class HotelBooking(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    destination = models.CharField(max_length=100)
    travel_date = models.DateField()
    travelers = models.IntegerField()
    hotel_type = models.CharField(max_length=100)
    special_request = models.TextField(blank=True)



    def __str__(self):
        return self.full_name