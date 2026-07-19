from django.urls import path
from .views import hotel_booking
from .views import cancel_booking

from . import views

urlpatterns = [

    path("register/", views.register, name="register"),

    path("destinations/", views.destinations, name="destinations"),

    path("bookings/", views.create_booking, name="create_booking"),

    path("contacts/", views.create_contact, name="create_contact"),

    path("newsletter/", views.newsletter, name="newsletter"),

    path("hotel-booking/", hotel_booking),

    path( "cancel-booking/<int:pk>/", views.cancel_booking,),

]
# from django.urls import path
# from .views import (
#     BookingCreateView,
#     BookingListView
# )


# urlpatterns = [

#     path(
#         "bookings/",
#         BookingCreateView.as_view()
#     ),


#     path(
#         "bookings/list/",
#         BookingListView.as_view()
#     ),

# ]