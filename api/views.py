from django.http import JsonResponse
from django.conf import settings
import json
import resend

from rest_framework import generics, status, viewsets
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import (
    Destination,
    Booking,
    Contact,
    Newsletter,
    HotelBooking,
)

from .serializers import (
    BookingSerializer,
    ContactSerializer,
    RegisterSerializer,
)

resend.api_key = settings.RESEND_API_KEY

def destinations(request):
    data = list(Destination.objects.values())
    return JsonResponse(data, safe=False)

class BookingListView(generics.ListAPIView):

    queryset = Booking.objects.all().order_by("-id")
    serializer_class = BookingSerializer

class BookingCreateView(generics.CreateAPIView):

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

@api_view(["GET", "POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def create_booking(request):

    if request.method == "GET":
        bookings = Booking.objects.all().order_by("-id")
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    serializer = BookingSerializer(data=request.data)

    if serializer.is_valid():

        booking = serializer.save()

        try:
            resend.Emails.send({

                "from": "TravelX <onboarding@resend.dev>",
                "to": [booking.email],
                "subject": "🎉 TravelX Booking Confirmed",

                "html": f"""
                <div style="font-family:Arial;padding:25px;background:#f8f9fa">

                    <h1 style="color:#0d6efd;">✈️ TravelX</h1>

                    <h2 style="color:green;">
                        Booking Confirmed ✅
                    </h2>

                    <p>Hello <b>{booking.full_name}</b>,</p>

                    <p>Your booking has been confirmed successfully.</p>

                    <table cellpadding="8">

                        <tr>
                            <td><b>Booking ID</b></td>
                            <td>{booking.booking_id}</td>
                        </tr>

                        <tr>
                            <td><b>Destination</b></td>
                            <td>{booking.destination.place}</td>
                        </tr>

                        <tr>
                            <td><b>Travel Date</b></td>
                            <td>{booking.travel_date}</td>
                        </tr>

                        <tr>
                            <td><b>Return Date</b></td>
                            <td>{booking.return_date}</td>
                        </tr>

                        <tr>
                            <td><b>Payment</b></td>
                            <td>{booking.payment_method}</td>
                        </tr>

                        <tr>
                            <td><b>Total Amount</b></td>
                            <td>₹{booking.total_amount}</td>
                        </tr>

                    </table>

                    <br>

                    <p>Thank you for choosing <b>TravelX</b>.</p>
                    <p>Have a Safe Journey ✈️</p>

                </div>
                """

            })

        except Exception as e:
            print("Email Error:", e)

        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(["PATCH"])
@authentication_classes([])
@permission_classes([AllowAny])
def cancel_booking(request, pk):

    try:
        booking = Booking.objects.get(id=pk)

    except Booking.DoesNotExist:
        return Response(
            {"error": "Booking not found"},
            status=404
        )

    if booking.status == "Cancelled":
        return Response(
            {"message": "Booking already cancelled"},
            status=400
        )

    booking.status = "Cancelled"
    booking.save()

    try:

        resend.Emails.send({

            "from": "TravelX <onboarding@resend.dev>",
            "to": [booking.email],
            "subject": "Booking Cancelled",

            "html": f"""
            <h2 style="color:red;">Booking Cancelled ❌</h2>

            <p>Hello <b>{booking.full_name}</b>,</p>

            <p>Your booking has been cancelled successfully.</p>

            <table cellpadding="8">

                <tr>
                    <td><b>Booking ID</b></td>
                    <td>{booking.booking_id}</td>
                </tr>

                <tr>
                    <td><b>Destination</b></td>
                    <td>{booking.destination.place}</td>
                </tr>

                <tr>
                    <td><b>Status</b></td>
                    <td>Cancelled</td>
                </tr>

            </table>

            <br>

            <p>Thank you for using <b>TravelX</b>.</p>
            """

        })

    except Exception as e:
        print("Email Error:", e)

    return Response({
        "message": "Booking cancelled successfully"
    })
# ===========================
# Contact APIs
# ===========================

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by("-created_at")
    serializer_class = ContactSerializer


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def create_contact(request):

    serializer = ContactSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ===========================
# Register API
# ===========================

@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def register(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# ===========================
# Newsletter API
# ===========================

@api_view(["GET", "POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def newsletter(request):

    if request.method == "POST":

        email = request.data.get("email")

        if not email:
            return Response(
                {"message": "Email required"},
                status=400
            )

        if Newsletter.objects.filter(email=email).exists():
            return Response(
                {"message": "Email already subscribed"},
                status=400
            )

        Newsletter.objects.create(email=email)

        return Response(
            {"message": "Subscribed successfully"}
        )

    return Response(
        {"message": "Newsletter API Working"}
    )


# ===========================
# Hotel Booking API
# ===========================

@api_view(["GET", "POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def hotel_booking(request):

    if request.method == "GET":

        bookings = HotelBooking.objects.all().order_by("-id")

        data = []

        for booking in bookings:

            data.append({
                "id": booking.id,
                "full_name": booking.full_name,
                "email": booking.email,
                "phone": booking.phone,
                "destination": booking.destination,
                "travel_date": booking.travel_date,
                "travelers": booking.travelers,
                "hotel_type": booking.hotel_type,
                "special_request": booking.special_request,
                "status": booking.status,
            })

        return Response(data)

    HotelBooking.objects.create(
        full_name=request.data.get("full_name"),
        email=request.data.get("email"),
        phone=request.data.get("phone"),
        destination=request.data.get("destination"),
        travel_date=request.data.get("travel_date"),
        travelers=request.data.get("travelers"),
        hotel_type=request.data.get("hotel_type"),
        special_request=request.data.get("special_request", "")
    )

    return Response(
        {"message": "Hotel Booking Successful"},
        status=status.HTTP_201_CREATED
    )