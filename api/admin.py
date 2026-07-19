from django.contrib import admin
from .models import Destination, Booking
from django.contrib import admin
from .models import Contact
from django.contrib import admin
from .models import Newsletter
from django.contrib import admin
from .models import HotelBooking



admin.site.register(Destination)
admin.site.register(Booking)
admin.site.register(Contact)
admin.site.register(Newsletter)
admin.site.register(HotelBooking)
