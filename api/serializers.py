from rest_framework import serializers
# from .models import Destination, Booking
from .models import Destination, Booking, Contact

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer(read_only=True)

    destination_id = serializers.PrimaryKeyRelatedField(
        queryset=Destination.objects.all(),
        source="destination",   
        write_only=True
    )
    return_date = serializers.DateField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = Booking
        fields = [
            "id",
            "booking_id",
            "full_name",
            "email",
            "phone",
            "destination",
            "destination_id",
            "travel_date",
            "return_date",
            "payment_method",
            "total_amount",
            "status",
            "created_at",
        ]

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password"
        ]


    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user